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

from . import u4
from pyrbo import turbo
import numpy as np

@turbo(ampsize = u4, outp = [np.float32], naivex2outxp = [np.int32], outsize = u4, demultiplexedp = [np.float32], naivex2offp = [np.int32], ampp = [np.float32], naivex = u4, naiverate = u4, outrate = u4, mixinsize = u4, out0 = u4, dclevel = np.float32, dcindex = u4, ampchunk = u4, a = np.float32, i = u4, k = u4, mixinp = [np.float32])
def pasteminbleps(ampsize, outp, naivex2outxp, outsize, demultiplexedp, naivex2offp, ampp, naivex, naiverate, outrate, mixinsize):
    # TODO LATER: This code needs tests.
    out0 = naivex2outxp[naivex]
    dclevel = 0
    dcindex = 0
    while ampsize:
        ampchunk = min(ampsize, naiverate - naivex)
        for naivex in range(naivex, naivex + ampchunk):
            a = ampp[0]
            ampp += 1
            if a:
                i = naivex2outxp[naivex] - out0
                mixinp = demultiplexedp + naivex2offp[naivex]
                if dcindex <= i: # We can DC-adjust while pasting this mixin.
                    k = i - dcindex
                    for UNROLL, CLOBBER in range(k):
                        outp[0] += dclevel
                        outp += 1
                    for UNROLL, k in range(mixinsize):
                        outp[0] += mixinp[0] * a + dclevel
                        outp += 1
                        mixinp += 1
                else: # The mixin starts before the pending DC adjustment.
                    k = i + mixinsize - dcindex
                    for UNROLL, CLOBBER in range(k):
                        outp[0] += dclevel
                        outp += 1
                    outp -= mixinsize
                    for UNROLL, k in range(mixinsize):
                        outp[0] += mixinp[0] * a
                        outp += 1
                        mixinp += 1
                dcindex = i + mixinsize
                dclevel += a
        ampsize -= ampchunk
        naivex = 0
        out0 -= outrate
    k = outsize - dcindex
    for UNROLL, CLOBBER in range(k):
        outp[0] += dclevel
        outp += 1
