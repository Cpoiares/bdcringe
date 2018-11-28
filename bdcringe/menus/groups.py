import bdcringe.database.artists as artists
import bdcringe.database.groups as groups
import bdcringe.database.albums as albums
import bdcringe.database.labels as labels
from bdcringe import User


def menu():
    print("Gestão de grupos")

    options = [
        (list_all, "Listar grupos.", False),
        (insert, "Inserir novo grupo.", True),
        (search, "Procurar grupo.", False)
    ]

    op = 0
    while op != len(options):
        print(chr(27) + "[2J") # clear
        for i, option in enumerate(options):
            print("{0}. {1} {3}".format(i, "[E]" if option[2] else "   ", *option))
        print(len(options),". Sair")

        op = int(input("> "))
        if (op >= 0) and (op < len(options)):
            if options[op][2] and not User.editor:
                print("Nao tem permissoes de editor.")
            else:
                options[op][0]()


def list_all():
    print("Listagem de todos os grupos")

    grupos = groups.get_all()

    for i, grupo in enumerate(grupos):
        print("{3}. ({2} até {1}) {0}".format(*grupo, i))


def insert():
    name = input("Nome do grupo músical: ")
    date_begin = input("Data de criação do grupo: ")
    date_end = input("Data de fim do grupo ('0' no caso de ainda esteja ativo):  ")

    if groups.insert(name, date_begin, date_end):
        print("Success")
    else:
        print("Erro.")


def search():
    print("Procurar grupo.")
    nome = input("Nome: ")

    grupos = groups.search(nome)

    for i, grupo in enumerate(grupos):
        print("{3}. ({2} até {1}) {0}".format(*grupo, i))
    print("{}. Sair".format(len(grupos)))

    option = int(input("Seleccionar grupo: "))

    if option == len(grupos):
        return

    if (option >= 0) and (option < len(grupos)):
        nome_grupo = grupos[option][0]
        op = '0'
        while op != '3':
            print("0. Listar artistas do grupo.")
            print("1. [E] Adicionar artista.")
            print("2. [E] Adicionar albúm.")
            print("3. Sair.")
            op = input("> ")

            if op == '1' and User.editor:
                artista = input("Nome do artista a inserir no grupo: ")

                while not artists.exists(artista):
                    artista = input("Nome do artista a inserir no grupo: ")

                if groups.add_artist(artista, nome_grupo):
                    print("Sucesso.")
                else:
                    print("Erro")
            elif op == '0':
                artistas = groups.members(nome_grupo)
                for x in artistas:
                    print(x)
            elif op == '2' and User.editor:
                nome_album = input("Nome do novo album: ")
                data_lancamento = input("Data de lancamento (yyyy-mm-dd): ")
                nome_editora = input("Nome da editora: ")

                while not labels.exists(nome_editora):
                    nome_editora = input("Nome da editora: ")

                if albums.insert(nome_album, data_lancamento, nome_grupo, nome_editora):
                    print("Sucesso.")
                else:
                    print("Erro.")
