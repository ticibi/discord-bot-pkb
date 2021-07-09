import sqlite3
from datetime import datetime


DATABASE = './database/pkb.db'
BUILD = './database/build.sql'

def with_cursor(func):
    def inner(*args, **kwargs):
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            return func(cur, *args, **kwargs)
            con.commit()
    return inner

@with_cursor
def execute(cursor, command, *values):
    cursor.execute(command, tuple(values))

@with_cursor
def one(cursor, command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchone()

@with_cursor
def all(cursor, command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchall()

@with_cursor
def column(cursor, command, *values):
    cursor.execute(command, tuple(values))
    return [item[0] for item in cursor.fetchall()]

@with_cursor
def query(cursor, command, *values):
    cursor.execute(command, tuple(values))
    if (result := cursor.fetchone()) is not None:
        return result[0]

@with_cursor
def scriptexec(cursor, path):
    with open(path, "r", encoding="utf-8") as script:
        cursor.executescript(script.read())

def build_database():
    try:
        scriptexec(BUILD)
        print('successfully built database')
    except Exception as e:
        print('failed to build database', e)

def insert_all(member):
    query(
        'INSERT OR IGNORE INTO members (Id, DateJoined) VALUES (?,?)',
        member.id,
        datetime.utcnow(),
    )
    query(
        'INSERT OR IGNORE INTO economy (Id) VALUES (?)',
        member.id,
    )
    query(
        'INSERT OR IGNORE INTO daily (Id) VALUES (?)',
        member.id,
    )
    query(
        'INSERT OR IGNORE INTO lottery (Id) VALUES (?)',
        member.id,
    )
    query(
        'INSERT OR IGNORE INTO voting (Id) VALUES (?)',
        member.id,
    )
    query(
        'INSERT OR IGNORE INTO metrics (Id) VALUES (?)',
        member.id,
    )
    query(
        'INSERT OR IGNORE INTO badges (Id) VALUES (?)',
        member.id,
    )

def delete_all(member):
    query(
        'DELETE FROM members WHERE Id = ?',
        member.id,
    )
    query(
        'DELETE FROM economy WHERE Id = ?',
        member.id,
    )
    query(
        'DELETE FROM daily WHERE Id = ?',
        member.id,
    )
    query(
        'DELETE FROM lottery WHERE Id = ?',
        member.id,
    )
    query(
        'DELETE FROM voting WHERE Id = ?',
        member.id,
    )
    query(
        'DELETE FROM metrics WHERE Id = ?',
        member.id,
    )
    query(
        'DELETE FROM badges WHERE Id = ?',
        member.id,
    )

def check_exists(id):
    data = one(
        'SELECT Points FROM members WHERE Id = ?',
        id,
    )
    return True if data else False
