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

def insert_artist(artist_name, artist_db):
    sql = """INSERT INTO artista(nome, data_nascimento) values(%s, %s);"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_name, artist_db))
        conn.commit()
    except DatabaseError as error:
        raise DatabaseError(error)
    else:
        pass

def exists_artist(artist_name):
    sql = """SELECT * FROM artista WHERE nome like %s"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_name,))
    except DatabaseError as error:
        return False
    else:
        return True


def get_songs(artist_name):
    sql = """SELECT nome, data, historia 
            FROM 
            musica, musica_artista 
            WHERE 
            artista_id = (SELECT id FROM artista WHERE nome like %s) 
            and 
            musica_id = id"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_name,))
        info = cur.fetchall()
    except DatabaseError as error:
        raise DatabaseError(error)
        return None
    else:
        return info