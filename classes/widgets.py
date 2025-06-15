import tkinter as tk
from tkinter import ttk

class Widgets:

    def create_widgets(self):
        self.menu_bar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menu_bar)
        self.file_menu.add_command(label='Настройка MySQL', command=self.show_mysql_settings)
        self.file_menu.add_command(label='Экспорт в MySQL', command=self.export_to_mysql)
        self.file_menu.add_command(label='Импорт в MySQL', command=self.import_to_mysql)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Выход', command=self.root.quit)

        self.menu_bar.add_cascade(label='Настройки', menu=self.file_menu)

        self.root.config(menu=self.menu_bar)



        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.add_button = tk.Button(self.list_frame, text='Добавить заметку', command=self.add_note)
        self.add_button.pack(fill=tk.X, pady=5)

        self.delete_button = tk.Button(self.list_frame, text='Удалить заметку', command=self.delete_note,
                                       state=tk.DISABLED)
        self.delete_button.pack(fill=tk.X, pady=5)

        self.notes_list = ttk.Treeview(
            self.list_frame,
            columns=('title', 'created'),
            show='headings'
        )
        self.notes_list.heading('title', text='Заголовок')
        self.notes_list.heading('created', text='Создано')
        self.notes_list.column('title', width=150)
        self.notes_list.column('created', width=100)
        self.notes_list.pack(fill=tk.BOTH, expand=True)

        self.notes_list.bind('<<TreeviewSelect>>', self.on_note_select)

        self.edit_frame = tk.Frame(self.root)
        self.edit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.title_label = tk.Label(self.edit_frame, text='Заголовок:')
        self.title_label.pack(fill=tk.X, pady=5)

        self.title_entry = tk.Entry(self.edit_frame)
        self.title_entry.pack(fill=tk.X, pady=5)

        self.content_label = tk.Label(self.edit_frame, text='Описание: ')
        self.content_label.pack()

        self.content_text = tk.Text(self.edit_frame)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=5)

        self.save_button = tk.Button(
            self.edit_frame,
            text='Сохранить',
            command=self.save_button_,
            state=tk.DISABLED
        )
        self.save_button.pack(fill=tk.X, pady=5)

        self.info_label = tk.Label(self.edit_frame, text='')
        self.info_label.pack(fill=tk.X)