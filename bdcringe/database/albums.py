from psycopg2 import DatabaseError
from bdcringe.database import Database


def search(nome):
    sql = "SELECT * FROM album WHERE nome like %(like)s ESCAPE '='"
    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (dict(like='%'+nome+'%')))
        values = cur.fetchall()

    except DatabaseError as error:
        print(error)

    return values


def exists(nome):
    sql = "SELECT * FROM album WHERE nome like %s"
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome,))
        values = cur.fetchall()
        return len(values) != 0

    except DatabaseError as error:
        print(error)
        return False


def update_nome(antigo, novo):
    sql = "UPDATE album SET nome = %s WHERE nome like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (antigo, novo))
        cur.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


def delete(nome):
    sql = "DELETE from album where nome like %s"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        cur.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


def insert(nome, lancamento, grupo_musical, editora):
    sql = """
    INSERT 
    INTO
        album
        (nome, lancamento, editora_id, grupo_musical_nome)
        SELECT
            %s,
            %s,
            id,
            %s 
        FROM
            editora
        WHERE
            nome like %s
    """
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, lancamento, grupo_musical, editora))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def get_all():
    sql = "select * from album"
    values = []

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql)
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


def songs(nome):
    sql = """
        select
            *
        from
            musica
        where
            album_nome like %s
    """
    values = []

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


def review(nome, pontuacao, justificacao, username):
    sql = """
    insert
    into
        critica
        (album_nome, utilizador_username, pontuacao, justificacao)
    values
        (%s, %s, %s, %s)
    """

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, username, pontuacao, justificacao))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False
    return True


def reviews(nome):
    sql = """
    select
        pontuacao, justificacao, utilizador_username
    from
        critica
    where
        album_nome like %s
    """
    values = []
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values
