import random
from apostas import Aposta

class Sorteio:
    vencedores = []

    # Construtor
    def __init__(self):
        self.__numeros_sorteio = []
        self.__rodadas_extra = 0

    # Método que diz se foi realizada alguma aposta
    @staticmethod
    def destrava_apostas():
        if len(Aposta.all) <= 0:
            return False
        else:
            return True

    def realiza_sorteio(self):
        mensagem = ""

        Sorteio.vencedores = []  # Limpa a lista de vencedores
        self.__numeros_sorteio = []  # Limpa a lista de números sorteados
        self.__rodadas_extra = 0  # Reseta o contador de rodadas extras

        if self.destrava_apostas():
            self.__rodadas_extra = 1
            mensagem += "Realizando sorteio...\n"
            self.__numeros_sorteio = random.sample(range(1, 51), 5)
            mensagem += f"Números sorteados: {self.__numeros_sorteio}\n"
            
            # Loop que checa se há um vencedor
            while self.__rodadas_extra <= 25:
                ha_vencedor = False # Verifica se há pelo menos um vencedor
                vencedores_rodada = [] # Lista das apostas vencedoras

                for aposta in Aposta.all:
                    acertos = set(aposta.numeros) & set(self.__numeros_sorteio) # Analisa quantos valores estão na intersecção dos dois conjuntos
                    if len(acertos) == 5: # Se todo conjunto de numeros apostados estiverem no conjunto de números sorteados significa que o apostador venceu
                        vencedores_rodada.append(aposta) # Insere a aposta na lista de vencedores

                if vencedores_rodada:
                    ha_vencedor = True
                    for vencedor in vencedores_rodada:
                        mensagem += f"Parabéns para {vencedor.nome}! Você é um vencedor na rodada {self.__rodadas_extra - 1}.\n"
                        # Aqui é necessário adicionar cada vencedor individualmente
                        Sorteio.vencedores.append(vencedor)

                if ha_vencedor:
                    break

                while True:
                    numero_novo = random.randint(1, 50) # Sorteia um número extra ao sorteio
                    if numero_novo not in self.__numeros_sorteio:
                        self.__numeros_sorteio.append(numero_novo) # Insere na lista de núemro sorteados
                        self.__rodadas_extra += 1 # Conta a nova rodada
                        break

            if self.__rodadas_extra == 25 and not Sorteio.vencedores:
                mensagem += "Não houve nenhum vencedor."

        sorteio = Sorteio()
        return self.__numeros_sorteio, self.__rodadas_extra, sorteio.vencedores, mensagem

    
    # Método que realiza o fim da apuração
    def fim_apuracao(self, numeros_sorteio, rodadas_extra, vencedores):
        mensagem = "\n\n------------ Fim da apuração ------------\n"
        mensagem += f"- Números sorteados: {sorted(numeros_sorteio)}\n"
        mensagem += f"- Quantidade de rodadas de sorteio realizadas: {rodadas_extra-1}\n"
        mensagem += f"- Quantidade de apostas vencedoras: {len(vencedores)}\n"
        if len(vencedores) > 0: # Verfica se há vencedores
            mensagem += "- Lista de apostas vencedoras:\n"
            vencedores = sorted(vencedores, key=lambda aposta: aposta.nome) # Ordena em ordem alfabética
            for aposta in vencedores:
                # Imprime na tela os vencedores
                mensagem += f"---- Nome: {aposta.nome} | CPF: {aposta.cpf} | Números: {sorted(aposta.numeros)}\n"
        else:
            mensagem += "- Não houve vencedores."

        # Trecho do código que analisa quantas vezes um número foi apostado
        mensagem += f"\n- Lista de todos os números apostados:\n"
        numeros_e_quantidades = {} # Dicionário que diz o número e sua quantidades
        for aposta in Aposta.all:
            for num in aposta.numeros:
                if num in numeros_e_quantidades:
                    numeros_e_quantidades[num] += 1 # Se o número ja estiver no dicionário adiciona um
                else:
                    numeros_e_quantidades[num] = 1 # Se o número não estiver no dicionário inicializa
        
        # Ordena dos número que mais apareceu para o que menos apareceu
        numeros_e_quantidades = sorted(numeros_e_quantidades.items(), key=lambda x: x[1], reverse=True)
        mensagem += f"Nro apostado Qtd de apostas\n" # Imprime na tela os números e as quantidades
        for num, qtd in numeros_e_quantidades:
            if num < 10:
                mensagem += f" "   
            mensagem += f"             {num:<22}{qtd}\n"

        Aposta.iniciar_apostas()
        numeros_sorteio = []
        rodadas_extra = 0

        return mensagem

    # Método que define a premiação    
    def premiacao(self, numeros_sorteio, rodadas_extra, vencedores):
        mensagem = ""
        if len(vencedores) > 0:
            premio_total = 10000000 # Prêmio de 10M !!!!!
            premio_por_vencedor = premio_total / len(vencedores) # Divide o prêmio entre os vencedores
            mensagem += "\n\n\n------------ Parabéns aos vencedores! ------------"
            mensagem +=  "\n- Detalhes da premiação:"
            for vencedor in vencedores: # Imprime os vencedores
                mensagem += f"\n-- Nome: {vencedor.nome} | CPF: {vencedor.cpf} | Números apostados: {sorted(vencedor.numeros)} | Números sorteados: {sorted(numeros_sorteio)}\n Número de rodadas: {rodadas_extra-1} | Número de registro: {vencedor.numero_registro}"
            mensagem += f"\n-- Valor do prêmio por vencedor: R$ {premio_por_vencedor:.2f}"

        return mensagem   

    # Definições de Getter da linguagem Python
    # Getter de números sorteados
    @property
    def nome(self):
        return self.__numeros_sorteio
    
    # Getter das rodadas adicionais
    @property
    def cpf(self):
        return self.__rodadas_extra