import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk

class TranslatorApp:
    def __init__(self, master, translate_callback, reset_callback):
        self.master = master
        self.translate_callback = translate_callback
        self.reset_callback = reset_callback

        self.master.title("Translation and Text-to-Speech App")
        self.master.geometry("450x500")
        self.master.configure(bg="#E8F5E9")  # Light green background color

        # Define a font for the app
        self.app_font = font.Font(family="Helvetica", size=12)

        # Create a frame for better organization
        self.frame = ttk.Frame(self.master, padding="20", relief=tk.RAISED, borderwidth=2)
        self.frame.pack(pady=20)

        # Create a title label
        self.title_label = ttk.Label(self.frame, text="Translation App", font=("Helvetica", 16, "bold"), foreground="#388E3C")
        self.title_label.pack(pady=10)

        # Create UI components
        self.text_label = ttk.Label(self.frame, text="Enter text to translate:", font=self.app_font)
        self.text_label.pack(pady=5)

        self.text_entry = tk.Text(self.frame, height=5, width=40, font=self.app_font, bd=2, relief=tk.SUNKEN)
        self.text_entry.pack(pady=5)

        self.language_label = ttk.Label(self.frame, text="Select target language:", font=self.app_font)
        self.language_label.pack(pady=5)

        # Add a ComboBox for language selection
        self.language_options = {
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Italian": "it",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko",
            "Russian": "ru",
            "Portuguese": "pt",
            "Hindi": "hi"
        }
        self.language_combobox = ttk.Combobox(self.frame, values=list(self.language_options.keys()), state="readonly")
        self.language_combobox.set("Select a language")  # Default text
        self.language_combobox.pack(pady=5)

        # Add some spacing between buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)

        self.translate_button = ttk.Button(button_frame, text="Translate", command=self.translate_text)
        self.translate_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_text)
        self.reset_button.pack(side=tk.LEFT)

        self.result_label = ttk.Label(self.frame, text="", wraplength=350, font=self.app_font, foreground="#388E3C")
        self.result_label.pack(pady=10)

    def translate_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        selected_language = self.language_combobox.get()

        if text and selected_language != "Select a language":
            target_language = self.language_options[selected_language]
            try:
                translated_text = self.translate_callback(text, target_language)
                self.result_label.config(text=f"Translated text: {translated_text}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please enter both text and select a target language.")

    def reset_text(self):
        self.text_entry.delete("1.0", tk.END)
        self.language_combobox.set("Select a language")
        self.result_label.config(text="")
        self.reset_callback()
