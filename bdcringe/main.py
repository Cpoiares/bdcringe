import bdcringe.database.user as user
import bdcringe.database.artists as artists
import bdcringe.database.songs as songs

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
    print("2 - Procurar Artista")
    option = input("> ")

    if option == '2':
        search_artist()


def search_artist():
    print("1 - Procurar Artista por nome")
    option = input("> ")

    if option == '1':
        nome = input("Nome: ")
        artistas = artists.search_name(nome)
        print(artistas)

def leave():
    print("kk.")
    return


if __name__ == '__main__':
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
