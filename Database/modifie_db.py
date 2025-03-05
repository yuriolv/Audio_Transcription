import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("language_school.db")
cursor = conn.cursor()

# Executar todas as instruções em um único comando
cursor.executescript('''

INSERT INTO Aluno (Nome, Email) VALUES ('Alice', 'alice@email.com');
INSERT INTO Aluno (Nome, Email) VALUES ('Bob', 'bob@email.com');
INSERT INTO Aluno (Nome, Email) VALUES ('Carlos', 'carlos@email.com');
INSERT INTO Aluno (Nome, Email) VALUES ('Diana', 'diana@email.com');
INSERT INTO Aluno (Nome, Email) VALUES ('Eduardo', 'eduardo@email.com');

INSERT INTO Professor (Nome, Email) VALUES ('Prof. Silva', 'silva@email.com');
INSERT INTO Professor (Nome, Email) VALUES ('Prof. Souza', 'souza@email.com');
INSERT INTO Professor (Nome, Email) VALUES ('Prof. Lima', 'lima@email.com');
INSERT INTO Professor (Nome, Email) VALUES ('Prof. Alves', 'alves@email.com');
INSERT INTO Professor (Nome, Email) VALUES ('Prof. Mendes', 'mendes@email.com');

INSERT INTO Aula (Data, Turma, idProfessor) VALUES ('2025-03-01', 'Turma A', 1);
INSERT INTO Aula (Data, Turma, idProfessor) VALUES ('2025-03-02', 'Turma B', 2);
INSERT INTO Aula (Data, Turma, idProfessor) VALUES ('2025-03-03', 'Turma C', 3);
INSERT INTO Aula (Data, Turma, idProfessor) VALUES ('2025-03-04', 'Turma D', 4);
INSERT INTO Aula (Data, Turma, idProfessor) VALUES ('2025-03-05', 'Turma E', 5);

INSERT INTO Transcricao (idAula, Hora, Frase) VALUES (1, '08:00', 'Bem-vindos à aula de hoje!');
INSERT INTO Transcricao (idAula, Hora, Frase) VALUES (2, '09:00', 'Vamos revisar o conteúdo passado.');
INSERT INTO Transcricao (idAula, Hora, Frase) VALUES (3, '10:00', 'Hoje aprenderemos sobre novas técnicas.');
INSERT INTO Transcricao (idAula, Hora, Frase) VALUES (4, '11:00', 'Espero que todos tenham feito os exercícios.');
INSERT INTO Transcricao (idAula, Hora, Frase) VALUES (5, '12:00', 'Vamos encerrar com um resumo.');

INSERT INTO Correcao (Correcao, idAluno, idTranscricao) VALUES ('Corrigido erro de concordância.', 1, 1);
INSERT INTO Correcao (Correcao, idAluno, idTranscricao) VALUES ('Revisão ortográfica feita.', 2, 2);
INSERT INTO Correcao (Correcao, idAluno, idTranscricao) VALUES ('Erro gramatical ajustado.', 3, 3);
INSERT INTO Correcao (Correcao, idAluno, idTranscricao) VALUES ('Frase reformulada.', 4, 4);
INSERT INTO Correcao (Correcao, idAluno, idTranscricao) VALUES ('Adicionado contexto.', 5, 5);
''')

conn.commit()
conn.close()