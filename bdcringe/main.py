import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.songs as songs
import bdcringe.database.albums as albums
from psycopg2 import DatabaseError

global conn
global cur
global online


def login():
    global online

    username = input("Username: ")
    password = input("Password: ")

    if user.login(username, password):
        print("Logged in!")
        online = True
        main_menu()
  
  
def register():
    try:
        sql = "INSERT INTO utilizador(username, password) values(%s, %s)"
        user = input("Insert Username: ")
        pw = input("Insert Password: ")
        cur.execute(sql, (user, pw,))
    except DatabaseError as error:
        print("RIP REGISTER" + str(error))
        register()
    except(Exception, KeyboardInterrupt) as error:
        print("Cancelling login\nGoing back to the first menu")
        first_menu()
    else:
        print("Logged in!")
        online = True
        main_menu()


def register():
    global online

    switch_dict = {
        "0" : leave,
        "1" : find_user
    }
    for key in switch_dict:
        print(key, " -> ", switch_dict.get(key))
    option = input("Enter valid option\n")
    if option in switch_dict:
        switch_dict[option]()
    else:
        print("ENTER A VALID OPTION")
        main_menu()


def find_user():
    try:
        sql = "SELECT username, password FROM utilizador WHERE username = %s"
        user = input("INSERT USERNAME TO SEARCH: ")
        cur.execute(sql, (user,))
    except DatabaseError as err:
        print("FAILED TO SEARCH" + str(err))
    except(Exception, KeyboardInterrupt) as err:
        print(str(err))
        main_menu()
    else:
        print("SUCESS! Found: ")
        print(cur.fetchone())
        main_menu()


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
    print("1 - Procurar Artista por nome")
    option = input("> ")

    if option == '1':
        nome = input("Nome: ")
        artistas = artists.search_name(nome)
        print(artistas)

def insert_artist():
    print("INSERIR NOVO ARTISTA\nIntroduza o nome do artista a criar:\n")
    name = input("> ")
    print("Introduza o data de nascimento do artista no formato YY-MM-DD:\n")
    date = input("> ")
    try:
        artists.new_artist(name, date)
    except DatabaseError as error:
        print(error)
    else:
        print("Sucess")

def insert_song():
    try:
        print("INSERIR NOVA MUSICA\nIntroduza o nome da musica:\n")
        name = input("> ")
        date = input("Data da musica:\n> ")
        history = input("Breve história da música:\n> ")
        genre = input("Genero da musica:\n> ")

        album = input("Nome do album:\n> ")
        while not albums.exists_album(album):
            album = input("Nome do album:\n> ")

        artist = input("Nome do artista:\n> ")
        while not artists.exists_artist(artist):
            artist = input("Nome do artista não encontrado!\nNome do artista:\n> ")

        songs.insert_new(name, date, history, genre, album, artist)
        # sei lá o que criar primeiro ja pego nisto
    except KeyboardInterrupt as error:
        print("CNTRL+C -> Going back to main menu")
        main_menu()
    except DatabaseError as error:
        print(error)


def leave():
    print("BYE")
    return


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
