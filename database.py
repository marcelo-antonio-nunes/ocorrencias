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

def consultar_ocorrencias(filtros):
    ocorrencias = []
    with conectar_banco() as conn:
        cursor = conn.cursor()

        # sql = '''
        #     SELECT * FROM ocorrencias
        #     WHERE 1=1
        # '''

        # params = []
        # for campo, v in filtros.items():
        #     if v:
        #         # sql += f' AND {campo} LIKE ?'
        #         # params.append(f'%{valor}%')

        #         # sql += f' AND {campo} LIKE ?'
        #         params.append(v)

        # cursor.execute(sql, params)
        for c, v in filtros.items():
            if v:
                ocorrencias.append( cursor.execute(f"select * from ocorrencias where {c} =?",[v,]))
               
                print(f"V={v}")
                print(F"C={c}")
        ocorrencias = cursor.fetchall()

    return ocorrencias
