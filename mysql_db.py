import json

import mysql.connector
from os.path import exists


class Mysql:

    def __init__(self, path):
        self.host = None
        self.user = None
        self.password = None
        self.db_name = None
        self.path = path
        if exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'host' in data and 'user' in data and 'password' in data and 'db_name' in data:
                self.host = data['host']
                self.user = data['user']
                self.password = data['password']
                self.db_name = data['db_name']

        self.connection = self.connect_to_mysql()
        self.create_table()

    def connect_to_mysql(self):
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
        if connection.is_connected():
            return connection
        return False

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
