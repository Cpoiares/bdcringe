from psycopg2 import DatabaseError
from bdcringe.database import Database

global conn
global cur
global online


def login():
    try:
        sql = "SELECT * FROM utilizador where username like %s and password like %s "
        user = input("Insert Username:")
        pw = input("Insert Password: ")
        cur.execute(sql, (user, pw,))
    except DatabaseError as error:
        print("RIP LOGIN\n" + str(error))
        login()
    except(Exception, KeyboardInterrupt) as error:
        print("Cancelling login\nGoing back to the first menu")
        first_menu()
    else:
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
        print("Cancelling login\nGoing back to the first menu")
        first_menu()
    else:
        print("Logged in!")
        online = True
        main_menu()


def main_menu():

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
        print("FAILED TO SEARCH" + str(err))
    except(Exception, KeyboardInterrupt) as err:
        print(str(err))
        main_menu()
    else:
        print("SUCESS! Found: ")
        print(cur.fetchone())
        main_menu()


def first_menu():
    try:
        option = input("OPTIONS:\nREGISTER - 1\nLOGIN - 2\nCNTRL+C TO LEAVE")
    except(Exception, KeyboardInterrupt) as err:
        print("BYE\n" + str(err))
        leave()
    else: 
        if option == '1':
            register()
        elif option == '2':
            login()


def leave():
    print("BYE")
    return


if __name__ == '__main__':
    try:
        conn = Database().connect()
        cur = conn.cursor()

    except DatabaseError as error:
        print(error)

    finally:
        online = False
        first_menu()
