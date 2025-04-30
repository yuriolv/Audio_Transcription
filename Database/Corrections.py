import sqlite3


db_path = "language_school.db"

def create_correction(correction, phrase, id_student, id_transcription):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Corrections (Error, Phrase, Student_Id, Transcription_Id) VALUES (?, ?, ?, ?)", (correction, phrase, id_student, id_transcription))
        conn.commit()

def read_corrections():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Corrections")
        return cursor.fetchall()
    
def get_corrections(student_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Phrase,Error FROM Corrections WHERE Student_id = ? " \
        "order by Transcription_Id DESC, Id DESC LIMIT 4;", (student_id,))
        return cursor.fetchall()[-3:]

def update_correction(correction_id, correction, id_student, id_transcription):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Corrections SET Correction = ?, Student_Id = ?, Transcription_Id = ? WHERE Id = ?", (correction, id_student, id_transcription, correction_id))
        conn.commit()

def delete_correction(correction_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Corrections WHERE Id = ?", (correction_id,))
        conn.commit()

get_corrections(1)