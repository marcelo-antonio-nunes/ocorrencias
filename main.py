from flask import Flask, render_template, request
from database import criar_tabela, salvar_ocorrencia, consultar_ocorrencias

app = Flask(__name__)

# Configuração do banco de dados SQLite
DATABASE = "ocorrencias.db"


# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ocorrencia")
def ocorrencia():
    return render_template("form_ocorrencia.html")

# Rota para lidar com o envio do formulário
@app.route("/salvar_ocorrencia", methods=["POST"])
def salvar_ocorrencia_route():
    criar_tabela()

    if request.method == "POST":
        # Obtenha os dados do formulário
        data = request.form["data"]
        horario = request.form["horario"]
        nome_aluno = request.form["nomeAluno"]
        turma = request.form["turma"]
        serie = request.form["serie"]
        nome_prof = request.form["nomeProf"]
        materia = request.form["materia"]
        ocorrencia = request.form["ocorrencia"]
        status1 = request.form["status1"]
        encaminhamento = request.form["encaminhamento"]
        status2 = request.form["status2"]
        numero_ata = request.form["numeroATA"]
        convocacao = request.form["convocacao"]
        responsavel = request.form["responsavel"]

        # Salvar a ocorrência no banco de dados
        salvar_ocorrencia(
            data,
            horario,
            nome_aluno,
            turma,
            serie,
            nome_prof,
            materia,
            ocorrencia,
            status1,
            encaminhamento,
            status2,
            numero_ata,
            convocacao,
            responsavel,
        )

        return render_template("msg_ok.html")
    else:
        return render_template("msg_error.html")


# Rota para a busca
@app.route("/busca", methods=["GET", "POST"])
def buscar_ocorrencias():
    if request.method == "POST":
        # Obtenha os parâmetros da consulta do formulário
        data = request.form.get("data")
        nome_aluno = request.form.get("nome_aluno")
        status1 = request.form.get("status1")
        status2 = request.form.get("status2")
        numero_ata = request.form.get("numeroATA")
        nome_prof = request.form.get("nome_prof")
        turma = request.form.get("turma")
        serie = request.form.get("serie")

        # Construa um dicionário com os filtros
        filtros = {
            "nome_aluno": nome_aluno,
            "data": data,
            "status1": status1,
            "status2": status2,
            "numero_ata": numero_ata,
            "nome_prof": nome_prof,
            "turma": turma,
            "serie": serie,
        }
        if (
            nome_aluno
            or data
            or status1
            or status2
            or numero_ata
            or nome_prof
            or turma
            or serie
        ):
            # Consulte o banco de dados com base nos filtros
            r = consultar_ocorrencias(filtros)
            ocorrencias = []
            for i in r:
                ocorrencias.append(i)
            return render_template(
                "busca.html", ocorrencias=ocorrencias, len=len(ocorrencias)
            )

    return render_template("busca.html")


if __name__ == "__main__":
    app.run(debug=True)
