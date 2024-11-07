import sqlite3

def conectarBanco():
    conn = sqlite3.connect('C://Users//Guilherme//Desktop//Projetos//Alura_challenger/challenger.db')
    return conn


def criarBanco():
    with conectarBanco() as db:
        with open('schema.sql', 'r') as file:
            sql_script = file.read()
            db.cursor().executescript(sql_script)
        db.commit()
    
    

