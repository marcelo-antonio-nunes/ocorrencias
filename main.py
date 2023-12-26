from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados SQLite
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

# Página inicial
@app.route('/')
def index():
    return render_template('form_ocorrencia.html')

# Rota para lidar com o envio do formulário
@app.route('/salvar_ocorrencia', methods=['POST'])
def salvar_ocorrencia():
    criar_tabela()

    if request.method == 'POST':
        data = request.form['data']
        horario = request.form['horario']
        nome_aluno = request.form['nomeAluno']
        turma = request.form['turma']
        serie = request.form['serie']
        nome_prof = request.form['nomeProf']
        materia = request.form['materia']
        ocorrencia = request.form['ocorrencia']
        status1 = request.form['status1']
        encaminhamento = request.form['encaminhamento']
        status2 = request.form['status2']
        numero_ata = request.form['numeroATA']
        convocacao = request.form['convocacao']
        responsavel = request.form['responsavel']

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

        return render_template("msg_ok.html")
    else:
        return render_template("msg_error.html")

#====================Busca====================================
    
def consultar_ocorrencias(filtros):
    with conectar_banco() as conn:
        cursor = conn.cursor()

        # Construa a consulta SQL baseada nos filtros fornecidos
        sql = '''
            SELECT * FROM ocorrencias
            WHERE 1=1
        '''

        params = []
        for campo, valor in filtros.items():
            if valor:
                sql += f' AND {campo} LIKE ?'
                params.append(f'%{valor}%')

        # Execute a consulta
        cursor.execute(sql, params)
        ocorrencias = cursor.fetchall()

    return ocorrencias

@app.route('/busca', methods=['GET', 'POST'])
def buscar_ocorrencias():
    if request.method == 'POST':
        # Obtenha os parâmetros da consulta do formulário
        data = request.form.get('data')
        nome_aluno = request.form.get('nome_aluno')
        status1 = request.form.get('status1')
        status2 = request.form.get('status2')
        numero_ata = request.form.get('numero_ata')
        atendido_por = request.form.get('atendido_por')

        # Construa um dicionário com os filtros
        filtros = {
            'data': data,
            'nome_aluno': nome_aluno,
            'status1': status1,
            'status2': status2,
            'numero_ata': numero_ata,
            'responsavel': atendido_por
        }

        # Consulte o banco de dados com base nos filtros
        ocorrencias = consultar_ocorrencias(filtros)

        return render_template('resultados.html', ocorrencias=ocorrencias)

    return render_template('busca.html')
#-----------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
