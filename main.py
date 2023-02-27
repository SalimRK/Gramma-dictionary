import customtkinter as ctk
import enchant
from PIL import Image

d = enchant.Dict("en_US")

# set ctk default colors
ctk.set_default_color_theme("green.json")

# create root window and set name
root = ctk.CTk()
root.title("Gramma Dictionary")
root.minsize(1140, 500)
root.resizable(False, False)


def fix_spelling(text):
    words = text.split(" ")
    for i, word in enumerate(words):
        if not d.check(word):
            suggestions = d.suggest(word)
            if len(suggestions) > 0:
                words[i] = suggestions[0]

    corrected_text = " ".join(words)
    print(corrected_text)
    return corrected_text


def process():
    text = inputText.get(0.0, ctk.END)
    correction = fix_spelling(text)
    outputText.configure(state="normal")
    outputText.delete(0.0, ctk.END)
    outputText.insert(0.0, correction)
    outputText.configure(state="disabled")
    inputText.delete(0.0, ctk.END)


side_frame = ctk.CTkFrame(root, height=620)


GDimage = ctk.CTkImage(dark_image=Image.open("image/Gramma Dictionary.png"), size=(200, 100))
appImg = ctk.CTkLabel(side_frame, image=GDimage, text="")
appImg.grid(row=0, column=0, padx=5, pady=5)


outputText = ctk.CTkTextbox(root, state="disabled", width=900, height=500)
inputText = ctk.CTkTextbox(root, width=800, height=100)
sendButton = ctk.CTkButton(root, text="Process", command=process, width=100, height=50)

side_frame.grid(row=0, column=0, rowspan=2, sticky="snwe")
outputText.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
inputText.grid(row=1, column=1, sticky="we", padx=10, pady=10)
sendButton.grid(row=1, column=2, sticky="e", padx=10, pady=10)

root.mainloop()
