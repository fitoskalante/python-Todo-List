import os
import sqlite3
from datetime import datetime

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()


def setupTodos():
    sql = """
    CREATE TABLE IF NOT EXISTS todos(
    Id INTEGER PRIMARY KEY,
    Task TEXT NOT NULL,
    Due_Date INTEGER,
    User_Id INTEGER,
    Email TEXT NOT NULL,
    Status TEXT NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()


def setupUsers():
    sql = """
    CREATE TABLE IF NOT EXISTS users(
    User_Id INTEGER PRIMARY KEY,
    Email TEXT NOT NULL,
    Username TEXT NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()


setupTodos()
setupUsers()
