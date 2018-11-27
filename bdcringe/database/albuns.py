from psycopg2 import DatabaseError
from bdcringe.database import Database


def search(nome):
    sql = "SELECT * FROM album WHERE nome like %%s%"
    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, ))
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


def update(antigo, novo):
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
