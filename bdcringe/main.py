from bdcringe import User
import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.labels as labels
import bdcringe.menus.groups as groups
import bdcringe.menus.albums as albums
import bdcringe.menus.playlists as playlists

from psycopg2 import DatabaseError


def login():
    username = input("Username: ")
    password = input("Password: ")
    value = user.login(username, password)
    if value:
        print(value)
        User.username = value[0]
        User.editor = value[1]
        return True
    return False


def register():
    username = input("Username: ")
    password = input("Password: ")
    value = user.register(username, password)
    if value:
        User.username = value[0]
        User.editor = value[1]
        return True
    return False



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

    if artists.insert(name, data):
        print("Sucesso.")
    else:
        print("Erro.")


def list_artist_songs():
    artista = input("Introduza o nome do artista a procurar:\n> ")

    while not artists.exists(artista):
        artista = input("Introduza o nome do artista a procurar:\n> ")

    try:
        print(artists.get_songs(artista))
    except DatabaseError as error:
        print(error)


def main_menu():
    options = [
        (insert_label, "Inserir editora.", True),
        (make_editor, "Tornar editor.", True),
        (insert_artist, "Inserir Artista.", True),
        (groups.menu, "Gestão de grupos.", False),
        (albums.menu, "Gestão de albuns.", False),
        (playlists.menu, "Gestão de playlists.", False),
        (insert_label, "Inserir editora.", True),
        (list_artist_songs, "Listar musicas de um artista.", False),
        (list_labels, "Listar editoras.", False),
        (make_editor, "Tornar editor.", True),
    ]

    op = 0
    while op != len(options):
        print(chr(27) + "[2J") # clear
        for i, option in enumerate(options):
            print("{}. {} {}".format(i, "[E]" if option[2] else '', option[1]))
        print(len(options),". Sair")

        op = int(input("> "))
        if (op >= 0) and (op < len(options)):
            if options[op][2] and not User.editor:
                print("Nao tem permissoes de editor.")
            else:
                options[op][0]()


def make_editor():
    print("Procurar utilizador.")
    username = input("Nome: ")
    users = user.find_user(username)

    for i, v in enumerate(users):
        print("{}. {}".format(i, v[0]))

    print("{}. Sair".format(len(users)))

    op = int(input("> "))
    if (op >= 0) and (op < len(users)):
        username = users[op][0]

        if user.make_editor(username):
            print("Sucesso.")
        else:
            print("Erro.")


if __name__ == '__main__':
    leave = False
    online = False

    while not online and not leave:
        print(chr(27) + "[2J") # clear
        print("1. Registar")
        print("2. Login")
        print("3. Sair")
        option = input("> ")

        if option == '1':
            online = register()
        elif option == '2':
            online = login()
        elif option == '3':
            leave = True

        if leave:
            print("Adeus.")
            exit(0)

        if not online:
            print("Tente outra vez.")
        else:
            main_menu()
            online = False
            leave = False
