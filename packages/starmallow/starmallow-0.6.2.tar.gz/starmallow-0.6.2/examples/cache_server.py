from multiprocessing import Value, Manager
from typing import Annotated, Optional

import hashlib
import marshmallow.fields as mf
from brotli_asgi import BrotliMiddleware
from marshmallow.validate import Range
from marshmallow_dataclass import dataclass as ma_dataclass
from starlette.middleware import Middleware
from starlette_context import middleware, plugins

from starmallow.applications import StarMallow
from starmallow.params import Body, Cookie, Header, Query


counter = Value('i', 0)
cache = Manager().dict()


app = StarMallow(
    title="My API",
    version="1.0.0",
    middleware=[
        # Order matters!
        Middleware(BrotliMiddleware, minimum_size=500),
        Middleware(
            middleware.ContextMiddleware,
            plugins=(
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin(),
            ),
        ),
    ],
)

@ma_dataclass
class CreateRequest:
    my_string: str
    my_int: int = 5


@ma_dataclass
class CreateResponse:
    my_string: str


@app.post('/test')
async def test(
    create_request: CreateRequest,
    limit: Annotated[int, Query()],
    offset: int = 0,
    offset2: int = Query(0, model=mf.Integer(validate=[Range(min=0, max=50)])),
    my_string: str = Body('foobar'),
    email: str = Body(..., model=mf.Email()),
    foobar: str = Header(...),
    preference: Optional[str] = Cookie(...),
) -> CreateResponse:
    with counter.get_lock():
        counter.value += 1

    print(counter.value)

    cache_key = hashlib.blake2b(f'{create_request}{limit}{offset}{offset2}{my_string}{email}{foobar}')
    if (cache_key in cache):
        return cache[cache_key]

    else:
        print(create_request)
        print(limit)
        print(offset)
        print(offset2)
        print(foobar)
        print(my_string)
        print(email)
        print(preference)

        cache[cache_key] = create_request

        return create_request

