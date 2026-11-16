# Deutsch-TTS
A Text-To-Speech system made to "speak" German

---

### Current Functionality
- generate most sounds in the German language (except h and j, as they're reliant on the vowel that comes after them)  

### Functionality to come
- text-to-speech (pick the correct sounds and glue them into a big .wav file)
- text normalization (for example `bzw.`, `usw.`, `5 €`, `MfG`, etc.)

### Functionality that might be added later; no guarantees
- different voices

---

### Requirements
`NumPy` and `SciPy` python modules have to be installed
```
pip install numpy scipy
```

### Usage
- Step 1:
  Generate the sound library (generates a `sounds/` directory in the location you run the script from)
  ```
  python synth.py
  ```

- Step 2:
  Wait until I finish the actual TTS
