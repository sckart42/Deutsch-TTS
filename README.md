# Deutsch-TTS
A Text-To-Speech system made to "speak" German

best enjoyed with subtitles

---

### Current Functionality
- generate most sounds in the German language (except h and j, as they're reliant on the vowel that comes after them)
- Text-To-Speech

### Functionality to come
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
  Run TTS.py
  ```
  python TTS.py
  ```

  or, in quick mode, which takes `input.txt` as input and uses `output.wav` as output
  ```
  python TTS.py -q
  ```
  
- Step 2:
  Follow the instructions on screen (if you did not run in quick mode)
