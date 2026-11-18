# synthesizes sounds

import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import os

rate = 16000; pitch = 140
os.makedirs("sounds", exist_ok=True)
np.random.seed(42)

src = np.zeros(int(rate))
src[::rate // pitch] = 1.0
out = src

# The following function I did not write. In fact, I do not know at all how the math behind it does the magic, but it works. This is a chinese room to me. God bless the internet.
def resonator (x, freq, bw):
    C = -np.exp(-2 * np.pi * bw / rate)
    B = 2 * np.exp(-np.pi * bw / rate) * np.cos(2 * np.pi * freq / rate)
    A = 1 - B - C
    return lfilter([A], [1, -B, -C], x)

def antiresonator (x, freq, bw):
    C = -np.exp(-2 * np.pi * bw / rate)
    B = 2 * np.exp(-np.pi * bw / rate) * np.cos(2 * np.pi * freq / rate)
    A = 1 - B - C
    return lfilter([1, -B, -C], [A], x)

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
    ["i", 369, 1902, 3000, 0.1], # it indeed sounded bad, so I reverted it
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
    ["e-", 517, 1447, 2500, 0.1], # this is an unstressed e

    # the following are consonants but I'm not going to rename the list because of them
    ["l", 360, 1300, 2700, 0.1],
    ["r-", 450, 1450, 2500, 0.1]] # uvular r

for i in vowels:
    name = i[0]
    fr1 = i[1]
    fr2 = i[2]
    fr3 = i[3]
    length = i[4]

    out = out[:int(rate * length)]

    for fr, bw in [(fr1, 60), (fr2, 90), (fr3, 150)]:
        out = resonator(out, fr, bw)

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
    x = resonator(src[:int(samples)], 300, 400)
    return x / np.max(np.abs(x))



wav("s", fade(hiss(140, 5500, 1500)))
wav("sch", fade(hiss(140, 2600, 1000)))
wav("ch", fade(hiss(140, 1200, 1200)) * 0.5)

f = noise(140)
wav("f", fade(f / np.max(np.abs(f))) * 0.3)

wav("z", fade(hiss(115, 5500, 1500) * 0.3 + buzz(115) * 0.7)) # sounds like an English z; in German it's always an s like in Sonne
wav("v", fade(hiss(115, 5000, 4000) * 0.1 + buzz(115) * 0.7))


t = np.concatenate([silence(60), click(12, 4000, 1200), 0.3 * fade(hiss(30, 5500, 1500))])
wav("t", t)
k = np.concatenate([silence(60), click(15, 2000, 1000), 0.3 * fade(hiss(40, 2500, 1500))])
wav("k", k)
p = np.concatenate([silence(60), click(10, 800, 1500), 0.2 * fade(hiss(20, 1500, 2000))])
wav("p", p)

g = np.concatenate([0.15 * fade(buzz(30)), 0.7 * click(20, 2000, 600), 0.2 * fade(hiss(20, 2200, 800))])
wav("g", g)
d = np.concatenate([0.15 * fade(buzz(30)), 0.7 * click(20, 4000, 1200)])
wav("d", d)
b = np.concatenate([0.15 * fade(buzz(30)), 0.6 * click(20, 800, 1500)])
wav("b", b)


nasals = [
    ["m", 115, 1000],
    ["n", 115, 1500],
    ["ng", 115, 3200]]

for i in nasals:
    name = i[0]
    length = i[1]
    freq = i[2]
    samples = int(rate * length / 1000)

    out = resonator(src[:samples], 250, 100)
    out = resonator(out, 2500, 300)
    out = antiresonator(out, freq, 150)
    out /= np.max(np.abs(out))
    out = fade(out) * 0.5

    wav(name, out)


# I wanted to just glue these sounds (eg t and s) together but it didn't sound natural for some reason, so we're just going to regenerate both and glue them together before they're audio files
ts = np.concatenate([silence(60), click(12, 4000, 1200), fade(hiss(80, 5500, 1500))])
wav("ts", ts)
tsch = np.concatenate([silence(60), click(12, 4000, 1200), fade(hiss(80, 2600, 1000))])
wav("tsch", tsch)
pf = np.concatenate([silence(60), click(10, 800, 1500), fade(f / np.max(np.abs(f))) * 0.3])
wav("pf", pf)

wav("zh", fade(hiss(115, 2600, 1000) * 0.15 + buzz(115) * 0.8)) # eg Gara`g`e, `J`ournal


def trill (ms):
    trill_hz=25
    depth=0.85
    sharpness=5

    samples = int(rate * ms / 1000)
    r = src[:samples]
    for fr, bw in [(450, 60), (1450, 90), (2500, 150)]:
        r = resonator(r, fr, bw)
    t = np.arange(samples) / rate
    closure = ((1 - np.cos(2 * np.pi * trill_hz * t)) / 2) ** sharpness
    r /= np.max(np.abs(r))
    r *= (1 - depth * closure)
    return r
wav("r+", fade(trill(115))) # rolling r
