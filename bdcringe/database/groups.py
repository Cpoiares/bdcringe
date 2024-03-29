from psycopg2 import DatabaseError
from bdcringe.database import Database

# nome      (varchar) PK
# inicio    (date)
# fim       (date)


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


def search(nome):
    sql = "SELECT * FROM grupo_musical WHERE nome LIKE %(like)s ESCAPE '='"
    value = []
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (dict(like='%'+nome+'%')))
        value = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return value


def members(nome):
    sql = """
    SELECT
        *
    FROM
        artista a,
        artista_grupo_musical agm     
    WHERE
        a.id = agm.artista_id ands
        agm.grupo_musical_nome like %s
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


def insert(name, date_begin, date_end = None):
    sql = """
    INSERT
    INTO
        grupo_musical
        (nome, inicio, fim)
    VALUES
        (%s, %s, %s)
    """

    if date_end == '0':
        date_end = None

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (name, date_begin, date_end))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def add_show(address, date, group_name):
    sql = """INSERT INTO concerto(data, morada, grupo_musical_nome) VALUES(%s,%s,%s)"""
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (date, address, group_name))
        conn.commit()
        return True
    except DatabaseError as error:
        print(error)
        return False


def list_shows(group_name):
    sql = "SELECT data, morada FROM concerto WHERE concerto.grupo_musical_nome like %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (group_name,))
        values = cur.fetchall()
        return values
    except DatabaseError as error:
        print(error)


def get_all():
    sql = "SELECT * FROM grupo_musical"
    values = []

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql)
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


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
    print(get_all())
