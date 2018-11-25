from psycopg2 import DatabaseError
from bdcringe.database import Database


def search_album(album_name):
    sql = """SELECT * FROM album WHERE nome like %s"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql,(album_name,))

    except DatabaseError as error:
        raise DatabaseError(error)
    else:
        values = cur.fetchall()
        return values
    pass


def exists_album(album_name):
    sql = """SELECT * FROM album WHERE nome like %s"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql,(album_name,))
    except DatabaseError as error:
        raise DatabaseError(error)
    else:
        values = cur.fetchall()
        return values
    pass
