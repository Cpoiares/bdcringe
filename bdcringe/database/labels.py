from psycopg2 import DatabaseError
from bdcringe.database import Database


def exists_label(label_name):
    sql = """SELECT * FROM editora WHERE nome like %s"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (label_name,))
    except DatabaseError as error:
        return False
    else:
        return True


def insert_new(label_name):
    sql = """INSERT INTO editora(nome) VALUES(%s)"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (label_name,))
        conn.commit()
    except DatabaseError as error:
        raise DatabaseError(error)
    else:
        return False

