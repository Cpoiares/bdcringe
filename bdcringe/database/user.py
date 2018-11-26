from psycopg2 import DatabaseError
from bdcringe.database import Database


def login(username, password):
    sql = "SELECT * FROM utilizador where username like %s and password like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        values = cur.fetchone()

        if values is None:
            return False
        else:
            return True
        # return values is not None

    except DatabaseError as error:
        print(error)
        return False


def register(username, password):
    sql = "INSERT INTO utilizador(username, password) values(%s, %s)"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def get_users():
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
    sql = "UPDATE utilizador SET editor = true WHERE username like '%s'"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username, ))
    except DatabaseError as error:
        print(error)
        return False

    return True


def find_user(username):
    sql = "SELECT username FROM utilizador WHERE username LIKE %s"
    user = None

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username,))
        user = cur.fetchone()
    except DatabaseError as error:
        print(error)

    return user
