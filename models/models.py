from pydantic import BaseModel, Field
from typing import List
import uuid


class Drug(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")

    idProduto: int = Field(...)
    nomeComercial: str = Field(...)
    numeroRegistro: str = Field(...)
    lab: str = Field(...)
    numeroProcesso: str = Field(...)
    principiosAtivos: List[str] = Field(...)
    categoriaRegulatoria: str = Field(...)
    viaAdministracao: str = Field(...)
    formaFisica: str = Field(...)
    ultimo_update_anvisa: str = Field(...)
    excipientes: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                '_id': "60f7bb2f-bbb1-4b49-b3c3-5f1b2e42791e",
                'idProduto': 'ID DO PRODUTO NA ANVISA',
                'nomeComercial': 'NOME COMERCIAL DO PRODUTO',
                "numeroRegistro": 'NUM DO REGISTRO NA ANVISA',
                'lab': 'Nome do laboratorio',
                "numeroProcesso": 'num do processo na anvisa',
                'principiosAtivos': ['Lista de principios ativos'],
                'categoriaRegulatoria': 'Generico',
                'viaAdministracao': 'oral',
                "formaFisica": 'capsula gelatinosa',
                'ultimo_update_anvisa': 'isodate do ultimo update na anvisa',
                'excipientes': ['Lista de excipientes identificados']
            }
        }


class Substance(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "60f7bb2f-bbb1-4b49-b3c3-5f1b2e42791e",
                "name": "NOME DA SUBSTANCIA ATIVA",
            }
        }


class GetAllSubstancesRes(BaseModel):
    content: List[Substance] = Field(...)
    totalElements: int = Field(..., alias='totalElements')
    elementsPerPage: int = Field(...)
    currentPage: int = Field(...)

    totalPages: int = Field(...)
    lastPage: bool = Field(...)
    firstPage: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "content": [{'_id': '123-90ejakldnas93109as=d', "name": 'nome substancia'}],
                "totalElements": 100,
                "totalPages": 4,
                "last": False,
                "first": True,
                "elementsPerPage": 25,
                "currentPage": 1
            }
        }


class GetAllResponse(BaseModel):
    content: List[Drug | None] = Field(...)
    totalElements: int = Field(..., alias='totalElements')
    elementsPerPage: int = Field(...)
    currentPage: int = Field(...)

    totalPages: int = Field(...)
    lastPage: bool = Field(...)
    firstPage: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "content": [{
                    '_id': "60f7bb2f-bbb1-4b49-b3c3-5f1b2e42791e",
                    'idProduto': 'ID DO PRODUTO NA ANVISA',
                    'nomeComercial': 'NOME COMERCIAL DO PRODUTO',
                    "numeroRegistro": 'NUM DO REGISTRO NA ANVISA',
                    'lab': 'Nome do laboratorio',
                    "numeroProcesso": 'num do processo na anvisa',
                    'principiosAtivos': ['Lista de principios ativos'],
                    'categoriaRegulatoria': 'Generico',
                    'viaAdministracao': 'oral',
                    "formaFisica": 'capsula gelatinosa',
                    'ultimo_update_anvisa': 'isodate do ultimo update na anvisa',
                    'excipientes': ['Lista de excipientes identificados']
                }],
                "totalElements": 100,
                "totalPages": 4,
                "last": False,
                "first": True,
                "elementsPerPage": 25,
                "currentPage": 1
            }
        }


class Error(BaseModel):
    message: str
