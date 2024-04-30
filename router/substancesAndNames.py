import uuid

import pymongo
from fastapi import APIRouter, Body, Depends
from typing import List
from fastapi.requests import Request
from db import DBCollection
from router.utils.api_keys import get_api_key, get_update_key
from models.models import GetAllSubstancesRes
from models.update_models import PutBodySubstance, PutResponse
from fastapi.responses import JSONResponse
from router.utils.responseDocs import get_response_doc
from router.utils.pagination import pagination, handle_500_response

router = APIRouter()

@router.get(path="/getByName", responses=get_response_doc('subst'))
async def get_by_name(req: Request, name: str, count: int = None, page: int = None, api_key: str = Depends(get_api_key)):
    collection = DBCollection(req.url.path).collection
    r = pagination(count, page, collection, filter={'name': {'$regex': name}}, sort=[("name", pymongo.ASCENDING)])

    if r.code == 200:
        return GetAllSubstancesRes(content=r.content, totalElements=r.total_elements, elementsPerPage=r.items_per_page,
                                   currentPage=r.current_page, totalPages=r.total_pages, firstPage=r.first_page,
                                   lastPage=r.last_page)

    else:
        return JSONResponse(status_code=r.code, content={'message': r.message})



@router.get(path="/all", responses=get_response_doc('subst'))
async def get_all(req: Request, count: int = None, page: int = None, api_key: str = Depends(get_api_key)):
    collection = DBCollection(req.url.path).collection
    r = pagination(count, page, collection)

    if r.code == 200:
        return GetAllSubstancesRes(content=r.content, totalElements=r.total_elements, elementsPerPage=r.items_per_page,
                              currentPage=r.current_page, totalPages=r.total_pages, firstPage=r.first_page,
                              lastPage=r.last_page)

    else:
        return JSONResponse(status_code=r.code, content={'message': r.message})


@router.post(path='/update', responses=get_response_doc('substUpdate'))
async def update_all(req: Request, body: PutBodySubstance = Body(...), api_key: str = Depends(get_update_key)):
    database = DBCollection(req.url.path)
    collection = database.collection

    lista: List[str] = body.lista

    if len(lista) == 0:
        response = PutResponse(createdCount=0, deletedCount=0, modifiedCount=0)
        return response

    del_count = 0
    cre_count = 0
    exist_count = 0
    try:
        for name in lista:
            exists = collection.find_one({"name": name})
            print(name)
            if not exists:
                create = collection.insert_one({'_id': uuid.uuid4().__str__(), 'name': name})
                print(create.inserted_id)
                if create.inserted_id:
                    cre_count += 1
            else:
                exist_count += 1

        response = PutResponse(createdCount=cre_count, deletedCount=del_count, modifiedCount=exist_count)
        database.register_update()
        return response

    except Exception as e:
        return handle_500_response(e)
