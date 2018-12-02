import bdcringe.database.songs as songs
import bdcringe.database.artists as artists
import bdcringe.database.albums as albums
import bdcringe.database.composer as composer
from psycopg2 import DatabaseError



def menu():
    print("Gestão de Músicas")

    options = [
        (list_all, "Listar músicas"),
        (search, "Procurar música"),
        (insert_song, "Inserir música")
    ]

    op = 0
    while op != len(options):
        print(chr(27) + "[2J")  # clear
        for i, option in enumerate(options):
            print("{0}. {2}".format(i, *option))

        print(str(len(options)) + ". Sair")

        op = int(input("> "))
        if (op >= 0) and (op < len(options)):
            options[op][0]()


def list_all():
    print("Listar todas as músicas.")

    lista = songs.get_all()

    for i, song in enumerate(lista):
        print("{3}. '{0}' pelos {2} -> {1}".format(song[1], song[2], song[7], i))


def search():
    print("Procurar musica.")
    nome = input("Nome: ")

    musicas = songs.search(nome)

    for i, song in enumerate(musicas):
        print("{2}. '{0}' pelos {1} ".format(song[1], song[7], i))
    print("{}. Sair".format(len(musicas)))

    option = int(input("Selecionar música: "))
    if option == len(musicas):
        return

    if (option >= 0) and (option < len(musicas)):
        id_musica = musicas[option][0]
        op = '0'
        while op != '3':
            print("0. Adicionar Letra.")
            print("1. Adicionar artista")
            print("2. Ver Letra.")
            print("3. Sair.")
            op = input("> ")

            if op == '0':
                insert_lyrics(id_musica)
            if op == '1':
                insert_artist(id_musica)
            if op == '2':
                get_lyrics(id_musica)


def insert_lyrics(id_musica):

    print(repr("Introduza a letra: (translineações devem ser feitas com \n)"))
    letra = input("> ")
    artistas = artists.get_all()

    print("Artistas: ")
    for i, artista in enumerate(artistas):
        print("{1}. {0}".format(artista[1], i))
    print("{}. Sair".format(len(artistas)))

    op = int(input("Selecionar compositor da letra: "))

    if op == len(artistas):
        return

    if (op >= 0) and (op < len(artistas)):
        artista_id = artistas[op][0]
        # if not composer.exists(artist_id):
        # ^nao funcimina por isso mando o erro para o utilizador, nao ha mal se inserir um ja inserido
        composer.insert(artista_id)
        if songs.letra(id_musica, artista_id, letra):
            print("Sucesso")
        else:
            print("Error")


def insert_artist(id_musica):
    lista = artists.get_all()
    print("Artistas: ")
    for i, artista in enumerate(lista):
        print("{1}. {0}".format(artista[1], i))
    print("{}. Sair".format(len(lista)))

    option = int(input("Selecionar compositor da musica: "))
    if option == len(lista):
        return
    if (option >= 0) and (option < len(lista)):
        artist_id = lista[option][0]
        if songs.insert_song_artist(artist_id, id_musica):
            print("Sucesso.")
        else:
            print("Erro.")


def get_lyrics(id_musica):

    try:
        letra = songs.get_letra(id_musica)
        texto = letra[0][0]
        artista_id = letra[0][1]
        artista = artists.search_id(artista_id)
        print("{0}\n -------- \nLetra escrita por: {1}".format(texto, artista[0][1]))
    except DatabaseError as error:
        print("Não tem letra.")


def insert_song():
    print("Inserir música.")
    name = input("Introduza o nome da música:\n> ")
    date = input("Introduza a data de criação (YYYY-MM-DD):\n> ")
    history = input("Introduza uam breve história da música:\n> ")
    genre = input("Introduza o género da música:\n> ")

    lista = albums.get_all()

    for i, album in enumerate(lista):
        print("{4}. {3} - {0}".format(*album, i))
    print("{}. Sair".format(len(lista)))

    option = int(input("Seleccionar album: "))

    if option == len(lista):
        return

    if (option >= 0) and (option < len(lista)):
        album_name = lista[option][0]
        if songs.insert_song(name, date, history, genre, album_name):
            print("Sucesso.")
        else:
            print("Erro.")

