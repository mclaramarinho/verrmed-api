from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
from os import environ

load_dotenv()

API_KEYS = []


_api_key_header = APIKeyHeader(name="x-api-key")


UNAUTH_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key. Please talk to the devs."
    )


def set_api_keys_list():
    keys = environ.keys()
    for key in keys:
        if "_API_KEY_VERR_MED" in key:
            API_KEYS.append(environ.get(key))


def get_api_key(api_key_header: str = Security(_api_key_header)) -> str:
    set_api_keys_list()

    if api_key_header in API_KEYS:
        return api_key_header

    raise UNAUTH_ERROR


def get_update_key(api_key_header: str = Security(_api_key_header)) -> str:
    print(api_key_header)
    if api_key_header == environ['UPDATE_API_KEY_VERR_MED']:
        return api_key_header

    raise UNAUTH_ERROR
