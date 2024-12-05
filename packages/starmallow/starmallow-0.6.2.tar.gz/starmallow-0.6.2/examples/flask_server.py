import tempfile
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from enum import Enum

import orjson
from flask import Flask
from flask import json as flask_json
from flask.views import MethodView
# from flask_compress import Compress
from flask_smorest import Api, Blueprint
from marshmallow_dataclass import dataclass as ma_dataclass

default_flask_config = {
    'OPENAPI_VERSION': '3.0.3',
    'OPENAPI_URL_PREFIX': '/doc',
    'OPENAPI_JSON_PATH': '/openapi.json',
    'OPENAPI_SWAGGER_UI_PATH': '/swagger',
    'OPENAPI_SWAGGER_UI_URL': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/',
    'OPENAPI_REDOC_PATH': '/redoc',
    'OPENAPI_REDOC_URL': 'https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.min.js',

    'JWT_ALGORITHM': 'RS256',
    'JWT_IDENTITY_CLAIM': 'sub',
    'JWT_USER_CLAIMS': 'claims',
}


class FlaskJSONEncoder(flask_json.JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'

    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        elif is_dataclass(obj):
            return asdict(obj)
        elif isinstance(obj, Enum):
            return obj.name
        return flask_json.JSONEncoder.default(self, obj)


app = Flask(__name__)
app.config.update(default_flask_config)
app.config['API_TITLE'] = __name__
app.config['API_VERSION'] = 'v1'
app.json_encoder = FlaskJSONEncoder
api = Api(app)

blp = Blueprint("root", "root")


@ma_dataclass
class CreateRequest:
    my_string: str
    my_int: int = 5


@ma_dataclass
class CreateResponse:
    my_string: str


@blp.route('/test2')
class Test2(MethodView):

    @blp.arguments(schema=CreateRequest.Schema)
    @blp.response(status_code=200, schema=CreateResponse.Schema)
    def put(self, create_request: CreateResponse):
        print(create_request)

        return asdict(create_request)


@blp.route('/tmp_file')
class TempFile(MethodView):

    @blp.arguments(schema=CreateRequest.Schema)
    @blp.response(status_code=200, schema=CreateResponse.Schema)
    def put(self, create_request: CreateResponse):
        with tempfile.TemporaryFile('wb') as f:
            f.write(orjson.dumps(create_request))

        # time.sleep(1)

        return asdict(create_request)


api.register_blueprint(blp)
