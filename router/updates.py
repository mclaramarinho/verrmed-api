import datetime
import uuid
from fastapi import APIRouter, status, Depends, Body
from starlette.responses import JSONResponse
from db import db
from fastapi.requests import Request
from models.update_models import UpdateStatsBody, UpdatesResponseModel
from router.utils.api_keys import get_api_key, get_update_key

router = APIRouter()


@router.get('/medicamentos', status_code=status.HTTP_200_OK, response_model=UpdatesResponseModel)
def get_update_drugs(req: Request, api_key: str = Depends(get_api_key)):
    return return_update(req)


@router.get('/substanciasAtivas', status_code=status.HTTP_200_OK, response_model=UpdatesResponseModel)
def get_update_active(req: Request, api_key: str = Depends(get_api_key)):
    return return_update(req)


@router.get('/substanciasInativas', status_code=status.HTTP_200_OK, response_model=UpdatesResponseModel)
def get_update_inactive(req: Request, api_key: str = Depends(get_api_key)):
    return return_update(req)


@router.get('/nomesComerciais', status_code=status.HTTP_200_OK, response_model=UpdatesResponseModel)
def get_update_names(req: Request, api_key: str = Depends(get_api_key)):
    return return_update(req)


@router.post('/stats')
def set_latest_update_stats(req: Request, body: UpdateStatsBody = Body(...), api_key: str = Depends(get_update_key)):
    try:
        col = db['updateStats']
        now = datetime.datetime.now().isoformat() + 'Z'
        data = {
            '_id': uuid.uuid4().__str__(),
            'date': now,
            'totalTokens': body.tokens_spent,
            'totalTime': body.time_spent,
            'success': body.success,
            'page': body.page
        }

        cre = col.insert_one(data)

        if cre.inserted_id is not None:
            return JSONResponse(status_code=201, content={'message': "Update stats created successfully"})
        else:
            raise
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={'message': "We ran into an unexpected error."})


def return_update(req: Request):
    path = req.url.path
    col = db['updates']
    name = ''

    if 'nomesComerciais' in path: name = 'comName'
    elif 'substanciasInativas' in path: name = 'inactiveSubst'
    elif 'substanciasAtivas' in path: name = 'activeSubst'
    elif 'medicamentos' in path: name = 'drugs'

    res = col.find_one(filter={'collection': name})
    if res is not None:
        res['_id'] = str(res['_id'])
        response = UpdatesResponseModel(id=res['_id'], collection=res['collection'], last_update=res['last_update'])
        return response

    else:
        response = UpdatesResponseModel(id='none', collection='none', last_update='1980-03-21T18:36:10.989Z')
        return response