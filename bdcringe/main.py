import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.songs as songs
import bdcringe.database.labels as labels
import bdcringe.database.groups as groups
import bdcringe.database.albuns as albuns
from psycopg2 import DatabaseError


def login():
    username = input("Username: ")
    password = input("Password: ")
    return user.login(username, password)


def register():
    username = input("Username: ")
    password = input("Password: ")
    return user.register(username, password)


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
        print("7. Sair")
        option = int(input("> "))
        if (option >= 0) and (option < len(options) + 1):
            if option == len(options):
                return
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
        labels.insert(label)
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
        groups.insert(name, date_begin, date_end)
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
    while not groups.exists(group):
        group = input("Introduza o grupo musical que gravou o album:\n> ")

    label = input("Introduza a editora que criou o album:\n> ")
    while not labels.exists(label):
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

        songs.insert(nome, data, historia, genre, album, artista)

    except DatabaseError as error:
        print(error)
    else:
        print('Success')
        main_menu()


if __name__ == '__main__':

    online = False
    leave = False

    while not online and not leave:
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
