import tkinter
import fixtext
import customtkinter as ctk
from tkinter import *
from spellchecker import SpellChecker
from PIL import Image

spell = SpellChecker()

# set ctk default colors
ctk.set_default_color_theme("green.json")

# create root window and set name
root = ctk.CTk()
root.title("Gramma Dictionary")
root.iconbitmap("image/GD.ico")
root.minsize(1140, 500)
root.resizable(False, False)


def process():
    text = inputText.get(0.0, ctk.END)
    spelling_correction = fixtext.spellcheck(text)
    grammer_correction = fixtext.fix_grammar()
    outputText.configure(state="normal")
    outputText.delete(0.0, ctk.END)
    outputText.insert(0.0, spelling_correction)
    outputText.configure(state="disabled")
    inputText.delete(0.0, ctk.END)


def text_to_speech():
    text = outputText.get(0.0, ctk.END)
    print(text)


side_frame = ctk.CTkFrame(root, height=620)
GDimage = ctk.CTkImage(dark_image=Image.open("image/Gramma Dictionary.png"), size=(200, 100))
appImg = ctk.CTkLabel(side_frame, image=GDimage, text="")
tts_frame = ctk.CTkFrame(side_frame)

ttsLabel = ctk.CTkLabel(tts_frame, text="Text To Speech Options")
talkButton = ctk.CTkButton(tts_frame, text="TTS", command=text_to_speech)

voiceRadioButtonMale = ctk.CTkRadioButton(tts_frame, text="Male", value=0)
voiceRadioButtonFemale = ctk.CTkRadioButton(tts_frame, text="Female", value=1)

outputText = ctk.CTkTextbox(root, state="disabled", width=900, height=500)
inputText = ctk.CTkTextbox(root, width=800, height=100)
sendButton = ctk.CTkButton(root, text="Process", command=process, width=100, height=50)

side_frame.grid(row=0, column=0, rowspan=2, sticky="snwe")
appImg.grid(row=0, column=0, padx=5, pady=5)
tts_frame.grid(row=1, column=0)

outputText.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
inputText.grid(row=1, column=1, sticky="we", padx=10, pady=10)
sendButton.grid(row=1, column=2, sticky="e", padx=10, pady=10)

ttsLabel.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
talkButton.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
voiceRadioButtonMale.grid(row=2, column=0, padx=10, pady=10)
voiceRadioButtonFemale.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
