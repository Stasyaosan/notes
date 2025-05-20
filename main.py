import tkinter as tk
from db import DB
from config import TITLE, WINDOWS
from datetime import datetime
from classes.widgets import Widgets


class NoteApp(Widgets):
    def __init__(self, root):
        self.db = DB()
        self.root = root
        self.root.title(TITLE)
        self.root.geometry(WINDOWS)
        self.create_widgets()
        self.load_notes()

    def load_notes(self):
        for item in self.notes_list.get_children():
            self.notes_list.delete(item)

        notes = self.db.select_notes()
        for id, title, created_at in notes:
            self.notes_list.insert('', tk.END, values=(title, created_at), iid=id)

    def save_button_(self):
        pass

    def on_note_select(self, event):
        pass

    def add_note(self):
        pass

    def delete_note(self):
        pass


a = tk.Tk()
note = NoteApp(a)
a.mainloop()
