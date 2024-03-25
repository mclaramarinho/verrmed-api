from models.models import GetAllResponse, Error, GetAllSubstancesRes
from models.update_models import PutResponse

DESC_GET_ALL_SUBST_NAMES = f'''Get a list of all available, with name and id 
                            (id not related to Anvisa database). Any API key works here.'''

DESC_GET_ALL_DRUGS = 'Get a list with all drugs available in Verr Med\'s database.'

DESC_GET_DRUGS_BYNAME = '''Get a list with the drugs available in Verr Med\'s
                            database with the commercial name informed.'''

DESC_UPDATE_DRUGS = '''Pass a list of drugs to update and this endpoint will
                        update the existing drugs or create if it doesnt exist. 
                        You should use the specific update API Key here.'''

DESC_UPDATE_SUBST_NAMES = '''Update the available inactive substances by sending a list with all of them. 
                To perform this action, enter an update api key.'''


def get_response_doc(what, desc_401: str | None = None,
                     desc_404: str | None = None,
                     desc_406: str | None = None,
                     desc_500: str | None = None):

    desc_401 = "UNAUTHORIZED - If the x-api-key header is not informed or is invalid." if desc_401 is None else desc_401
    desc_404 = "NOT FOUND" if desc_404 is None else desc_404
    desc_406 = "NOT ACCEPTABLE - If the params are invalid." if desc_406 is None else desc_406
    desc_500 = "INTERNAL SERVER ERROR - If we run into any problems." if desc_500 is None else desc_500

    model_200 = None
    desc_200 = None

    if what == 'drugs':
        model_200 = GetAllResponse
        desc_200 = DESC_GET_ALL_DRUGS
    elif what == 'drugsByName':
        model_200 = GetAllResponse
        desc_200 = DESC_GET_DRUGS_BYNAME
    elif what == 'subst':
        model_200 = GetAllSubstancesRes
        desc_200 = DESC_GET_ALL_SUBST_NAMES
    elif what == 'drugsUpdate':
        model_200 = PutResponse
        desc_200 = DESC_UPDATE_DRUGS
    elif what == 'substUpdate':
        model_200 = PutResponse
        desc_200 = DESC_UPDATE_SUBST_NAMES

    return {
        200: {"model": model_200, "description": desc_200},
        401: {"model": Error, "description": desc_401},
        404: {"model": Error, "description": desc_404},
        406: {"model": Error, "description": desc_406},
        500: {"model": Error, "description": desc_500}
    }
