import tkinter as tk
from datetime import datetime
from tkinter.messagebox import showerror, askyesno, showinfo
import json

import mysql.connector

from classes.widgets import Widgets
from config import TITLE, WINDOWS
from db import DB
from mysql_db import Mysql


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

        try:
            with open('config_mysql.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}

        mysql_window.grab_set()
        mysql_window.transient(self.root)
        mysql_window.focus_set()

        tk.Label(mysql_window, text='Host').grid(row=0, column=0, padx=5, pady=5)
        self.host_entry = tk.Entry(mysql_window)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        self.host_entry.insert(0, data.get('host', ''))

        tk.Label(mysql_window, text='Port').grid(row=1, column=0, padx=5, pady=5)
        self.port_entry = tk.Entry(mysql_window)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
        self.port_entry.insert(0, '3306')
        self.port_entry.insert(0, data.get('port', ''))

        tk.Label(mysql_window, text='User').grid(row=2, column=0, padx=5, pady=5)
        self.user_entry = tk.Entry(mysql_window)
        self.user_entry.grid(row=2, column=1, padx=5, pady=5)
        self.user_entry.insert(0, data.get('user', ''))

        tk.Label(mysql_window, text='Password:').grid(row=3, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(mysql_window, show='*')
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)
        self.password_entry.insert(0, data.get('password', ''))

        tk.Label(mysql_window, text='DB_name:').grid(row=4, column=0, padx=5, pady=5)
        self.db_entry = tk.Entry(mysql_window, )
        self.db_entry.grid(row=4, column=1, padx=5, pady=5)
        self.db_entry.insert(0, data.get('db_name', ''))

        self.save_button = tk.Button(mysql_window, text='Сохранить', command=self.save_settings)
        self.save_button.grid(row=5, column=0, padx=5, pady=5)

        self.test_button = tk.Button(mysql_window, text='Тест подключения',
                                     command=self.test_mysql_connection)
        self.test_button.grid(row=5, column=1, padx=5, pady=5)

    def save_settings(self):
        date = {
            'host': self.host_entry.get(),
            'user': self.user_entry.get(),
            'password': self.password_entry.get(),
            'db_name': self.db_entry.get()
        }

        with open('config_mysql.json', 'w', encoding='utf-8') as f:
            json.dump(date, f, indent=4)

    def test_mysql_connection(self):
        try:
            connection = mysql.connector.connect(host=self.host_entry.get(), user=self.user_entry.get(),
                                                 password=self.password_entry.get(), db=self.db_entry.get(),
                                                 port=self.port_entry.get())
            if connection.is_connected():
                self.test_button.config(state=tk.DISABLED)
                showinfo('Success', 'Connection success')
                connection.close()
                return True
            else:
                showerror('Error', 'Error connection')
                return False
        except:
            showerror('Error', 'Error connection')
            return False

    def export_to_mysql(self):
        mysql = Mysql('config_mysql.json')
        self.get_all_notes()

    def get_all_notes(self):
        data = []

        for i in self.notes_list.get_children():
            values = self.notes_list.item(i, 'values')
            r = {
                'title': values[0],
                'created_at': values[1]
            }
            data.append(r)
        print(data)


a = tk.Tk()
note = NoteApp(a)
a.mainloop()
