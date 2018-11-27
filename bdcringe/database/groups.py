from psycopg2 import DatabaseError
from bdcringe.database import Database


def exists(nome):
    sql = "SELECT * FROM grupo_musical WHERE nome like %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome,))
        values = cur.fetchall()
        return len(values) != 0
    except DatabaseError as error:
        print(error)
        return False


def members(nome):
    sql = """
    SELECT
        *
    FROM
        artista a,
        artista_grupo_musical agm     
    WHERE
        agm.grupo_musical_nome like %s and
        a.id = agm.artista_id
    """

    values = None

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


def insert(name, date_begin, date_end):
    sql = """
    INSERT
    INTO
        grupo_musical
        (nome, inicio, fim)
    VALUES
        (%s, %s, %s)
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (name, date_begin, date_end))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def add_artist_id(artist_id, group_name):
    sql = """
    INSERT
    INTO
        artista_grupo_musical
        (artista_id, grupo_musical_nome)
        SELECT
            %s,
            nome
        FROM
            grupo_musical
        WHERE
            nome like %s
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (group_name, artist_id))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


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


if __name__ == '__main__':
    print(insert("Jessica Password Megane", "2010-10-01", "2010-01-02"))
    print(add_artist("yaboi", "Jessica Password Megane"))
    print(exists("Jessica Password Megane"))
    print(members("Jessica Password Megane"))
