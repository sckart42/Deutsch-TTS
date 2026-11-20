#uses sounds from the library built by synth.py to say words

import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import os
import sys
import argparse
from synth import resonator, fade, vowels, wav, rate, pitch, silence
import re

os.makedirs("output", exist_ok=True)
np.random.seed(42)

# this is UX code
parser = argparse.ArgumentParser(description="German TTS System")
modes = parser.add_mutually_exclusive_group()
modes.add_argument("-q", action="store_true", help="launch in quick mode (input.txt as input and output.wav as output)")
# modes.add_argument("-n", action="store_true", help="normalize text and exit without using TTS")
args = parser.parse_args()

if args.q == False:
    filename = input("Please enter the filename of your text file, without the .txt extension. The file has to be located inside the same folder as this script. ")
    if os.path.exists(filename + ".txt"):
        with open(filename + ".txt", encoding="utf-8") as f:
            text = f.read()
        print()
        print(text)
        conf = input("Is this correct? [Y/n] ")
        if conf == "n" or conf == "N":
            sys.exit()
    else:
        sys.exit("File " + filename + ".txt" + " doesn't exist")


if args.q == False: #and args.n == False
    output = input("How would you like the output file to be called (without the .wav extension)? ")


if args.q:
    filename = "input.txt"
    output = "output"
    if os.path.exists(filename):
        with open(filename, encoding="utf-8") as f:
            text = f.read()
    else:
        sys.exit("input.txt doesn't exist")



# these are functions for generating h and j, since they're dependent on the vowel after them, and I couldn't just generate static sounds for them because of that
formants = {v[0]: v[1:4] for v in vowels}

def h (vowel):
    if vowel in ("ä", "ö", "ü"):
        if vowel == "ä":
            vowel = "ae"
        elif vowel == "ö":
            vowel = "oe"
        else:
            vowel = "ue"

    x = np.random.randn(int(rate * 0.1))
    for fr, bw in zip(formants[vowel], (200, 300, 400)):
        x = resonator(x, fr, bw)
    x = fade(x / np.max(np.abs(x))) * 0.3
    return x

