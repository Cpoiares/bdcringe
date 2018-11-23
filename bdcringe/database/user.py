from psycopg2 import DatabaseError
from bdcringe.database import Database


def login(username, password):
    sql = "SELECT * FROM utilizador where username like %s and password like %s "

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
