import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.songs as songs
import bdcringe.database.albums as albums
import bdcringe.database.labels as labels
import bdcringe.database.groups as groups
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
        print(error)
        #first_menu()
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
        print(err)
    except(Exception, KeyboardInterrupt) as err:
        print(err)
        main_menu()
    else:
        print("SUCESS! Found: ")
        print(cur.fetchone())
        main_menu()


def main_menu():
    options = {
        0: search_artist,
        1: insert_artist,
        2: insert_album,
        3: insert_group,
        4: insert_song,
        5: insert_label,
    }

    option = 0
    while option != 1:
        print("0. Procurar artista")
        print("1. Inserir artista")
        print("2. Inserir album")
        print("3. Inserir grupo")
        print("4. Inserir musica")
        print("5. Inserir editora")
        option = int(input("> "))
        if (option >= 0) and (option < 6):
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
        artists.insert_artist(name, date)
    except DatabaseError as error:
        print(error)
    else:
        print("Success.\nBack to main menu.")
        main_menu()


def insert_label():
    label = input("Introduza o nome da editora\n> ")
    try:
        labels.insert_new(label)
    except DatabaseError as error:
        print(error)
    else:
        print('Sucess')
        main_menu()


def insert_group():
    name = input("Introduza o nome do grupo a introduzir:\n> ")
    artista = input("Introduza o nome do artista a introduzir no grupo\n> ")
    while not artists.exists_artist(artista):
        artista = input("Introduza o nome do artista a introduzir no grupo\n> ")

    date_begin = input("Introduza a data de criação do grupo:\n> ")
    date_end = input("Introduza a data de fim do grupo: 0 caso de ainda estar ativo.\n> ")
    try:
        # cria um novo grupo e adiciona posteriormente
        groups.insert_new(name, date_begin, date_end)
        groups.add_artist(name, artista)
    except DatabaseError as error:
        print(error)
    else:
        print('Success')
        main_menu()


def insert_album():
    name = input("INSERIR NOVO ALBUM\nIntroduza o nome do album a adicionar:\n> ")
    date = input("Introduza a data de lançamento:\n> ")

    group = input("Introduza o grupo musical que gravou o album:\n> ")
    # TODO: Confirmar grupos musicais e não artistas
    while not groups.exists_group(group):
        group = input("Introduza o grupo musical que gravou o album:\n> ")

    label = input("Introduza a editora que criou o album:\n> ")
    while not labels.exists_label(label):
        label = input("Introduza a editora que criou o album:\n> ")
    try:
        albums.insert_new(name, date, group, label)
    except DatabaseError as error:
        print(error)
    else:
        print('Success')
        main_menu()


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
    except KeyboardInterrupt as error:
        print("CNTRL+C -> Going back to main menu")
        main_menu()
    except DatabaseError as error:
        print(error)
    else:
        print('Success')
        main_menu()


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