def j (vowel):
    if vowel in ("ä", "ö", "ü"):
        if vowel == "ä":
            vowel = "e" # the short one is e and the long one is ae
        elif vowel == "ö":
            vowel = "oe"
        else:
            vowel = "ue"

    samples = int(rate * 0.1)
    src = np.zeros(samples)
    src[::rate // pitch] = 1.0
    a = src
    b = src
    for fr, bw in zip(formants["ie"], (60, 90, 150)):
        a = resonator(a, fr, bw)
    for fr, bw in zip(formants[vowel], (60, 90, 150)):
        b = resonator(b, fr, bw)
    ramp = np.linspace(0, 1, samples)
    x = (a / np.max(np.abs(a))) * (1 - ramp) + (b / np.max(np.abs(b))) * ramp
    x = fade(x / np.max(np.abs(x))) * 0.7
    return x

# for diphthongs
def glide (v1, v2):
    samples = int(rate * 0.2)
    src = np.zeros(samples)
    src[::rate // pitch] = 1.0
    a = src
    b = src
    for fr, bw in zip(formants[v1], (60, 90, 150)):
        a = resonator(a, fr, bw)
    for fr, bw in zip(formants[v2], (60, 90, 150)):
        b = resonator(b, fr, bw)
    ramp = np.linspace(0, 1, samples)
    x = (a / np.max(np.abs(a))) * (1 - ramp) + (b / np.max(np.abs(b))) * ramp
    x = fade(x / np.max(np.abs(x))) * 0.7
    return x






# this is the part for the actual TTS
text_lc = text.lower()
words = re.split(r'(\W)', text_lc)
sounds = []
sounds.append(silence(200))
vowellist = ["a", "e", "i", "o", "u", "ä", "ö", "ü"]
print(words)

def load (name):
    if name in ("ä", "ö", "ü"):
        if name == "ä":
            name = "e" # the short one is e and the long one is ae
        elif name == "ö":
            name = "oe"
        else:
            name = "ue"

    r, x = wavfile.read("sounds/" + name + ".wav")
    if x.dtype == np.int16:
        x = x / 32767
    return x

def load_long (vowel):
    if vowel in ("a", "e", "o", "u"):
        name = vowel * 2
    elif vowel == "i":
        name = "ie"
    elif vowel == "ä":
        name = "ae" # the short one is e and the long one is ae
    elif vowel == "ö":
        name = "oee"
    elif vowel == "ü":
        name = "uee"

    return load(name)

for w in words:
    x = 0
    syll = 0 # syllables
    while x < len(w):
        if w[x:x+4] == "tsch":
            sounds.append(load("tsch"))
            x += 4
        elif x <= len(w) - 4 and x >= len(w) - 6 and  w[x:x+4] == "tion":
            sounds.append(load("ts"))
            x += 1
        elif w[x:x+3] == "sch":
            sounds.append(load("sch"))
            x += 3
        elif w[x:x+3] == "chs":
            sounds.append(load("k"))
            sounds.append(load("s")) # ks as in sechs
            x += 3
        elif w[x:x+2] == "pf":
            sounds.append(load("pf"))
            x += 2
        elif w[x:x+2] == "tz":
            sounds.append(load("ts"))
            x += 2
        elif w[x:x+2] == "dt":
            sounds.append(load("t"))
            x += 2
        elif w[x:x+2] == "au":
            sounds.append(glide("a", "u"))
            syll += 1
            x += 2
        elif w[x:x+2] in ("ei", "ai"):
            sounds.append(load("a"))
            sounds.append(j("ie"))
            syll += 1
            x += 2
        elif w[x:x+2] in ("eu", "oi"):
            sounds.append(load("o"))
            sounds.append(j("ie"))
            syll += 1
            x += 2
        elif w[x:x+2] == "äu":
            sounds.append(load("oe"))
            sounds.append(j("ie"))
            syll += 1
            x += 2
        elif w[x:x+2] in ("ng", "nk"):
            sounds.append(load("ng"))
            if w[x+1] == "k":
                sounds.append(load("k"))
            x += 2
        elif w[x:x+2] == "ie":
            sounds.append(load("ie"))
            syll += 1
            x += 2
        elif w[x:x+2] == "ss":
            sounds.append(load("s"))
            x += 2
        elif x < len(w) - 1 and w[x] not in vowellist and w[x] == w[x+1]:
            x += 1
        elif x == 0 and w[x:x+2] in ("sp", "st"):
            sounds.append(load("sch"))
            x += 1
        elif w[x:x+2] == "qu":
            sounds.append(load("k"))
            sounds.append(load("v"))
            x += 2
        elif w[x:x+2] == "ck":
            sounds.append(load("k"))
            x += 2
        elif w[x:x+2] == "ch":
            if x == 0:
                sounds.append(load("ch"))
            else:
                if w[x-2:x] in ("eu", "äu"):
                    sounds.append(load("sch")) # hessian accent: ich laut -> sch
                else:
                    if w[x-1] in ("a", "o", "u"):
                        sounds.append(load("ch"))
                    else:
                        sounds.append(load("sch")) # hessian accent: ich laut -> sch
            x += 2
        else:
            if w[x] in ("b", "d", "g") and w[x+1:x+2] not in vowellist and w[x+1:x+2] not in ("l", "r", "n"):
                if w[x] == "b":
                    sounds.append(load("p"))
                elif w[x] == "d":
                    sounds.append(load("t"))
                else:
                    sounds.append(load("k"))
            elif w[x] in ("b", "d", "f", "g", "k", "m", "p", "t", "z", "n", "w", "ß", "l", "x", "y", "q", "c"):
                if w[x] == "z":
                    sounds.append(load("ts"))
                elif w[x] == "w":
                    sounds.append(load("v"))
                elif w[x] == "ß":
                    sounds.append(load("s"))
                elif w[x] == "x":
                    sounds.append(load("k"))
                    sounds.append(load("s"))
                elif w[x] == "y":
                    sounds.append(load("uee"))
                elif w[x] in ("q", "c"):
                    sounds.append(load("k")) # idk how to interpret a q without the u so I'll just inteerpret it as k (from how the letter is called, 'ku')
                else:
                    sounds.append(load(w[x]))

            elif w[x] == "v":
                    sounds.append(load("f"))
            elif w[x] == "s":
                if x != len(w) - 1 and w[x+1] in vowellist:
                    sounds.append(load("z"))
                else:
                    sounds.append(load("s"))
            elif w[x] == "r":
                if x != len(w) - 1 and w[x+1] in vowellist:
                    sounds.append(load("r+"))
                else:
                    sounds.append(load("r-"))
            elif w[x] == "j":
                if x != len(w) - 1 and w[x+1] in vowellist:
                    sounds.append(j(w[x+1]))
                else:
                    sounds.append(j("ie"))
            elif w[x] == "h":
                if x > 0 and w[x-1] in vowellist:
                    2+2
                elif x != len(w) - 1 and w[x+1] in vowellist:
                    sounds.append(h(w[x+1]))
                else:
                    print("Stray h") # this isn't supposed to happen btw

            elif w[x] == "e":
                if w in ("an", "in", "mit", "ab", "ob", "bin", "hat", "was", "das", "es", "bis", "man", "hin", "von", "um", "zum", "vom", "im", "am", "des"):
                    sounds.append(load("e"))

                elif x == len(w) - 1 or x == len(w) - 2 and w[x+1] in ("n", "r", "l", "m", "s", "t"):
                    if syll == 0:
                        sounds.append(load_long("e"))
                    else:
                        sounds.append(load("e-"))
                elif w[x+1] in vowellist:
                    sounds.append(load_long("e"))
                    if w[x+1] == "e":
                        x += 1 # skip two ahead
                elif w[x+1] == "h":
                    sounds.append(load_long(w[x]))
                    x += 1 # skip two ahead
                elif x != len(w) - 2 and w[x+2] not in vowellist:
                    sounds.append(load("e"))
                else:
                    sounds.append(load_long("e"))
                syll += 1

            elif w[x] in vowellist:
                if w in ("an", "in", "mit", "ab", "ob", "bin", "hat", "was", "das", "es", "bis", "man", "hin", "von", "um", "zum", "vom", "im", "am", "des"):
                    sounds.append(load(w[x]))
                elif w in ("buch", "tuch", "fluch", "besuch", "versuch", "suchen", "buchen", "fluchen", "kuchen", "buche", "bücher", "tücher", "wucher", "nach", "sprache", "brache", "schmach", "hoch"):
                    sounds.append(load_long(w[x]))
                elif x == len(w) - 1:
                    if syll > 0:
                        sounds.append(load(w[x]))
                    else:
                        sounds.append(load_long(w[x]))
                elif w[x+1] in vowellist:
                    sounds.append(load_long(w[x]))
                    if w[x] == w[x+1]:
                        x += 1 # skip two ahead
                elif w[x+1] == "h":
                    sounds.append(load_long(w[x]))
                    x += 1 # skip two ahead
                elif x != len(w) - 2 and w[x+2] not in vowellist:
                    sounds.append(load(w[x]))
                else:
                    sounds.append(load_long(w[x]))
                syll += 1


            elif w[x] == " ":
                sounds.append(silence(75))
            elif w[x] in (",", ";", ":", "-", "—", "–"): # turns out that besides em dashes and hyphens there are also en dashes
                sounds.append(silence(200))
            elif w[x] in (".", "!", "?", "\n"):
                sounds.append(silence(400))
            else:
                print('No sound found for: ' + w[x])
            x += 1


# generate the big wav file
wavfile.write("output/" + output + ".wav", rate, (np.concatenate(sounds) * 0.8 * 32767).astype(np.int16))
