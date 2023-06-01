from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
cors = CORS(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api = Api(app)
api.add_resource(HelloWorld, '/')

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    return send_from_directory('static', 'swagger.json')

if __name__ == '__main__':
    app.run()
