from flask import Flask, render_template, request, jsonify, json
from jinja2 import Environment, FileSystemLoader
from database import criar_tabela, salvar_ocorrencia, consultar_ocorrencias
import email.message
import smtplib

app = Flask(__name__)

template_env = Environment(loader=FileSystemLoader("templates"))

# Configuração do banco de dados SQLite
DATABASE = "ocorrencias.db"


@app.route("/enviar_email", methods=["POST"])
def enviar_email():
    dados = request.json.get("dados", [])
    corpo_email = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comunicado Importante - Ocorrência Escolar</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4;">

        <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #333;">Comunicado Importante - Ocorrência Escolar</h2>
            
            <p>Prezados pais e responsáveis,</p>
    """
    for ocorrencia in dados:
        corpo_email += f"""
        <p>Espero que esta mensagem os encontre bem. Gostaria de informar sobre um incidente ocorrido no dia {ocorrencia['data']}, durante o horário das {ocorrencia['horario']}, envolvendo o aluno {ocorrencia['aluno']}, do {ocorrencia['serie']}ª Ano turma {ocorrencia['turma']}.</p>

        <p><strong>Detalhes do incidente:</strong></p>
        <ul>
            <li>Data: {ocorrencia['data']}</li>
            <li>Horário: {ocorrencia['horario']}</li>
            <li>Aluno: {ocorrencia['aluno']}</li>
            <li>Ano/Série: {ocorrencia['serie']}ª</li>
            <li>Turma: {ocorrencia['turma']}</li>
             <li>Atendido por: {ocorrencia['atendido_por']}</li>
            <li>Ocorrência: {ocorrencia['ocorrencia']}</li>
        </ul>

        <p>A(o) professor(a) {ocorrencia['atendido_por']} relata que o aluno(a) esteve envolvido em uma ocorrência escolar. Estamos comprometidos em garantir a segurança e o bem-estar de todos os estudantes, e é por isso que compartilhamos essa informação com vocês.</p>

        <p>Para mais detalhes sobre o incidente ou para discutir medidas preventivas, pedimos que entrem em contato com a escola. pelo telefone:<strong>{ocorrencia['telResponsavel']} de segunda a sexta-feira das 10:00 às 15:00.</strong></p>

        <p>Agradecemos pela atenção e colaboração. Estamos à disposição para esclarecer qualquer dúvida e trabalhar em conjunto para manter um ambiente escolar seguro e saudável.</p>

        <p>Atenciosamente<br>
        <hr style="border: 0.5px solid #ccc; margin-top: 10px; margin-bottom: 10px;">
        <strong>Gestão/Coordenação<br>
        E.E.Professora Vânia Aparecida Cassará<br>
        Avenida João de Souza Franco, 350 - Jundiapeba - Mogi das Cruzes - SP<br>
        Telefone: (11) 4738-4112</strong></p>
        """

    corpo_email += """
        </div>
    </body>
    </html>
    """
    msg = email.message.Message()
    msg["Subject"] = "Assunto"
    msg["From"] = "marcelo197519@gmail.com"  #'escolavaniaaparecida2@gmail.com'
    msg["To"] = ocorrencia["email"]
    password = "vmztwphyxvxoyfrj"
    msg.add_header("Content-type", "text/html")
    msg.set_payload(corpo_email)
    s = smtplib.SMTP("smtp.gmail.com:587")
    s.starttls()
    s.login(msg["From"], password)
    s.sendmail(msg["From"], msg["To"], msg.as_string().encode("utf-8"))
    print("Email enviado")
    return corpo_email


# -----------------------------email---------------------------


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
    try:
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
            end_res = request.form["end_res"]
            email = request.form["email"]
            Atendido_por = request.form["Atendido_por"]

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
                end_res,
                email,
                Atendido_por,
            )

            return render_template("msg_ok.html")
        else:
            return render_template("msg_error.html")
    except:
        return render_template("index.html")


# Rota para a busca
@app.route("/busca", methods=["GET", "POST"])
def buscar_ocorrencias():
    try:
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
            responsavel = request.form["responsavel"]
            end_res = request.form.get("end_res")
            email = request.form.get("email")
            Atendido_por = request.form.get("Atendido_por")
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
                "responsavel": responsavel,
                "end_res": end_res,
                "email": email,
                "Atendido_por": Atendido_por,
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
                or responsavel
                or email
                or Atendido_por
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
    except:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
