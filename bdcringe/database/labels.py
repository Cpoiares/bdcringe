from psycopg2 import DatabaseError
from bdcringe.database import Database


def insert(nome):
    sql = "INSERT INTO editora(nome) values(%s)"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def search(nome):
    sql = "SELECT * FROM editora WHERE nome LIKE %(like)s ESCAPE '='"
    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (dict(like='%'+nome+'%')))
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


def exists(nome):
    sql = "SELECT * FROM editora WHERE nome like %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        values = cur.fetchall()
        return len(values) != 0

    except DatabaseError as error:
        print(error)
        return False


def update(antigo, novo):
    sql = "UPDATE editora SET nome = %s WHERE nome LIKE %s"

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


def get_all():
    sql = "SELECT * FROM editora"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    except DatabaseError as error:
        print(error)
        return False
