import tkinter as tk
from PIL import Image, ImageTk

class VideoChatUI:
    def __init__(self, window, title):
        self.window = window
        self.window.title(title)

        self.label = tk.Label(window)
        self.label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky='nsew')

        self.chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.entry = tk.Entry(window)
        self.entry.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.send_button = tk.Button(window, text='보내기', command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky='se')

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=4)
        window.grid_columnconfigure(1, weight=1)

    def show_frame(self, frame):
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.label.config(image=photo)
        self.label.image = photo

    def send_message(self):
        message = self.entry.get()
        if message:
            self.entry.delete(0, 'end')
            self.on_send_message(message)
    def on_send_message(self, message):
        pass

    def receive_message(self, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + '\n')
        self.chat_text.config(state=tk.DISABLED)