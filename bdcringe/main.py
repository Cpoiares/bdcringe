import bdcringe.database.user as user

global online


def login_menu():
    global online

    username = input("Username: ")
    password = input("Password: ")

    if user.login(username, password):
        print("Logged in!")
        online = True
    else:
        print("sqn.")


def register_menu():
    global online

    username = input("Username: ")
    password = input("Password: ")

    if user.register(username, password):
        print("Account created!")
        online = True
    else:
        print("sqn.")


def first_menu():
    try:
        print("1 - Register")
        print("2 - Login")
        print("3 - Leave")
        option = input("> ")
    except(Exception, KeyboardInterrupt) as err:
        print("BYE\n" + str(err))
        leave()
    else: 
        if option == '1':
            register_menu()
        elif option == '2':
            login_menu()
        elif option == '3':
            leave()


def leave():
    print("kk.")
    return


if __name__ == '__main__':
    online = False
    first_menu()
