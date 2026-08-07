# pip install pyttsx3
# pip uninstall pyttsx3
# This is a Text-to-Speech (TTS) module.

import pyttsx3
engine=pyttsx3.init()
engine.say("Hello Abhishek Giri, How Are You? What Are You Doing?")
engine.runAndWait()
