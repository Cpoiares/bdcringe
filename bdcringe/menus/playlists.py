import bdcringe.database.playlists as playlists
import bdcringe.database.songs as songs

from bdcringe import User


def edit_playlist():
    print("Listagem de todos as playlists")

    listas = playlists.get_all(User.username)

    for i, lista in enumerate(listas):
        print("{1}. {0}".format(lista[1], i))
    print("{}. Sair".format(len(listas)))

    option = int(input("Seleccionar playlist: "))

    if option == len(listas):
        return
    if (option >= 0) and (option < len(listas)):
        id_playlist = int(listas[option][0])
        nome_playlist = listas[option][1]

    op = '0'
    while op != '4':
        print("0. Inserir musica.")
        print("1. Remover musica.")
        print("2. Listar musicas")
        print("3. Mudar privacidade")
        print("4. Sair.")
        op = input("> ")

        if op == '0':
            musicas = songs.get_all()
            for j, musica in enumerate(musicas):
                print("{1}. {0}".format(musica[1], j))
            print("{}. Sair".format(len(musica)))

            option = int(input("Seleccionar musica a adicionar: "))
            if option == len(musicas):
                return
            if (option >= 0) and (option < len(musicas)):
                id_musica = int(musicas[option][0])
                op = '0'
            if playlists.add_song(id_playlist, id_musica):
                print('Sucesso')
            else:
                print('Erro.')

        elif op == '1':
            musicas = playlists.list_songs(id_playlist)
            for i, musica in enumerate(musicas):
                print("{1}. {0}".format(musica[1], i))
            print("{}. Sair".format(len(musica)))

            option = int(input("Seleccionar musica a remover: "))
            if option == len(musicas):
                return
            if (option >= 0) and (option < len(musicas)):
                id_musica = int(musicas[option][0])
                op = '0'
            if playlists.remove_song(id_playlist, id_musica):
                print('Sucesso')
            else:
                print('Erro.')

        elif op == '2':
            print("Musicas da playlist '{0}': ".format(nome_playlist))
            musicas = playlists.list_songs(id_playlist)
            for i, musica in enumerate(musicas):
                print("{1}. {0}".format(musica[1], i))
            print("-----------------------------------")

        elif op == '3':
            value = playlists.get_status(id_playlist)[0]
            print(value)
            if value is not None and value[0] is True:
                print("Playlist {0} privada. Tornar pública?\n0 - Sim\n1 - Não")
                if input("> ") == '0':
                    playlists.set_status(id_playlist, False)
            elif value is not None and value[0] is False:
                print("Playlist {0} publica. Tornar privada?\n0 - Sim\n1 - Não")
                if input("> ") == '0':
                    playlists.set_status(id_playlist, True)


def insert_playlist():
    nome = input("Introduza o nome da playlist:\n> ")
    if playlists.insert(nome, User.username):
        print('Sucesso.')
    else:
        print('Erro.')


def menu():
    print("Gestão de playlists")

    options = [
        (insert_playlist, "Inserir playlist.", False),
        (edit_playlist, "Editar playlist.", False)

    ]

    op = 0
    while op != len(options):
        for i, option in enumerate(options):
            print("{0}. {1} {3}".format(i, "[E]" if option[2] else "   ", *option))
        print(len(options), ". Sair")

        op = int(input("> "))
        if (op >= 0) and (op < len(options)):
            if options[op][2] and not User.editor:
                print("Nao tem permissoes de editor.")
            else:
                options[op][0]()

