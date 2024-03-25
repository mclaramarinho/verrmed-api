import datetime
import uuid
from typing import List
from fastapi import APIRouter, Body, Depends
from starlette.responses import JSONResponse
from db import DBCollection
from models.models import GetAllResponse
from fastapi.requests import Request
from models.update_models import PutResponse, PutDrugBody
from router.utils.api_keys import get_api_key, get_update_key
from router.utils.responseDocs import get_response_doc
from router.utils.pagination import pagination, handle_500_response

router = APIRouter()


@router.get('/all', responses=get_response_doc('drugs'))
async def get_all_drugs(req: Request, count: int | None = None, page: int | None = None, api_key: str = Depends(get_api_key)):
    try:
        database = DBCollection(req.url.path)
        col = database.collection
        r = pagination(count, page, col)
        if r.code == 200:
            return GetAllResponse(content=r.content, totalElements=r.total_elements, elementsPerPage=r.items_per_page,
                                  currentPage=r.current_page, totalPages=r.total_pages, firstPage=r.first_page,
                                  lastPage=r.last_page)

        else:
            return JSONResponse(status_code=r.code, content={'message': r.message})

    except Exception as e:
        return handle_500_response(e)


@router.get('/{name}', responses=get_response_doc("drugsByName"))
async def get_drug_by_name(name: str, req: Request, count: int | None = None, page : int | None = None, api_key: str = Depends(get_api_key)):
    try:
        database = DBCollection(req.url.path)
        col = database.collection

        r = pagination(count, page, col, filter={'produto.nomeComercial': name})

        if r.code == 200:
            return GetAllResponse(content=r.content, totalElements=r.total_elements, elementsPerPage=r.items_per_page,
                                  currentPage=r.current_page, totalPages=r.total_pages, firstPage=r.first_page,
                                  lastPage=r.last_page)
        else:
            return JSONResponse(status_code=r.code, content={'message': r.message})

    except Exception as e:
        return handle_500_response(e)


@router.post('/update', responses=get_response_doc("drugsUpdate"))
async def update_drugs(req: Request, body: List[PutDrugBody] = Body(...), api_key: str = Depends(get_update_key)):
    print("requested")
    try:
        database = DBCollection(req.url.path)
        col = database.collection

        del_count = 0
        cre_count = 0
        mod_count = 0
        print(body)
        for item in body:
            item = {k: v for k, v in item if v is not None}
            key_list = item.keys()
            print(item)
            upd = col.update_one(filter={'idProduto': item['idProduto']},
                                update={"$set": item}, upsert=False)
            if upd.matched_count > 0:
                mod_count += 1
            else:

                if (('principiosAtivos' in key_list) and('viaAdministracao' in key_list) and ('formaFisica' in key_list)
                        and ('lab' in key_list)):

                    doc = {
                        '_id': str(uuid.uuid4()),
                        'idProduto': item['idProduto'],
                        'nomeComercial': item['nomeComercial'],
                        "numeroRegistro": item['numeroRegistro'],
                        'lab': item['lab'],
                        "numeroProcesso": item['numeroProcesso'],
                        'principiosAtivos': item['principiosAtivos'],
                        'categoriaRegulatoria': item['categoriaRegulatoria'],
                        'viaAdministracao': item['viaAdministracao'],
                        "formaFisica": item['formaFisica'],
                        "lastUpdate": datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                    }
                    if 'excipientes' not in doc.keys():
                        if 'excipientes' in key_list:
                            doc['excipientes'] = item['excipientes']
                        else:
                            doc['excipientes'] = []
                    cre = col.insert_one(doc)
                    if cre.inserted_id is not None:
                        cre_count += 1

        database.register_update()

        r = PutResponse(deletedCount=del_count, modifiedCount=mod_count, createdCount=cre_count)

        return r
    except Exception as e:
        print(e)
        return handle_500_response(e)

