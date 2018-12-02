from psycopg2 import DatabaseError
from bdcringe.database import Database


def search(music_name):
    sql = """SELECT * FROM musica WHERE nome like %(like)s ESCAPE '='"""
    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (dict(like='%'+music_name+'%')))
        values = cur.fetchall()

    except DatabaseError as error:
        print(error)

    return values

# not even used
def search_name(music_name):
    sql_music_info = """
        select
            *
        from
            artista a,
            musica_artista ma,
            musica m
        where
            a.id = ma.artista_id and
            m.id = ma.musica_id and
            m.nome like %(like)s ESCAPE '='
    """

    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql_music_info, (dict(like='%'+music_name+'%')))
        values = cur.fetchall()

    except DatabaseError as error:
        print(error)

    return values


def insert_song_artist(artista_id, musica_id):
    sql = """INSERT
          INTO 
          musica_artista(artista_id, musica_id)
          VALUES(%s, %s)
        """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artista_id,musica_id))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


'''def insert(nome, data, historia, genero, album, artist):
    sql_musica = """
        INSERT 
        INTO
            musica
            (nome, data, historia, genero, album_nome) 
        VALUES
            ('%s', '%s', '%s', '%s', '%s')
    """
    sql_artista = """
        INSERT
        INTO
            musica_artista
            (artista_id, musica_id)
            SELECT
                a.id,
                m.id
            FROM
                artista a,
                musica m
            WHERE
                m.nome like '%s' and
                a.nome like '%s'
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql_musica, (nome, data, historia, genero, album))
        cur.execute(sql_artista, (nome, artist))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True
'''


def insert_song(nome, data, historia, genero, album):
    sql_musica = """
        INSERT 
        INTO
            musica
            (nome, data, historia, genero, album_nome) 
        VALUES
            (%s, %s, %s, %s, %s)
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql_musica, (nome, data, historia, genero, album))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def letra(musica_id, compositor, texto):
    sql = """
        insert
        into
            letra
            (texto, musica_id, compositor_artista_id) 
        values
            (%s, %s, %s)
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (texto, musica_id, compositor))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


def get_letra(musica_id):
    sql = """
        SELECT 
        texto, compositor_artista_id
        FROM
        letra
        WHERE musica_id = %s 
        """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (musica_id, ))
        values = cur.fetchall()
    except Database as error:
        raise DatabaseError(error)
    return values


def get_all():
    sql = "SELECT * FROM musica"
    values = []

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql)
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


if __name__ == '__main__':
    search_name('snoop')
