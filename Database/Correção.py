import sqlite3


db_path = "language_school.db"

def create_correcao(correcao, id_aluno, id_transcricao):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Correcao (Correcao, idAluno, idTranscricao) VALUES (?, ?, ?)", (correcao, id_aluno, id_transcricao))
        conn.commit()

def read_correcoes():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Correcao")
        return cursor.fetchall()
    
def get_correcoes(student_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Erro FROM Correcao WHERE idAluno = ?", (student_id,))
        return cursor.fetchall()

def update_correcao(correcao_id, correcao, id_aluno, id_transcricao):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Correcao SET Correcao = ?, idAluno = ?, idTranscricao = ? WHERE Id = ?", (correcao, id_aluno, id_transcricao, correcao_id))
        conn.commit()

def delete_correcao(correcao_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Correcao WHERE Id = ?", (correcao_id,))
        conn.commit()