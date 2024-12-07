# Copyright 2014, 2020 Andrzej Cichocki and contributors

# This file is part of minBlepy.
#
# minBlepy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# minBlepy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with minBlepy.  If not, see <http://www.gnu.org/licenses/>.

from . import floatdtype
from .paste import pasteminbleps
try:
    from fractions import gcd
except ImportError:
    # python >= 3.9
    from math import gcd
from lagoon.util import atomic
from pathlib import Path
import logging, numpy as np, pickle

log = logging.getLogger(__name__)

class MinBleps:

    defaultcutoff = .475
    defaulttransition = .05
    minmag = np.exp(-100)

    @staticmethod
    def round(v):
        return np.int32(v + .5)

    @staticmethod
    def resolvescale(naiverate, outrate, scaleornone):
        idealscale = naiverate // gcd(naiverate, outrate)
        if scaleornone is not None and scaleornone != idealscale:
            raise Exception("Expected scale %s but ideal is %s." % (scaleornone, idealscale))
        return idealscale

    @classmethod
    def loadorcreate(cls, naiverate, outrate, scaleornone, cutoff = defaultcutoff, transition = defaulttransition):
        scale = cls.resolvescale(naiverate, outrate, scaleornone)
        path = Path.home() / '.cache' / 'minBlepy' / f"{cls.__name__}({','.join(map(repr, [naiverate, outrate, scale, cutoff, transition]))})"
        if path.exists():
            log.debug("Loading cached minBLEPs: %s", path)
            with path.open('rb') as f:
                minbleps = pickle.load(f)
            log.debug("Cached minBLEPs loaded.")
        else:
            minbleps = cls(naiverate, outrate, scale, cutoff, transition)
            with atomic(path) as q, q.open('wb') as f:
                pickle.dump(minbleps, f, pickle.HIGHEST_PROTOCOL)
        return minbleps

    @classmethod
    def create(cls, naiverate, outrate, scaleornone, cutoff = defaultcutoff, transition = defaulttransition):
        return cls(naiverate, outrate, cls.resolvescale(naiverate, outrate, scaleornone), cutoff, transition)

    def __init__(self, naiverate, outrate, scale, cutoff, transition):
        log.debug('Creating minBLEPs.')
        # XXX: Use kaiser and/or satisfy min transition?
        # Closest even order to 4/transition:
        order = int(self.round(4 / transition / 2)) * 2
        kernelsize = order * scale + 1
        # The fft/ifft are too slow unless size is a power of 2:
        size = 2 ** 0
        while size < kernelsize:
            size <<= 1
        midpoint = size // 2 # Index of peak of sinc.
        x = (np.arange(kernelsize) / (kernelsize - 1) * 2 - 1) * order * cutoff
        # If cutoff is .5 the sinc starts and ends with zero.
        # The window is necessary for a reliable integral height later:
        self.bli = np.blackman(kernelsize) * np.sinc(x) / scale * cutoff * 2
        rpad = (size - kernelsize) // 2 # Observe floor of odd difference.
        lpad = 1 + rpad
        self.bli = np.concatenate([np.zeros(lpad), self.bli, np.zeros(rpad)])
        # Everything is real after we discard the phase info here:
        absdft = np.abs(np.fft.fft(self.bli))
        # The "real cepstrum" is symmetric apart from its first element:
        realcepstrum = np.fft.ifft(np.log(np.maximum(self.minmag, absdft)))
        # Leave first point, zero max phase part, double min phase part to compensate.
        # The midpoint is shared between parts so it doesn't change:
        realcepstrum[1:midpoint] *= 2
        realcepstrum[midpoint + 1:] = 0
        self.minbli = np.fft.ifft(np.exp(np.fft.fft(realcepstrum))).real
        self.minblep = np.cumsum(self.minbli, dtype = floatdtype)
        # Prepend zeros to simplify naivex2outx calc:
        self.minblep = np.append(np.zeros(scale - 1, floatdtype), self.minblep)
        # Append ones so that all mixins have the same length:
        ones = (-len(self.minblep)) % scale
        self.minblep = np.append(self.minblep, np.ones(ones, floatdtype))
        self.mixinsize = len(self.minblep) // scale
        # The naiverate and outrate will line up at 1 second:
        dualscale = outrate // gcd(naiverate, outrate)
        nearest = np.arange(naiverate, dtype = np.int32) * dualscale
        self.naivex2outx = nearest // scale
        self.naivex2shape = self.naivex2outx * scale - nearest + scale - 1
        self.demultiplexed = np.empty(self.minblep.shape, dtype = self.minblep.dtype)
        for i in range(scale):
            self.demultiplexed[i * self.mixinsize:(i + 1) * self.mixinsize] = self.minblep[i::scale]
        self.naivex2off = self.naivex2shape * self.mixinsize
        self.outx2minnaivex = np.empty(outrate, dtype = self.naivex2outx.dtype)
        for naivex in range(naiverate)[::-1]:
            self.outx2minnaivex[self.naivex2outx[naivex]] = naivex
        log.debug('%s minBLEPs created.', scale)
        self.naiverate = naiverate
        self.outrate = outrate

    def getoutcount(self, naivex, naiven):
        out0 = self.naivex2outx[naivex]
        naivex += naiven
        shift = naivex // self.naiverate
        out0 -= self.outrate * shift
        naivex -= self.naiverate * shift
        # Subtract from the first sample we can't output this block:
        return self.naivex2outx[naivex] - out0

    def getminnaiven(self, naivex, outcount):
        outx = self.naivex2outx[naivex] + outcount
        shift = outx // self.outrate
        outx -= self.outrate * shift
        naivex -= self.naiverate * shift
        return self.outx2minnaivex[outx] - naivex

    def paste(self, naivex, diffbuf, outbuf):
        '''Add minBLEPs to `outbuf` for the differentiated naive signal block in `diffbuf`.
        The first element of `diffbuf` should be the first naive value in the current block minus the last naive value of the previous block.
        The `naivex` is the index of the first naive value, modulo `naiverate`.
        The `outbuf` must have enough space for overflow of the last possible minBLEP, and should be initialised to the overflow section of the previous `outbuf` and otherwise zero.'''
        pasteminbleps(len(diffbuf), outbuf, self.naivex2outx, len(outbuf), self.demultiplexed, self.naivex2off, diffbuf, naivex, self.naiverate, self.outrate, self.mixinsize)

class Translator:

    naivex = 0

    def __init__(self, naiverate, minbleps):
        self.naiverate = naiverate
        self.minbleps = minbleps

    def step(self, framecount):
        naivex = self.naivex
        outcount = self.minbleps.getoutcount(naivex, framecount)
        self.naivex = (naivex + framecount) % self.naiverate
        return naivex, outcount
