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
        values = cur.fetchall()
    except DatabaseError as error:
        print(error)

    return values


if __name__ == '__main__':
    search_name('snoop')
