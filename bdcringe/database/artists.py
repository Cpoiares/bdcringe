from psycopg2 import DatabaseError
from bdcringe.database import Database


def search(nome):
    #FIXME: OLHA NAO SEI ESTA MERAD NAO QUER DAR COM %s
    sql = "SELECT * FROM artista where nome like '%" + nome + "%'"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        # cur.execute(sql, (nome, ))
        cur.execute(sql)
        values = cur.fetchall()
        return values

    except DatabaseError as error:
        print(error)

    return None


def insert(nome, data_nascimento):
    sql = "INSERT INTO artista(nome, data_nascimento) values (%s, %s)"

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql, (nome, data_nascimento))
        conn.commit()
    except DatabaseError as error:
        print(error)
        return False

    return True


def get_all():
    sql = "SELECT * from artista"
    values = None

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql)
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


if __name__ == '__main__':
    test = get_all()
    print(test)

