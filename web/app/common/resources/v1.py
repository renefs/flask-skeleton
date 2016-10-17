from flask import Flask, Blueprint
import flask_restful

from marshmallow_jsonapi import Schema, fields
from marshmallow import validate

API_VERSION_V1 = 1
API_VERSION = API_VERSION_V1

example_api_v1_bp = Blueprint('api_v1', __name__)
example_api_v1 = flask_restful.Api(example_api_v1_bp)


class HelloWorldSchema(Schema):
    id = fields.Str(dump_only=True)
    hello = fields.String()
    version = fields.Integer()

    class Meta:
        type_ = 'hello_world'


class HelloWorld(flask_restful.Resource):
    def get(self):
        api_info = dict(hello='world', version=API_VERSION)
        schema = HelloWorldSchema()
        result = schema.dump(api_info)
        return result

example_api_v1.add_resource(HelloWorld, '/hello')
