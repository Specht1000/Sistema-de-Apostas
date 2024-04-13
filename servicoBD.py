import pyodbc

class DatabaseManager:
    def __init__(self):
        self.server = "DESKTOP-FGNNDCL\SQLEXPRESS" # Alterar o DESKTOP com informa o template de resolução
        self.database = "ITAcademyDell"
        self.driver = "SQL SERVER"
        self.conn_str = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};"

    def execute_non_query(self, query, params=None): # Método para gerenciar o banco de dados
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()

db_manager = DatabaseManager() # Cria a instância do gerenciador do banco de dados

def adicionar_aposta(nome, cpf, numeros):
    query = """
    INSERT INTO Aposta (Nome, CPF, Numeros) VALUES (?, ?, ?)
    """ # Comando SQL que insere uma nova linha na tabela apostas
    numeros_str = ",".join(map(str, numeros))  # Converte a lista de números em uma string
    db_manager.execute_non_query(query, (nome, cpf, numeros_str)) # Executa a linha de código SQL

def adicionar_sorteio(numeros_sorteados, rodadas_extra):
    query = """
    INSERT INTO Sorteio (NumerosSorteados, RodadasExtra) VALUES (?, ?)
    """ # Comando SQL que insere uma nova linha na tabela apostas
    numeros_str = ",".join(map(str, numeros_sorteados))  # Converte a lista de números em uma string
    db_manager.execute_non_query(query, (numeros_str, rodadas_extra)) # Executa a linha de código SQL

