from psycopg2 import DatabaseError
from bdcringe.database import Database


def insert(nome):
    sql = "INSERT INTO editora(nome) values(%s)"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        cur.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def search(nome):
    sql = "SELECT * FROM editora WHERE nome like '%%s%'"
    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


def update(antigo, novo):
    sql = "UPDATE editora SET nome = %s WHERE nome like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (novo, antigo))
        cur.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def delete(nome):
    sql = "DELETE FROM editora WHERE nome LIKE %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        cur.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True
