import sqlite3
from config import DB_NAME


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        create table if not exists notes(
        id integer primary key autoincrement,
        title text not null,
        content text not null,
        created_at text not null,
        updated_at text not null
        )
        ''')
        self.conn.commit()

    def select_notes(self):
        self.cursor.execute('select * from notes order by updated_at desc')
        return self.cursor.fetchall()

    def select_note_by_id(self, id_note):
        self.cursor.execute('select * from notes where id = ?', (id_note,))
        return self.cursor.fetchone()

    def add_notes(self, title, content, now):
        self.cursor.execute('insert into notes (title, content, created_at, updated_at) values (?,?,?,?)',
                            (title, content, now, now))
        self.conn.commit()

    def edit_notes(self, title, content, now, id_note):
        self.cursor.execute('update notes set title = ?, content = ?, updated_at = ? where id = ?', (title, content, now, id_note))
        self.conn.commit()
