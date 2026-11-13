# synthesizes sounds

import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import os

rate = 16000; pitch = 140
os.makedirs("sounds", exist_ok=True)

src = np.zeros(int(rate / 5))
src[::rate // pitch] = 1.0

# The following function I did not write. In fact, I do not know at all how the math behind it does the magic, but it works. This is a chinese room to me. God bless the internet.
def resonator (x, freq, bw):
    C = -np.exp(-2 * np.pi * bw / rate)
    B = 2 * np.exp(-np.pi * bw / rate) * np.cos(2 * np.pi * freq / rate)
    A = 1 - B - C
    return lfilter([A], [1, -B, -C], x)
out = src

vowels = [
    ["a", 694, 1372, 2500, 0.1], # single letter = short
    ["aa", 737, 1275, 2500, 0.2], # double letter = long
    ["e", 489, 1817, 2500, 0.1],
    ["ee", 348, 2126, 2500, 0.2],
    ["i", 300, 2300, 3000, 0.1], # sounded to much like e so I adjusted it. Will revert to the earlier value if it sounds bad
    ["ie", 263, 2171, 3000, 0.2], # this is also long
    ["o", 537, 1074, 2500, 0.1],
    ["oo", 383, 841, 2500, 0.2],
    ["u", 391, 1010, 2500, 0.1],
    ["uu", 310, 854, 2500, 0.2],
    ["ae", 482, 1902, 2500, 0.2], # this one is also long; the short one sounds the same as e
    ["oe", 474, 1477, 2500, 0.1],
    ["oee", 371, 1501, 2500, 0.2], # this is also long
    ["ue", 373, 1543, 2500, 0.1],
    ["uee", 302, 1722, 2500, 0.2],
    ["e-", 517, 1447, 2500, 0.07]] # this is an unstressed e

for i in vowels:
    name = "sounds/" + i[0] + ".wav"
    fr1 = i[1]
    fr2 = i[2]
    fr3 = i[3]
    length = i[4]

    out = out[:int(rate * length)]

    for f, bw in [(fr1, 60), (fr2, 90), (fr3, 150)]:
        out = resonator(out, f, bw)

    out /= np.max(np.abs(out))
    wavfile.write(name, rate, (out * 0.8 * 32767).astype(np.int16))

    out = src
