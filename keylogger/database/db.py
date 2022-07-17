import sqlite3


class Database:

    @property
    def cursor(self):
        conn = sqlite3.connect('keylogger.db', isolation_level=None)
        return conn.cursor()


db = Database()
