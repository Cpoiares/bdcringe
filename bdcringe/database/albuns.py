from psycopg2 import DatabaseError
from bdcringe.database import Database


def search(nome):
    sql = "SELECT * FROM album WHERE nome like %%s%"
    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        values = cur.fetchall()

    except DatabaseError as error:
        print(error)

    return values


def exists(nome):
    sql = "SELECT * FROM album WHERE nome like %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome,))
        values = cur.fetchall()
        return values is not None

    except DatabaseError as error:
        print(error)
        return False


def update(antigo, novo):
    sql = "UPDATE album SET nome = %s WHERE nome like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (antigo, novo))
        cur.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


def delete(nome):
    sql = "DELETE from album where nome like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        cur.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True

