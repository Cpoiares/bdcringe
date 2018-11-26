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


def insert_new(name, date, group, label):
    sql = """INSERT INTO album(nome, lancamento, editora_id, grupo_musical_nome) SELECT %s, %s, id, %s FROM editora WHERE nome like %s"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (name, date, group, label))
        conn.commit()
    except DatabaseError as error:
        raise DatabaseError(error)
    else:
        return True


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
