# synthesizes sounds

import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import os

rate = 16000; pitch = 140
os.makedirs("sounds", exist_ok=True)

src = np.zeros(int(rate / 5))
src[::rate // pitch] = 1.0
out = src

# The following function I did not write. In fact, I do not know at all how the math behind it does the magic, but it works. This is a chinese room to me. God bless the internet.
def resonator (x, freq, bw):
    C = -np.exp(-2 * np.pi * bw / rate)
    B = 2 * np.exp(-np.pi * bw / rate) * np.cos(2 * np.pi * freq / rate)
    A = 1 - B - C
    return lfilter([A], [1, -B, -C], x)

def wav (name, x):
    wavfile.write("sounds/" + name + ".wav", rate, (x * 0.8 * 32767).astype(np.int16))
    
def fade (x, ms=5):
    samples = int(rate * ms / 1000)
    x[:samples] *= np.linspace(0, 1, samples)
    x[-samples:] *= np.linspace(1, 0, samples)
    return x


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
    name = i[0]
    fr1 = i[1]
    fr2 = i[2]
    fr3 = i[3]
    length = i[4]

    out = out[:int(rate * length)]

    for f, bw in [(fr1, 60), (fr2, 90), (fr3, 150)]:
        out = resonator(out, f, bw)

    out = fade(out)
    out /= np.max(np.abs(out))
    wav(name, out)

    out = src



def silence (ms):
    samples = int(rate * ms / 1000)
    return np.zeros(samples)

def noise (ms):
    samples = int(rate * ms / 1000)
    return np.random.randn(samples)

def hiss (ms, freq, bw):
    x = resonator(noise(ms), freq, bw)
    return x / np.max(np.abs(x))

def click (ms, freq, bw):
    x = noise(ms)
    x *= np.exp(np.linspace(6, 0, len(x)))
    x = resonator(x, freq, bw)
    return x / np.max(np.abs(x))

def buzz (ms):
    samples = int(rate * ms / 1000)
    x = np.zeros(samples)
    x[::rate // pitch] = 1.0
    x = resonator(x, 300, 400)
    x /= np.max(np.abs(x))
    return x


wav("s", fade(hiss(140, 5500, 1500)))
wav("sch", fade(hiss(140, 2600, 1000)))
wav("ch", fade(hiss(140, 1700, 1200)) * 0.5)

f = noise(140)
wav("f", fade(f / np.max(np.abs(f))) * 0.3)

wav("z", fade(hiss(115, 5500, 1500) * 0.3 + buzz(115) * 0.7)) # sounds like an English z; in German it's always an s like in Sonne
wav("v", fade(hiss(115, 5000, 4000) * 0.2 + buzz(115) * 0.6))


t = np.concatenate([silence(60), click(12, 4000, 1200), 0.3 * fade(hiss(30, 5500, 1500))])
wav("t", t)
k = np.concatenate([silence(60), click(15, 2000, 1000), 0.3 * fade(hiss(40, 2500, 1500))])
wav("k", k)
p = np.concatenate([silence(60), click(10, 800, 1500), 0.2 * fade(hiss(20, 1500, 2000))])
wav("p", p)

g = np.concatenate([0.15 * fade(buzz(30)), 0.7 * click(20, 2000, 1000)])
wav("g", g)
d = np.concatenate([0.15 * fade(buzz(30)), 0.7 * click(20, 4000, 1200)])
wav("d", d)
b = np.concatenate([0.15 * fade(buzz(30)), 0.6 * click(20, 800, 1500)])
wav("b", b)
