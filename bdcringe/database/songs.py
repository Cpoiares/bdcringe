from psycopg2 import DatabaseError
from bdcringe.database import Database


def search_name(music_name):
    sql_music_info = """
        select
            m.nome,
            m.data,
            m.historia,
            m.genero,
            a.nome,
            a.data_nascimento
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


def insert(nome, data, historia, genero, album, artist):
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


def letra(musica, compositor, texto):
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
        cur.execute(sql, (texto, musica, compositor))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


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
