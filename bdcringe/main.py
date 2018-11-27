import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.songs as songs
import bdcringe.database.labels as labels
import bdcringe.database.groups as groups
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
        1: insert_artist,
        2: insert_album,
        3: insert_group,
        4: insert_song,
        5: insert_label,
        6: list_artist_songs
    }

    option = 0
    while option != 1:
        print("0. Procurar artista")
        print("1. Inserir artista")
        print("2. Inserir album")
        print("3. Inserir grupo")
        print("4. Inserir musica")
        print("5. Inserir editora")
        print("6. Listar musicas de um artista")
        option = int(input("> "))
        if (option >= 0) and (option < len(options)):
            options[option]()


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

    while not artists.exists(artista):
        artista = input("Introduza o nome do artista a introduzir no grupo\n> ")

    date_begin = input("Introduza a data de criação do grupo:\n> ")
    date_end = input("Introduza a data de fim do grupo: 0 caso de ainda estar ativo.\n> ")

    try:
        # cria um novo grupo e adiciona posteriormente
        groups.insert_new(name, date_begin, date_end)
        groups.add_artist(artista, name)
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
        albuns.insert(name, date, group, label)
    except DatabaseError as error:
        print(error)
    else:
        print('Success')
        main_menu()


def list_artist_songs():
    artista = input("Introduza o nome do artista a procurar:\n> ")

    while not artists.exists(artista):
        artista = input("Introduza o nome do artista a procurar:\n> ")

    try:
        print(artists.get_songs(artista))
    except DatabaseError as err:
        print(err)


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

        songs.insert_new(nome, data, historia, genre, album, artista)

    except DatabaseError as error:
        print(error)
    else:
        print('Success')
        main_menu()


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
