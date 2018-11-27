from psycopg2 import DatabaseError
from bdcringe.database import Database


def insert(nome, username):
    sql = """
    INSERT 
    INTO
        playlist
        (nome, utilizador_username)
    VALUES
        (%s, %s)
    """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, username))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def add_song(musica_id, playlist_id):
    sql = """
    insert
    into
        playlist
    values
        (%s, %s)
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (musica_id, playlist_id))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True
