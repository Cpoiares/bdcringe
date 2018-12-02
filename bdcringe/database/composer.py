from psycopg2 import DatabaseError
from bdcringe.database import Database


def exists(artist_id):
    sql = """SELECT 
            *
            FROM
            compositor
            WHERE
            artista_id = %s
            """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_id,))
    except Database as error:
        print(error)
        return False

    return True


def insert(artist_id):
    sql = """INSERT INTO
            compositor(artista_id)
            VALUES
            (%s)
            """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_id,))
        conn.commit()

    except DatabaseError as error:
        print(error)
        return False

    return True


if __name__ == '__main__':
    exists(10)

