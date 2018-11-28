import bdcringe.database.albums as albums
import bdcringe.database.songs as songs
from bdcringe import User


def menu():
    print("Gestão de albums.")

    options = [
        (list_all, "Listar albums."),
        (search, "Procurar album.")
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
    print("Listar todos os albums.")

    lista = albums.get_all()

    for i, album in enumerate(lista):
        print("{4}. {3} - {0}".format(*album, i))


def search():
    print("Procurar album.")
    nome = input("Nome: ")

    lista = albums.search(nome)

    for i, album in enumerate(lista):
        print("{4}. {3} - {0}".format(*album, i))
    print("{}. Sair".format(len(lista)))

    option = int(input("Seleccionar album: "))

    if option == len(lista):
        return

    if (option >= 0) and (option < len(lista)):
        nome_album = lista[option][0]
        op = '0'
        while op != '2':
            print("0. Listar musicas.")
            print("1. [E] Adicionar musica.")
            print("2. Escrever critica.")
            print("3. Listar criticas.")
            print("4. Sair.")
            op = input("> ")

            if op == '1' and User.editor:
                insert_song(nome_album)
            elif op == '2':
                review(nome_album)
            elif op == '3':
                list_reviews(nome_album)
            elif op == '0':
                musicas = albums.songs(nome_album)
                for musica in musicas:
                    print(musica)


def insert_song(album):
    print("Inserir nova musica no album.")
    nome = input("Nome: ")
    data = input("Data da musica: ")
    historia = input("Breve história da música: ")
    genre = input("Genero da musica: ")

    if songs.insert_song(nome, data, historia, genre, album):
        print("Success.")
    else:
        print("Erro.")


def review(album):
    pontuacao = input("Pontuacao (0-100): ")
    justificacao = input("Justificacao: ")

    if albums.review(album, pontuacao, justificacao, User.username):
        print("Sucesso.")
    else:
        print("Erro.")


def list_reviews(album):
    values = albums.reviews(album)

    for x in values:
        print(x)


if __name__ == '__main__':
    menu()
