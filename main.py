import customtkinter as ctk
import enchant

d = enchant.Dict("en_US")

# set ctk default colors
ctk.set_default_color_theme("green.json")

# create root window and set name
root = ctk.CTk()
root.title("Gramma Dictionary")
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


outputText = ctk.CTkTextbox(root, state="disabled", width=1000, height=500)
inputText = ctk.CTkTextbox(root, width=900, height=100)
sendButton = ctk.CTkButton(root, text="Process", command=process, width=100, height=50)

outputText.grid(row=0, column=0, columnspan=2, sticky="we")
inputText.grid(row=2, column=0, sticky="we", padx=10, pady=10)
sendButton.grid(row=2, column=1, sticky="e", padx=10, pady=10)

root.mainloop()
