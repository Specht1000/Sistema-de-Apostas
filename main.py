#---------------------------------------------------------------------------
# Sistema de controle de apostas similar a Mega-Sena
# 
# Autor: Guilherme Martins Specht
# Data: 21/03/2024
# Version: 1.0                                                                                               
#---------------------------------------------------------------------------
# Projeto criado para exercicio DELL IT Academy
# - Sistema capaz de criar apostas
# - Listar todas as apostas
# - Finalizar aposta e realizar o sorteio
# - Realizar uma apuração
# - Entregar a premiação
#---------------------------------------------------------------------------

from apostas import Aposta
from sorteio import Sorteio
from servicoBD import adicionar_aposta, adicionar_sorteio
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

apostas = []

@app.route("/")
def index():
    Aposta.iniciar_apostas() # Inicia ou reinicia as apostas
    return render_template("index.html")

@app.route("/registrar_aposta", methods=["POST"])
def registrar_aposta():
    data = request.json  # Acessa os dados JSON enviados
    nome = data.get("nome")
    cpf = data.get("cpf")
    numeros = data.get("numeros", [])  # Garante que numeros seja uma lista

    if not all([nome, cpf, numeros]):
        return jsonify({"status": "error", "message": "Todos os campos são obrigatórios."}), 400 # Status de erro

    for aposta in Aposta.all: 
        if aposta.nome == nome and aposta.cpf == cpf and set(map(int, aposta.numeros)) == set(map(int, numeros)): # Analisa apostas repetidas
            return jsonify({"status": "error", "message": "Aposta duplicada."}), 400

    nova_aposta = Aposta(nome, cpf, list(map(int, numeros)), numero_registro=None) # Cria instância
    Aposta.all.append(nova_aposta) # Coloca na lista de todas as apostas

    adicionar_aposta(nome, cpf, numeros) # Adiciona a aposta no banco de dados

    return jsonify({"status": "success", "message": "Aposta registrada com sucesso.", "numero_registro": nova_aposta.numero_registro})

@app.route("/listar_apostas", methods=["GET"])
def listar_apostas():
    apostas_json = []
    if len(Aposta.all)  <= 0:
        return jsonify({"status": "error", "message": "Nenhuma aposta registrada."}), 400 # Status de erro
    else:
        for aposta in Aposta.all: # Convertendo cada objeto Aposta em um dicionário
            aposta_dict = {
                "nome": aposta.nome,
                "cpf": aposta.cpf,
                "numeros": aposta.numeros,
                "numero_registro": aposta.numero_registro
            }
            apostas_json.append(aposta_dict)
    
    return jsonify(apostas_json)

@app.route("/realizar_sorteio", methods=["GET"])
def sorteio():
    if len(Aposta.all) <= 0:
        return jsonify({"status": "error", "message": "Nenhuma aposta registrada."}), 400
    
    sorteio = Sorteio()
    numeros_sorteio, rodadas_extra, vencedores, mensagem_sorteio = sorteio.realiza_sorteio()
    
    mensagem_apuracao = sorteio.fim_apuracao(numeros_sorteio, rodadas_extra, vencedores)
    mensagem_premiacao = sorteio.premiacao(numeros_sorteio, rodadas_extra, vencedores)

    mensagem_final = mensagem_sorteio + mensagem_apuracao + mensagem_premiacao # Junta todas as informações
    print(mensagem_final)

    adicionar_sorteio(numeros_sorteio, rodadas_extra - 1)
    
    return jsonify({
        "status": "success",
        "mensagem": mensagem_final
    })



if __name__ == "__main__":
    app.run(debug=True)
