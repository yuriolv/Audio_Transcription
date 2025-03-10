import sqlite3


db_path = "language_school.db"

def create_transcricao(id_aula, frase):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Transcricao (idAula, Frase) VALUES (?, ?)", (id_aula, frase))
        conn.commit()

def read_transcricoes():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Frase FROM Transcricao")
        return cursor.fetchall()

def update_transcricao(transcricao_id, id_aula, frase):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Transcricao SET idAula = ?, Frase = ? WHERE Id = ?", (id_aula, frase, transcricao_id))
        conn.commit()

def delete_transcricao(transcricao_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Transcricao WHERE Id = ?", (transcricao_id,))
        conn.commit()