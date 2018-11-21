import psycopg2
import sys

global conn 
global cur 
global online


def login():
    try:
        sql = """SELECT * FROM users where username like %s and password like %s """
        user = raw_input("Insert Username:")
        print(user)
        pw = raw_input("Insert Password: ")
        cur.execute(sql, (user, pw,))
    except(Exception, psycopg2.DatabaseError) as error:
        print("RIP LOGIN\n" + str(error))
        login()
    except(Exception, KeyboardInterrupt) as error:
        print("Cancelling login")
        firstMenu()
    else:
        print("Logged in!")
        online = True
        mainMenu()
  
  
def register():
    try:
        sql = """INSERT INTO users(username, password) values(%s, %s) returning user_id"""
        user = raw_input("Insert Username: ")
        pw = raw_input("Insert Password: ")
        cur.execute(sql, (user, pw,))
    except(Exception, psycopg2.DatabaseError) as error:
        print("RIP REGISTER" + str(error))
        register()
    except(Exception, KeyboardInterrupt) as error:
        print("Cancelling register" + str(error))
        firstMenu()
    else:
        print("Logged in!")
        online = True
        mainMenu()

def mainMenu():
    try:
        switch_dict = {
                        "1" : findUser,
                        #"2" : findMusic,
                        "10" : leave
        }
        for key in switch_dict:
            print(str(key) + " -> " + str(switch_dict.get(key)) + "\n")
        option = raw_input("Enter valid option\n")
        if option in switch_dict:
            switch_dict[option]()
        else:
            print("ENTER A VALID OPTION")
            mainMenu()
    except(Exception, KeyboardInterrupt) as err:
        print(str(err))
        leave()

def findUser():
    try:
        sql = """SELECT username, password FROM users WHERE username = %s"""
        user = raw_input("INSERT USERNAME TO SEARCH: ")
        cur.execute(sql, (user,))
    except(Exception, psycopg2.DatabaseError) as err:
        print("FAILED TO SEARCH" + str(err))
    except(Exception, KeyboardInterrupt) as err:
        print(str(err))
        mainMenu()
    else:
        print("SUCESS! Found: ")
        print(cur.fetchone())
        mainMenu()

def firstMenu():
    try:
        option = input("OPTIONS:\nREGISTER - 1\nLOGIN - 2\n")
        if option == 1:
            register()
        elif option == 2:
            login()
    except(Exception, KeyboardInterrupt) as err:
        print("BYE\n" + str(err))
        return

def leave():
    conn.commit()
    cur.close()
    print("BYE")
    return

if __name__ == '__main__':
    try:
        conn = psycopg2.connect(host="localhost", database="dropmusic", user="postgres", password="postgres")
        cur = conn.cursor()
    except(Exception, psycopg2.DatabaseError) as err:
        print(str(err))
    else:
        online = False
        firstMenu()
    