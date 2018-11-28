import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.songs as songs
import bdcringe.database.labels as labels
import bdcringe.database.albuns as albuns

import bdcringe.menus.groups as groups

from psycopg2 import DatabaseError


def login():
    username = input("Username: ")
    password = input("Password: ")
    return user.login(username, password)


def register():
    username = input("Username: ")
    password = input("Password: ")
    return user.register(username, password)


def list_labels():
    values = labels.get_all()

    for label in values:
        print(label)


def insert_label():
    nome = input("Nome da editora: ")
    if labels.insert(nome):
        print("Sucess")
    else:
        print("Erro.")


def search_artist():
    print("1. Procurar Artista por nome: ")
    option = input("> ")

    if option == '1':
        nome = input("Nome: ")
        artistas = artists.search(nome)

        for i, artista in enumerate(artistas):
            print("{0}. [{data}] : {nome}".format(i, nome=artista[1], data=artista[2]))

        print("Mostrar detalhes de algum artista?")
        option = input("> ")


def insert_artist():
    print("Inserir novo artista...")
    name = input("Nome do artista a criar: ")
    data = input("Data de nascimento do artista (aaa-mm-dd): ")
    try:
        artists.insert(name, data)
    except DatabaseError as error:
        print(error)
    else:
        print("Success.\nBack to main menu.")
        main_menu()


def list_artist_songs():
    artista = input("Introduza o nome do artista a procurar:\n> ")

    while not artists.exists(artista):
        artista = input("Introduza o nome do artista a procurar:\n> ")

    try:
        print(artists.get_songs(artista))
    except DatabaseError as error:
        print(error)


def insert_song():
    try:
        print("INSERIR NOVA MUSICA\nIntroduza o nome da musica:\n")
        nome = input("> ")
        data = input("Data da musica:\n> ")
        historia = input("Breve história da música:\n> ")
        genre = input("Genero da musica:\n> ")

        album = input("Nome do album:\n> ")

        while not albuns.exists(album):
            album = input("Nome do album:\n> ")

        artista = input("Nome do artista:\n> ")
        while not artists.exists(artista):
            artista = input("Nome do artista não encontrado!\nNome do artista:\n> ")

        songs.insert(nome, data, historia, genre, album, artista)

    except DatabaseError as error:
        print(error)
    else:
        print('Success')
        main_menu()


def main_menu():
    options = {
        0: search_artist,
        1: insert_artist,
        2: groups.menu,
        3: insert_song,
        4: insert_label,
        5: list_artist_songs,
        6: list_labels,
        7: insert_label
    }

    option = 0
    while option != len(options):
        print(chr(27) + "[2J") # clear
        print("0. Procurar artista")
        print("1. Inserir artista")
        print("2. Gestão de grupos")
        print("3. Inserir musica")
        print("4. Inserir editora")
        print("5. Listar musicas de um artista")
        print("6. Listar editoras")
        print("7. Inserir editora")
        print("8. Sair")
        option = int(input("> "))
        if (option >= 0) and (option < len(options) + 1):
            if option != len(options):
                options[option]()


if __name__ == '__main__':

    online = False
    leave = False

    while not online and not leave:
        print(chr(27) + "[2J") # clear
        print("1 - Register")
        print("2 - Login")
        print("3 - Leave")
        option = input("> ")

        if option == '1':
            online = register()
        elif option == '2':
            online = login()
        elif option == '3':
            leave = True

        if leave:
            print("Adeuxito manito")
            exit(0)

        if not online:
            print("Tente outra vez.")
        else:
            main_menu()
            online = False
            leave = False
