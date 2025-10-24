from sqlalchemy import Column, Integer, String, Float
from database import Base #base criada no outro arquivo "database.py"

#criar uma classe chamada carro que herda da base carro que criamos, o sql alchemy vai usar isso pra criar a tabela carro no banco de dados
class Carro(Base):
    __tablename__ = 'carros'  #nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True)  #coluna id, chave primaria
    marca = Column(String, index=True)  #coluna marca
    modelo = Column(String, index=True)  #coluna modelo
    ano = Column(Integer, index=True)  #coluna ano
    quilometragem = Column(Integer, index=True)  #coluna quilometragem
    preco = Column(Float, index=True)  #coluna preço
    url_foto = Column(String, nullable=True)  #coluna url da foto que o nullable=true indica que essa coluna pode ficar vazia