import bdcringe.database.artists as artists
import bdcringe.database.groups as groups
import bdcringe.database.albuns as albuns
import bdcringe.database.labels as labels


def menu():
    print("Gestão de grupos")

    options = {
        0: list_all,
        1: insert,
        2: search
    }

    option = 0
    while option != len(options):
        print(chr(27) + "[2J") # clear
        print("0. Listar grupos.")
        print("1. Inserir novo grupo.")
        print("2. Procurar grupo.")
        print("3. Sair")
        option = int(input("> "))
        if (option >= 0) and (option < len(options) + 1):
            if option != len(options):
                options[option]()


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
        print('Success')
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
            print("1. Adicionar artista.")
            print("2. Adicionar albúm.")
            print("3. Sair.")
            op = input("> ")

            if op == '1':
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
            elif op == '2':
                nome_album = input("Nome do novo album: ")
                data_lancamento = input("Data de lancamento (yyyy-mm-dd): ")
                nome_editora = input("Nome da editora: ")

                while not labels.exists(nome_editora):
                    nome_editora = input("Nome da editora: ")

                if albuns.insert(nome_album, data_lancamento, nome_grupo, nome_editora):
                    print("Sucesso.")
                else:
                    print("Erro.")
