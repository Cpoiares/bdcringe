import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.songs as songs
import bdcringe.database.albuns as albuns
from psycopg2 import DatabaseError

global online


def login():
    global online

    username = input("Username: ")
    password = input("Password: ")

    if user.login(username, password):
        print("Logged in!")
        online = True
    else:
        print("sqn.")


def register():
    global online

    username = input("Username: ")
    password = input("Password: ")

    if user.register(username, password):
        print("Account created!")
        online = True
    else:
        print("sqn.")


def main_menu():
    options = {
        0: search_artist,
    }

    option = 0
    while option != 1:
        print("0. Procurar artista")
        print("1. Quit")
        option = int(input("> "))
        if (option >= 0) and (option < 1):
            options[option]()


def search_artist():
    print("1. Procurar Artista por nome: ")
    option = input("> ")

    if option == '1':
        nome = input("Nome: ")
        artistas = artists.search(nome)
        print(artistas)


def insert_artist():
    print("Inserir novo artista...")
    name = input("Introduza o nome do artista a criar: ")
    data = input("Introduza o data de nascimento do artista no formato YY-MM-DD:\n")
    try:
        artists.insert(name, data)
    except DatabaseError as error:
        print(error)
    else:
        print("Sucess")


def insert_song():

    print("Inserir nova música...")
    name = input("Introduza o nome da musica: ")
    date = input("Data da musica (aaa-mm-dd): ")
    history = input("Breve história da música: ")
    genre = input("Genero da musica: ")
    album = input("Nome do album: ")

    # try:
    #     while not albuns.exists_album(album):
    #         album = input("Nome do album: ")
    #
    #     artist = input("Nome do artista: ")
    #     while not artists.exists_artist(artist):
    #         artist = input("Nome do artista não encontrado!\nNome do artista:\n> ")
    #
    #     songs.insert_new(name, date, history, genre, album, artist)


def leave():
    print("Adeuxito manito.")
    exit(0)


if __name__ == '__main__':

    main_menu()
    exit(0)

    online = False
    print("1 - Register")
    print("2 - Login")
    print("3 - Leave")
    option = input("> ")

    if option == '1':
        register()
    elif option == '2':
        login()
    elif option == '3':
        leave()
