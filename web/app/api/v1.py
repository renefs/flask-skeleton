from flask import Flask, Blueprint
import flask_restful

API_VERSION_V1 = 1
API_VERSION = API_VERSION_V1

example_api_v1_bp = Blueprint('api_v1', __name__)
example_api_v1 = flask_restful.Api(example_api_v1_bp)


class HelloWorld(flask_restful.Resource):
    def get(self):
        return {
            'hello': 'world',
            'version': API_VERSION,
        }

example_api_v1.add_resource(HelloWorld, '/hello')
