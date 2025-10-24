from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


import schemas
import models
from database import SessionLocal, engine #importar o que foi feito anteriormente

#agora criar as tabelas no banco de dados: esta linha é importante pois cria as tabelas no banco de dados conforme as classes que criamos em models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#|-------------------------------------------------------------------------------------------------------------------------------------------------INICIO-CORS|
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #permite todos métodos
    allow_headers=["*"] #e permite todos cabeçalhos
)

#|-------------------------------------------------------------------------------------------------------------------------------------------------INICIO-BANCO-DE-DADOS|
'''a "dependencia" do banco de dados: esse é um conceito central do fastAPI, essa função get_db é uma dependência.
Ela cria uma sessão temporária com o banco de dados toda vez que uma rota precisar interagir com o banco de dados.
Ela abre a sessão, permite que a rota use essa sessão para fazer operações no banco de dados, e depois fecha a sessão quando a operação é concluída.'''
def get_db():
    db = SessionLocal()  #iniciar a sessão
    try:
        yield db  #devolver a sessão pro endpoint que chamou essa dependencia
    finally:
        db.close()  #fechar a sessão depois que o endpoint terminar de usar

#Root da concessionária
@app.get("/")
def ler_raiz():
    return {"mensagem": "Bem-vindo à API da Concessionária Placa Preta!"}

#|-------------------------------------------------------------------------------------------------------------------------------------------------CRUD-CREATE|
#agora vamos criar o C do CRUD: Create
@app.post("/carros/", response_model=schemas.Carro)
def criar_carro(
    carro: schemas.CarroCreate, 
    db: Session = Depends(get_db)
):
    
    db_carro = models.Carro(**carro.dict())

    #adicionar o carro no banco de dados em modo de "espera"
    db.add(db_carro)

    #sql da um INSERT no db
    db.commit()

    #atualizar o objeto carro com o id que o banco de dados gerou
    db.refresh(db_carro)

    #retorna o objeto db_carro criado
    return db_carro

#|-------------------------------------------------------------------------------------------------------------------------------------------------CRUD-READ|
#agora vamos criar o R do CRUD: Read

#rota para listar todos os carros
@app.get("/carros/", response_model=list[schemas.Carro])
def listar_carros(db: Session = Depends(get_db)):
    carros = db.query(models.Carro).all()
    return carros

#ler um carro determinado
@app.get("/carros/{carro_id}", response_model=schemas.Carro)
def ler_carro(
    carro_id: int,
    db: Session = Depends(get_db)
):
    #mudar o filtro: dessa forma pedimos para que retorne o carro com o id igual ao primeiro e único carro_id passado na url
    db_carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()

    if db_carro is None: #tratamento de erros: se não achar, ele retorna "Carro não encontrado"
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    #se achar, retorna o carro procurado
    return db_carro

#|-------------------------------------------------------------------------------------------------------------------------------------------------CRUD-UPDATE|
#agora vamos criar o U do CRUD: Update
@app.put("/carros/{carro_id}", response_model=schemas.Carro)
def atualizar_carro(
    carro_id: int,
    carro_atualizado: schemas.CarroCreate,
    db: Session = Depends(get_db)
):
    
#achar o carro que queremos modificar pelo id
    db_carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()

#se ele não existir, retornamos um erro tratado:
    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro não encontrado.")

#parte de atualizar o carro
    dados_para_atualizar = carro_atualizado.dict()

    for chave, valor in dados_para_atualizar.items():
        setattr(db_carro, chave, valor)

#inserir a mudança feita no objeto no banco:
    db.commit()

#atualizar para que o db tenha a mudança commitada
    db.refresh(db_carro)

#retornar o carro atualizado
    return db_carro

#setor de atualização parcial (schema patch >> schemas.py)
@app.patch("/carros/{carro_id}", response_model=schemas.Carro)
def atualizar_parcialmente_carro(
    carro_id: int,
    carro_atualizado: schemas.CarroUpdate,
    db: Session = Depends(get_db)
):
#localizar o carro a ser parcialmente modificado
    db_carro = db.query(models.Carro).filter(models.Carro).filter(models.Carro.id == carro_id).first()

#tratar erro caso carro não seja encontrado
    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro não localizado.")

#agora o tratamento real
    dados_para_atualizar = carro_atualizado.dict(exclude_unset=True) #(exclude_unset=True) diz para inserir apenas o que foi modificado, espaços não "tocados" serão mantidos

    for chave, valor in dados_para_atualizar.items():
        setattr(db_carro, chave, valor)

#salvar e voltar
    db.commit()
    db.refresh(db_carro)
    return db_carro

#|-------------------------------------------------------------------------------------------------------------------------------------------------CRUD-DELETE|
#agora vamos criar o D do CRUD: Delete
@app.delete("/carros/{carro_id}")
def deletar_carro(carro_id: int, db: Session = Depends(get_db)): #mesma lógica de achar um carro, mas agora pra deletar
    db_carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()

    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro não encontrado. Inserir um ID válido") #se não achar o carro por id, retorna esse erro

    db.delete(db_carro)
    db.commit()
    return {"mensagem": f"Carro ID {carro_id} deletado com sucesso."}

