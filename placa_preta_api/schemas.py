from pydantic import BaseModel
from typing import Optional

#|-------------------------------------------------------------------------------------------------------------------------------------------------CRUD-DEFINIR-CAMPOS|
#definir o schema base, os campos de CRUD
class CarroBase(BaseModel):
    marca: str
    modelo: str
    ano: int
    quilometragem: int
    preco: float
    url_foto: Optional[str] = None  #campo opcional

class CarroCreate(CarroBase):
    pass

class Carro(CarroBase):
    id: int

#essa config diz ao pydantic para ler os dados mesmo que eles venham de um objeto do sql alchemy (orm) e não de um dicionário do python
    class Config:
        orm_mode = True

#|-------------------------------------------------------------------------------------------------------------------------------------------------SCHEMA-PATCH-(MANIPULACAO-DE-ALTERACOES)|
#schema para quando for atualizar os dados, modificar apenas aqueles que foram manipulados, ou seja, os que não sofrerem alterações se manterem

class CarroUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None
    quilometragem: Optional[int] = None
    preco: Optional[float] = None
    url_foto: Optional[str] = None

#manter a config do orm
    class Config:
        orm_mode = True
