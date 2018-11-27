from psycopg2 import DatabaseError
from bdcringe.database import Database


def search(nome):
    # https://stackoverflow.com/questions/2106207/escape-sql-like-value-for-postgres-with-psycopg2

    sql = "SELECT * FROM artista where nome LIKE %(like)s ESCAPE '='"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (dict(like='%'+nome+'%')))
        values = cur.fetchall()
        return values

    except DatabaseError as error:
        print(error)
        return None


def insert(nome, data_nascimento):
    sql = "INSERT INTO artista(nome, data_nascimento) values (%s, %s)"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, data_nascimento))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def exists(artist_name):
    sql = "SELECT * FROM artista WHERE nome like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_name, ))
        values = cur.fetchall()
        return len(values) != 0

    except DatabaseError:
        return False


def get_songs(artist_name):
    sql = """SELECT nome, data, historia 
            FROM 
            musica, musica_artista 
            WHERE 
            artista_id = (SELECT id FROM artista WHERE nome like '%s') 
            and 
            musica_id = id"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_name,))
        info = cur.fetchall()
        return info
    except DatabaseError as error:
        print(error)
        return None


if __name__ == '__main__':
    res = search('boi')
    for value in res:
        print(value)
