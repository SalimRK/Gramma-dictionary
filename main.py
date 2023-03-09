import fixtext
import customtkinter as ctk
import tkinter as tk
from spellchecker import SpellChecker
from PIL import Image
import pyttsx3
import threading
import os

spell = SpellChecker()
cwd = os.getcwd()
file_path = os.path.join(cwd, "themes")


def switch():
    global dark_theme_is_on

    # switch to light theme
    if dark_theme_is_on:
        ctk.set_appearance_mode("light")
        dark_theme_is_on = False
    else:
        ctk.set_appearance_mode("dark")
        dark_theme_is_on = True


# set ctk default colors
ctk.set_default_color_theme(os.path.join(file_path, "green.json"))
# create root window and set name
root = ctk.CTk()
root.title("Gramma Dictionary")
root.iconbitmap("image/GD.ico")
root.minsize(1140, 500)
root.resizable(False, False)

# Define TTS engine and voices
engine = pyttsx3.init()
voices = engine.getProperty('voices')

dark_theme_is_on = True


def fix_text():
    text = inputText.get(0.0, ctk.END)
    spelling_correction = fixtext.fix_spelling(text)
    grammar_correction = fixtext.fix_grammar(spelling_correction)
    outputText.configure(state="normal")
    outputText.delete(0.0, ctk.END)
    outputText.insert(0.0, grammar_correction)
    outputText.configure(state="disabled")
    inputText.delete(0.0, ctk.END)


def tts(text):
    voice = voice_var.get()
    engine.setProperty('voice', voices[voice].id)  # set TTS voice
    engine.say(str(text))
    engine.runAndWait()


def process():
    process_thread = threading.Thread(target=fix_text)
    process_thread.start()


def text_to_speech_process():
    text = outputText.get(0.0, ctk.END)
    tts_thread = threading.Thread(target=tts, args=(text,))
    tts_thread.start()


side_frame = ctk.CTkFrame(root, height=620)
GDimage = ctk.CTkImage(dark_image=Image.open("image/Gramma Dictionary.png"), size=(200, 100))
appImg = ctk.CTkLabel(side_frame, image=GDimage, text="")
tts_frame = ctk.CTkFrame(side_frame)

ttsLabel = ctk.CTkLabel(tts_frame, text="Text To Speech Options")
talkButton = ctk.CTkButton(tts_frame, text="TTS", command=text_to_speech_process)

voice_var = tk.IntVar(value=0)

voiceRadioButtonMale = ctk.CTkRadioButton(tts_frame, text="Male", variable=voice_var, value=0,
                                          command=lambda: engine.setProperty('voice', voices[voice_var.get()].id))
voiceRadioButtonFemale = ctk.CTkRadioButton(tts_frame, text="Female", variable=voice_var, value=4,
                                            command=lambda: engine.setProperty('voice', voices[voice_var.get()].id))

theme_switch_frame = ctk.CTkFrame(side_frame)  # create a frame to hold the theme switch buttons
theme_label = ctk.CTkLabel(theme_switch_frame, text="Switch to Dark/Light Theme", font=("TkDefaultFont", 12))
theme_switch = ctk.CTkSwitch(theme_switch_frame, text="Toggle Theme", command=switch)

outputText = ctk.CTkTextbox(root, state="disabled", width=900, height=500)
inputText = ctk.CTkTextbox(root, width=800, height=100)
sendButton = ctk.CTkButton(root, text="Process", command=process, width=100, height=50)

side_frame.grid(row=0, column=0, rowspan=2, sticky="snwe")
appImg.grid(row=0, column=0, padx=5, pady=5)
tts_frame.grid(row=1, column=0)
theme_switch_frame.grid(row=2, column=0, sticky="we", pady=5)

outputText.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
inputText.grid(row=1, column=1, sticky="we", padx=10, pady=10)
sendButton.grid(row=1, column=2, sticky="e", padx=10, pady=10)

ttsLabel.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
talkButton.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
voiceRadioButtonMale.grid(row=2, column=0, padx=10, pady=10)
voiceRadioButtonFemale.grid(row=2, column=1, padx=10, pady=10)

# add the theme switch buttons to the frame
ttsLabel.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
theme_label.grid(row=0, column=0, padx=10, pady=10)
theme_switch.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
