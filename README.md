# Deutsch-TTS
A Text-To-Speech system made to "speak" German

best enjoyed with subtitles

https://github.com/user-attachments/assets/a21cb0d3-e3d6-4ee6-8708-91c9258c3381

---

### Current Functionality
- generate most sounds in the German language (except h and j, as they're reliant on the vowel that comes after them)
- Text-To-Speech

### Functionality to come
- text normalization (for example `bzw.`, `usw.`, `5 €`, `MfG`, etc.)

---

### Requirements
`NumPy` and `SciPy` python modules have to be installed
```
pip install numpy scipy
```

### Usage
- Step 1:
  Clone the repository
  ```
  git clone https://github.com/sckart42/Deutsch-TTS
  ```
  
  or, just download both scripts and put them in a shared directory (a new directory is recommended to avoid clutter)
  
- Step 2:
  Run TTS.py
  ```
  python TTS.py
  ```

  or, in quick mode, which takes `input.txt` as input and `output.wav` as output
  ```
  python TTS.py -q
  ```
  
- Step 3:
  Follow the instructions on screen (if you did not run in quick mode)
