from psycopg2 import DatabaseError
from bdcringe.database import Database


def login(username, password):
    sql = "SELECT username, editor FROM utilizador where username like %s and password like %s"
    value = None

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        value = cur.fetchone()

    except DatabaseError as error:
        print(error)

    return value


def register(username, password):
    sql = "INSERT INTO utilizador(username, password) values(%s, %s) RETURNING username, editor"
    value = None

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        value = cur.fetchone()
        conn.commit()
    except DatabaseError as error:
        print(error)

    return value


def get_all():
    sql = "SELECT username FROM utilizador"
    values = None

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql,())
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


def make_editor(username):
    sql = "UPDATE utilizador SET editor = true WHERE username like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username, ))
    except DatabaseError as error:
        print(error)
        return False

    return True


def find_user(username):
    sql = "SELECT username, editor FROM utilizador WHERE username LIKE %s and editor = false"
    values = []

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username,))
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values
