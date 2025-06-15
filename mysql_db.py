import json

import mysql.connector
from os.path import exists
from db import DB


class Mysql:
    def __init__(self, path):
        self.host = None
        self.user = None
        self.password = None
        self.db_name = None
        self.path = path
        self.connection_flag = False

        if exists(path):

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'host' in data and 'user' in data and 'password' in data and 'db_name' in data and 'port' in data:
                self.host = data['host']
                self.user = data['user']
                self.password = data['password']
                self.db_name = data['db_name']
                self.port = data['port']

        self.connection = self.connect_to_mysql()

        self.create_table()

    def connect_to_mysql(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name,
                port=self.port
            )
            if connection.is_connected():
                return connection
            return False
        except:
            self.connection_flag = True

    def create_table(self):
        if exists(self.path):
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute('''
                create table if not exists notes(
                    id int auto_increment primary key,
                    title text not null,
                    content text not null,
                    created_at text not null,
                    updated_at text not null
                )
                ''')
                self.connection.commit()

    def add_notes(self):
        try:
            if self.connection_flag:
                return False
            notes = DB.select_notes_()
            cursor = self.connection.cursor()
            for note in notes:
                sql = 'insert into notes (title, content, created_at, updated_at) values (%s,%s,%s,%s)'
                r = (note[1], note[2], note[3], note[4])
                cursor.execute(sql, r)
                self.connection.commit()
            return True
        except:
            return False

    def import_notes(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('select * from notes')
            notes_mysql = cursor.fetchall()
            sqlite_db = DB()
            sqlite_db.delete_notes()
            for i in notes_mysql:
                sqlite_db.add_notes(i[1], i[2], i[3])
            return True
        except:
            return False

