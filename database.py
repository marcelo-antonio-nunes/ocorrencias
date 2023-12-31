import sqlite3

DATABASE = 'ocorrencias.db'

def conectar_banco():
    return sqlite3.connect(DATABASE)

def criar_tabela():
    with conectar_banco() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                horario TEXT NOT NULL,
                nome_aluno TEXT NOT NULL,
                turma TEXT NOT NULL,
                serie TEXT NOT NULL,
                nome_prof TEXT NOT NULL,
                materia TEXT NOT NULL,
                ocorrencia TEXT NOT NULL,
                status1 TEXT NOT NULL,
                encaminhamento TEXT NOT NULL,
                status2 TEXT NOT NULL,
                numero_ata TEXT,
                convocacao TEXT,
                responsavel TEXT
            )
        ''')
        conn.commit()

def salvar_ocorrencia(data, horario, nome_aluno, turma, serie, nome_prof, materia,
                      ocorrencia, status1, encaminhamento, status2,
                      numero_ata, convocacao, responsavel):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ocorrencias (
                    data, horario, nome_aluno, turma, serie, nome_prof, materia,
                    ocorrencia, status1, encaminhamento, status2,
                    numero_ata, convocacao, responsavel
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data, horario, nome_aluno, turma, serie, nome_prof, materia,
                  ocorrencia, status1, encaminhamento, status2,
                  numero_ata, convocacao, responsavel))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving occurrence: {e}")

def consultar_ocorrencias(filtros):
    try:
        with conectar_banco() as conn:
            cursor = conn.cursor()
            
            # Construct the SQL query dynamically based on filters
            sql = 'SELECT * FROM ocorrencias WHERE 1=1'
            params = []

            for campo, valor in filtros.items():
                if valor:
                    sql += f' AND {campo}=?'
                    params.append(valor)

            cursor.execute(sql, params)
            ocorrencias = cursor.fetchall()

            return ocorrencias

    except sqlite3.Error as e:
        print(f"Error querying occurrences: {e}")
        return []

# Example usage:
# filtros = {'turma': 'A', 'status1': 'Pending'}
# resultados = consultar_ocorrencias(filtros)
# print(resultados)
