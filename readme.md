---- INSTALAÇÃO DE DEPÊNDENCIAS DO PROJETO
    -- Instale o Python atraves do site https://www.python.org/downloads/
    -- pip install flask
    -- pip install pyodbc

---- INSTANCIAÇÃO DO BANCO DE DADOS
    -- Foi utilizado para a visualização do banco de dados o programa SQL Server Management Studio no qual é necessário conectar chamando o nome do serviodr de DESKTOP-XXXXXXX\SQLEXPRESS apenas trocando o nome do desktop como descrito no template de resolução utilizando o comando hostname no prompt. Posteriormente deve se criar um banco de dados chamado ITAcademyDell e criar dentro deste banco de dados as tabelas dbo.Aposta e dbo.Sorteio com tais scripts respectivamente.
    
    SELECT TOP (1000) [NumeroRegistro]
      ,[Nome]
      ,[CPF]
      ,[Numeros]
        FROM [ITAcademyDell].[dbo].[Aposta]
    
    SELECT TOP (1000) [SorteioID]
      ,[NumerosSorteados]
      ,[RodadasExtra]
        FROM [ITAcademyDell].[dbo].[Sorteio]

    Para visualizar o conteúdo das tabelas clique com o botão direito do mouse em cima da tabela deseja e pressione a opção "Selecionar 1000 linha superiores"

    -- Caso não consiga utilizar o banco de dados os sorteios não serão realizados na página WEB para isso as todas as informações serão impressas no terminal do VSCode.

---- EXECUÇÃO DO CÓDIGO
    -- Para executar o programa apenas clique na seta de executar ou use o comando "python main.py"