import random

class Aposta:
    
    all = [] # Lista que guarda objetos da classe Aposta
    numero_registro_atual = 1000  # Número de registro inicial

    # Construtor
    def __init__(self, nome: str, cpf: int, numeros: list, numero_registro: int):
        self.__nome = nome
        self.__cpf = cpf
        self.__numeros = numeros
        if numero_registro is None:
            self.__numero_registro = Aposta.numero_registro_atual  # Usa o número de registro atual
            Aposta.numero_registro_atual += 1  # Incrementa o número de registro atual para a próxima aposta
        else:
            self.__numero_registro = numero_registro

    # Inicialização das apostas
    @classmethod
    def iniciar_apostas(cls):
        cls.all = []
        Aposta.numero_registro_atual = 1000


    # Definições de Getter da linguagem Python
    # Getter de nome
    @property
    def nome(self):
        return self.__nome
    
    # Getter de CPF
    @property
    def cpf(self):
        return self.__cpf
    
    # Getter de números
    @property
    def numeros(self):
        return self.__numeros
    
    # Getter do número de registro
    @property
    def numero_registro(self):
        return self.__numero_registro