import math
from abc import ABC
from typing import Dict, Any, List, Union
from pymongo.collection import Collection
from starlette.responses import JSONResponse
from models.models import Drug, Substance


def handle_500_response(e: Exception):
    return JSONResponse(status_code=500, content={"message": 'We ran into an unexpected problem.', "details": e})


class PaginationResponse(ABC):
    code: int

    def __init__(self, status_code: int):
        self.code = status_code


class OKResponse(PaginationResponse):
    content: List[Union[Drug, Substance]]
    total_elements: int
    items_per_page: int
    current_page: int
    total_pages: int
    first_page: bool
    last_page: bool

    def __init__(self, code: int, content: List[Union[Drug, Substance]], total_elements: int,
                 items_per_page: int, current_page: int, total_pages: int, first_page: bool, last_page: bool):
        super().__init__(status_code=code)

        self.content = content
        self.total_elements = total_elements
        self.items_per_page = items_per_page
        self.current_page = current_page
        self.total_pages = total_pages
        self.first_page = first_page
        self.last_page = last_page


class NotOKResponse(PaginationResponse):
    message: str

    def __init__(self, code: int, msg: str):
        super().__init__(status_code=code)

        self.message = msg


def pagination(count: int, page: int, collection: Collection, filter: dict = None) -> Union[OKResponse, NotOKResponse]:
    f = {}
    if filter is not None and len(filter) > 0:
        f = filter

    try:
        total_elements = collection.count_documents(filter=f)
    except Exception as e:
        return NotOKResponse(code=406, msg=f"Error: {e}")

    items_per_page = 10
    content = []
    current_page = 0
    total_pages = 0
    first_page = False
    last_page = False

    if total_elements == 0:
        if count and count <= 50:
            items_per_page = count
        return OKResponse(code=200, content=content, total_elements=total_elements, items_per_page=items_per_page,
                          current_page=current_page, total_pages=total_pages, first_page=first_page, last_page=last_page)

    if count and count > 50:
        return NotOKResponse(code=406, msg='The maximum amount of items per page is 50.')

    if count and page:
        items_per_page = count
    elif (count and not page) or (not count and not page):
        current_page = 1
        if count:
            items_per_page = count

    total_pages = math.ceil(total_elements / items_per_page)

    if current_page > total_pages:
        return NotOKResponse(code=406, msg=f"This page does not exist. The last page is {total_pages}.")

    skip = (current_page * items_per_page) - items_per_page
    limit = (current_page * items_per_page) - skip

    c = list(collection.find(filter=f).skip(skip).limit(limit))

    for item in c:
        item['_id'] = str(item['_id'])

    content = c

    first_page = current_page == 1
    last_page = current_page == total_pages

    response = OKResponse(code=200, content=content, total_elements=total_elements,
                          items_per_page=items_per_page, current_page=current_page, total_pages=total_pages,
                          first_page=first_page, last_page=last_page)
    return response