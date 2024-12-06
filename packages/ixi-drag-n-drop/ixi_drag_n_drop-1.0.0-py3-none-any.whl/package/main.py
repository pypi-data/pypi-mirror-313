import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog as fd
import PIL.Image
import PIL.ImageTk
import webbrowser
import os


class FileDialog(TkinterDnD.Tk):

    def __init__(self):
        super().__init__()
        self.title("File Dialog")

        width = 1000
        height = 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.file_contents = tk.Frame(self)
        self.label = tk.Label(self.file_contents, text="Drag something here")
        self.label.pack(pady=5)
        self.file_contents.pack(fill=tk.BOTH, expand=True)
        self.file_contents.drop_target_register(DND_FILES)
        self.file_contents.dnd_bind('<<Drop>>', self.handle_drop)


    def filehandler(self):
        filetypes = (
            ('All files', '*.*'),
            ('Text files', '*.txt *.log *.csv *.ini'),
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'),
            ('PDF files', '*.pdf')
        )

        filepath = fd.askopenfilename(
            parent=self, title="Open file", filetypes=filetypes
        )

        if filepath:
            self.display_file(filepath)

    def handle_drop(self, event):
        filepaths = event.data.split('\n')
        for filepath in filepaths:
            if os.path.exists(filepath):
                self.display_file(filepath)
            else:
                tk.messagebox.showerror("Error", f"File not found: {filepath}")


    def clear_file_contents(self):
        for widget in self.file_contents.winfo_children():
            widget.destroy()

    def display_file(self, filepath):
        self.clear_file_contents()
        filename = os.path.basename(filepath)
        label = tk.Label(self.file_contents, text=f"File: {filename}")
        label.pack(pady=5)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                text_widget = tk.Text(self.file_contents, wrap=tk.WORD)
                text_widget.pack(fill=tk.BOTH, expand=True)
                text_widget.insert(tk.END, text)
        except UnicodeDecodeError:
            try:
                image = PIL.Image.open(filepath)
                photo = PIL.ImageTk.PhotoImage(image)
                label = tk.Label(self.file_contents, image=photo)
                label.image = photo
                label.pack(fill=tk.BOTH, expand=True)
            except Exception:
                try:
                    webbrowser.open(filepath)
                except Exception as e:
                    tk.messagebox.showerror("Error", f"Could not display this file type: {e}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    file_dialog = FileDialog()
    file_dialog.mainloop()