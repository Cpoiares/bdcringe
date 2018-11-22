import psycopg2
import sys

global cur
global conn



def drop():
    sqlDROP = """DROP TABLE %s;"""
    table = input("WHICH TABLE TO DROP")
    cur.execute(sqlDROP)
    conn.commit()
    cur.close()

def create():
    # cria apenas users para teste | alterar: pedir nome da tabela, e parametros, pedir caracteristicas de parametros -> concatenar strings e formar command
    sqlTABLE = """CREATE TABLE users (user_id SERIAL PRIMARY KEY, 
                                username VARCHAR(255) UNIQUE NOT NULL, 
                                password VARCHAR(255) NOT NULL)"""
    try:
        cur.execute(sqlTABLE)
        print("SUCESS")
        # commit the changes
        conn.commit()
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Failed to create table\n" + str(error))
    except(Exception, KeyboardInterrupt) as error:
        print("Interrupted\n" + str(error))

def leave():
    conn.commit()
    cur.close()
    return


if __name__ == "__main__":
    try:
        conn = psycopg2.connect(host="localhost", database="dropmusic", user="postgres", password="postgres")
        cur = conn.cursor()
        option = input("CREATE - 1\nDROP - 2\nQUIT - 3")
        if option == '1':
            create()
        elif option == '2':
            drop()
        elif option == '3':
            leave()
        
    except(Exception, psycopg2.DatabaseError) as err:
        print("MAIN FAIL\n" + + str(error))
