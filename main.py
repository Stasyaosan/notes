import tkinter as tk
from datetime import datetime
from tkinter.messagebox import showerror, askyesno

from classes.widgets import Widgets
from config import TITLE, WINDOWS
from db import DB


class NoteApp(Widgets):
    def __init__(self, root):
        self.db = DB()
        self.root = root
        self.root.title(TITLE)
        self.root.geometry(WINDOWS)
        self.create_widgets()
        self.load_notes()
        self.current_note_id = None

    def load_notes(self):
        for item in self.notes_list.get_children():
            self.notes_list.delete(item)

        notes = self.db.select_notes()
        for id, title, content, created_at, updated_at in notes:
            self.notes_list.insert('', tk.END, values=(title, created_at), iid=id)

    def save_button_(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', tk.END)

        if not title:
            showerror('Ошибка', 'Заголовок не может быть пустым')
            return
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.current_note_id:
            self.db.edit_notes(title, content, now, self.current_note_id)
        else:
            self.db.add_notes(title, content, now)
        self.load_notes()

    def on_note_select(self, event):
        selected = self.notes_list.selection()
        if selected:
            note_id = selected[0]
            id, title, content, created_at, updated_at = self.db.select_note_by_id(note_id)
            self.current_note_id = id

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)

            self.content_text.delete('1.0', tk.END)
            self.content_text.insert('1.0', content)

            self.info_label.config(text=f'Создано: {created_at} | Обновлено: {updated_at}')
            self.delete_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)

    def add_note(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)
        self.info_label.config(text='')

        self.title_entry.focus_set()

        self.save_button.config(state=tk.NORMAL)

        self.notes_list.selection_remove(self.notes_list.selection())

        self.delete_button.config(state=tk.DISABLED)

    def delete_note(self):
        if not self.current_note_id:
            return
        if askyesno('', 'Удалить заметку?'):
            self.db.delete_notes(self.current_note_id)
            self.load_notes()

    def show_mysql_settings(self):
        mysql_window = tk.Toplevel(self.root)
        mysql_window.title('Настройка Mysql')
        mysql_window.geometry('400x300')
        tk.Label(mysql_window, text='Host').grid(row=0, column=0, padx=5, pady=5)
        host_entry = tk.Entry(mysql_window)
        host_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(mysql_window, text='User').grid(row=1, column=0, padx=5, pady=5)
        user_entry = tk.Entry(mysql_window)
        user_entry.grid(row=1, column=1, padx=5, pady=5)

    def export_to_mysql(self):
        pass


a = tk.Tk()
note = NoteApp(a)
a.mainloop()
