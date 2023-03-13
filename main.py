import fixtext
import customtkinter as ctk
import tkinter as tk
from spellchecker import SpellChecker
from PIL import Image
import pyttsx3
import threading
import os
import difflib
import re
import webbrowser

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


def open_about_window():
    about_window = ctk.CTkToplevel(root)
    about_window.title("About")
    about_window.iconbitmap("image/GD.ico")
    about_window.geometry("700x300")
    about_window.resizable(False, False)
    text = """Welcome to Gramma Dictionary, your all-in-one tool for improving your writing!

At Gramma Dictionary, I understand the importance of clear and effective communication. That's why I've created an application that helps you fix spelling and grammar mistakes, as well as enhance the readability and engagement of your text.

My application is designed to be user-friendly and accessible, with features such as text-to-speech and dark/light mode that make it easy to use in any setting.

But that's not all – I also take plagiarism seriously. With my advanced plagiarism detection technology, you can ensure that your writing is original and free from any instances of academic dishonesty.

Whether you're a student, a professional writer, or just someone looking to improve your communication skills, Gramma Dictionary is the perfect tool for you. Try it out today and experience the power of clear and effective writing!"""
    about_label = ctk.CTkTextbox(about_window, width=680, height=280)
    about_label.grid(row=0, column=0, padx=10, pady=10)

    about_label.insert(ctk.END, text)


def plagiarism_Checker():
    text = outputText.get(0.0, ctk.END)
    pattern = r'\w+'
    words = re.findall(pattern, text)
    highlighted_text = text
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            similarity_ratio = difflib.SequenceMatcher(None, words[i], words[j]).ratio()
            if similarity_ratio >= 0.8:
                highlighted_text = highlighted_text.replace(words[i], '<span style="color:red">' + words[i] + '</span>')
                highlighted_text = highlighted_text.replace(words[j], '<span style="color:red">' + words[j] + '</span>')

    # write the highlighted text to an HTML file and open it in a web browser
    def write_and_open_html():
        with open(os.path.abspath('output.html'), 'w') as f:
            f.write(highlighted_text)
        webbrowser.open('file://' + os.path.abspath('output.html'))

    threading.Thread(target=write_and_open_html).start()


def detect_plagiarism_process():
    detect_plagiarism_process_thread = threading.Thread(target=plagiarism_Checker)
    detect_plagiarism_process_thread.start()


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

outputText.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
inputText.grid(row=1, column=1, sticky="we", padx=10, pady=10)
sendButton.grid(row=1, column=2, sticky="e", padx=10, pady=10)

plagiarism_frame = ctk.CTkFrame(side_frame)
plagiarismButton = ctk.CTkButton(plagiarism_frame, text="detect plagiarism", command=detect_plagiarism_process)

about_frame = ctk.CTkFrame(side_frame)
about_button = ctk.CTkButton(about_frame, text="About Us", command=open_about_window)

# side frame
side_frame.grid(row=0, column=0, rowspan=2, sticky="snwe")
appImg.grid(row=0, column=0, padx=5, pady=5)

# text to speach
tts_frame.grid(row=1, column=0)
ttsLabel.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
talkButton.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
voiceRadioButtonMale.grid(row=2, column=0, padx=10, pady=10)
voiceRadioButtonFemale.grid(row=2, column=1, padx=10, pady=10)

# add the theme switch buttons to the frame
theme_switch_frame.grid(row=2, column=0, sticky="we", pady=5)
theme_label.grid(row=0, column=0, padx=10, pady=10)
theme_switch.grid(row=1, column=0, padx=10, pady=10)

# plagiarism
plagiarism_frame.grid(row=3, column=0, sticky="we")
plagiarismButton.grid(row=0, column=0, padx=50, pady=10)

# about
about_frame.grid(row=4, column=0, sticky="we", pady=5)
about_button.grid(row=0, column=0, padx=50, pady=10)

root.mainloop()
