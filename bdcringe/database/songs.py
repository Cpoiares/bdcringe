from psycopg2 import DatabaseError
from bdcringe.database import Database


def search_name(music_name):
    sql_music_info = """select m.nome, m.data, m.historia, m.genero, a.nome, a.data_nascimento
                        from artista a, musica_artista ma, musica m
                        where a.id = ma.artista_id and m.id = ma.musica_id and m.nome like 'snoop' """
    values = None
    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql_music_info, (music_name, ))

    except DatabaseError as error:
        print(error)
    else:
        values = cur.fetchall()
        return values

def insert_new(name, date, history, genre, album, artist):
    sql_new_music = """INSERT INTO musica(nome, data, historia, genero, album_nome) VALUES('%s', '%s', '%s', '%s', '%s')"""
    sql = """INSERT INTO musica_artista(artista_id, musica_id) SELECT a.id, m.id FROM artista a, musica m WHERE a.nome like '%s' and m.nome like '%s'"""

    try:
        conn = Database.connect()
        cur = conn.cursor()
        cur.execute(sql_new_music, (name, date, history, genre, album))
        cur.execute(sql, (name, artist))
    except DatabaseError as error:
        print(error)
        return False
    else:
        return True

if __name__ == '__main__':
    search_name('snoop')
