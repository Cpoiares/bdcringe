from psycopg2 import DatabaseError
from bdcringe.database import Database


def search_name(nome):
    sql = "SELECT * FROM artista where nome like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        values = cur.fetchone()
        return values

    except DatabaseError as error:
        print(error)

    return None
