from psycopg2 import DatabaseError
from bdcringe.database import Database

def get_music(music_name):
    sql_music_info = "select m.nome, m.data, m.historia, m.genero, a.nome, a.data_nascimento " \
                   "from artista a, musica_artista ma, musica m " \
                   "where a.id = ma.artista_id and m.id = ma.musica_id and m.nome like 'snoop' "
    try:
        conn = Database.connect()
        cur = conn.cursor()
        if music_name is not None:
            cur.execute(sql_music_info, (music_name,))
            print(cur.fetchone())
    except DatabaseError as error:
        print(str(error))
    except KeyboardInterrupt as error:
        print("Cancelling queue")
    else:
        pass


if __name__ == '__main__':
    get_music('snoop')
