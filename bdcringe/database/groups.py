from psycopg2 import DatabaseError
from bdcringe.database import Database


def exists_group(group_name):
    sql = "SELECT * FROM grupo_musical WHERE nome like %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (group_name,))
    except DatabaseError as error:
        return False
    else:
        return True


def insert_new(name, date_begin, date_end):
    sql = "INSERT INTO grupo_musical(nome, inicio, fim) VALUES(%s, %s, %s)"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (name, date_begin, date_end))
        conn.commit()
    except DatabaseError as error:
        raise DatabaseError(error)
    else:
        return 'Success'


def add_artist(artist_name, group_name):
    sql = """
    INSERT
    INTO
        artista_grupo_musical
        (artista_id, grupo_musical_nome)
        SELECT
            a.id,
            g.nome 
        FROM
            artista a,
            grupo_musical g
        WHERE
            a.nome like %s and
            g.nome like %s
    """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (artist_name, group_name))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True
