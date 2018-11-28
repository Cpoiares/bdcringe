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


def add_song(id_playlist, musica_id):
    sql = """
    INSERT
    INTO
        playlist_musica(playlist_id, musica_id)
        SELECT
            %s,
            id
        FROM
            musica m
        WHERE
            m.id = %s
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (id_playlist, musica_id))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


def remove_song(playlist_id, musica_id):
    sql = """
    DELETE 
    FROM 
    playlist_musica
    WHERE 
    musica_id = (
    SELECT 
    id 
    FROM 
    musica
    WHERE 
    id = %s
    ) 
    and 
    playlist_id = %s
    """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (musica_id, playlist_id))
        conn.commit()
        return True
    except DatabaseError as error:
        print(error)
        return False


def list_songs(playlist_id):
    sql = """
    SELECT
    *
    FROM
    musica m, playlist_musica pm, playlist p
    WHERE
    pm.musica_id = m.id and
    pm.playlist_id = p.id and
    p.id = %s;
    """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (playlist_id,))
        values = cur.fetchall()
        return values

    except DatabaseError as error:
        print(error)
        return None


def get_all(username):
    sql = "SELECT * FROM playlist WHERE utilizador_username like %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (username,))
        values = cur.fetchall()
        return values
    except DatabaseError as error:
        print(error)
        return None


def get_status(id_playlist):
    sql = "SELECT privada FROM playlist WHERE id = %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (id_playlist,))
        value = cur.fetchall()
        return value
    except DatabaseError as error:
        print(error)


def set_status(playlist_id, bool):
    sql = "UPDATE playlist SET privada = %s WHERE id = %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (bool, playlist_id))
        return True
    except DatabaseError as error:
        print(error)
        return False


