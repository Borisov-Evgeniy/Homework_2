import sqlite3
import time

class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_objects(self, table):
        sql = f"SELECT * FROM {table}"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except IOError:
            print('Ошибка чтения базы данных')
        return []

    def add_post(self, title, text):
        tm = str(time.time())
        sql = 'INSERT INTO posts (title, text, time) VALUES (?, ?, ?)'
        try:
            self.__cur.execute(sql, (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавление статьи в базу данных' + str(e))
            return False
        return True
