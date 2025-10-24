from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#1 - O endereço do banco de dados: estamos dizendo que vamos usar um banco sqlite  e que o arquivo dele se chamará concessionaria.db e ficará na mesma pasta do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./placa_preta.db"

#2 - O motor do sqlalchemy: peça principal que sabe como "conversar" com o banco de dados que foi especificado acima
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    
    #linha abaixo é uma config necessária apenas pro sqlite funcionar bem com o fastapi
    connect_args = {"check_same_thread": False}
    )

#3 - Iniciar sessão: quando formos alterar algo no banco de dados, não fazemos isso direto, iniciamos uma sessao temporária; abaixo criamos um modo de iniciar essas sessões:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#4 - Classe Base: de onde nossas classes vão herdar as configs para funcionarem como tabelas do banco de dados
Base = declarative_base()