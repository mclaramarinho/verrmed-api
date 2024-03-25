from pydantic import BaseModel, Field
from typing import Optional, List


class PutDrugBody(BaseModel):
    idProduto: Optional[int]
    nomeComercial: Optional[str]
    numeroRegistro: Optional[str]
    principiosAtivos: Optional[List[str]]
    categoriaRegulatoria: Optional[str]
    excipientes: Optional[List[str]]
    viaAdministracao: Optional[str]
    formaFisica: Optional[str]
    lab: Optional[str]
    numeroProcesso: Optional[str]
    ultimo_update_anvisa: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "idProduto": "ID DO PRODUTO NA ANVISA",
                "nomeComercial": "NOME COMERCIAL DO PRODUTO",
                "numeroRegistro": "NUM DO REGISTRO NA ANVISA",
                "principiosAtivos": ["Lista de principios ativos"],
                "genericoOuMarca": "Generico",
                "excipientes": ["Lista de excipientes identificados"],
                "concentracao": "50mg",
                "viaAdministracao": "oral",
                "formaFisica": "capsula gelatinosa",
                "empresa": "Nome do laboratorio",
                "numProcesso": "num do processo na anvisa",
                "last_anvisa_update": "iso string do ultimo update na anvisa",
            }
        }


class PutBodySubstance(BaseModel):
    lista: List[str] = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "lista": ["subst. 1", "name. 2"]
            }
        }


class PutResponse(BaseModel):
    createdCount: int = Field(...)
    deletedCount: int = Field(...)
    modifiedCount: int = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                'createdCount': 1,
                'deletedCount': 2,
                'alreadyExistedCount': 3
            }
        }


class UpdateStatsBody(BaseModel):
    time_spent: int = Field(...)
    tokens_spent: int = Field(...)
    success: bool = Field(...)
    page: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "time_spent": 123423,
                "tokens_spent": 12345123,
                "success": True,
                "page": '2'
            }
        }


class UpdatesResponseModel(BaseModel):
    id: str = Field(...)
    collection: str = Field(...)
    last_update: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "jifaiodjasopie9120-39i019ryaiosdjma",
                "collection": "drugs",
                "last_update": "2024-03-18T23:34:40Z"
            }
        }
