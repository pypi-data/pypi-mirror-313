from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_cors import CORS

from oatk import OAuthToolkit

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

oatk = OAuthToolkit()
oatk.with_private("private_key.pem")
oatk.with_jwks("certs.json")

@app.route("/")
@oatk.authenticated
def hello_world():
  return "<p>Hello, World!</p>"

class HelloWorld(Resource):
  @oatk.authenticated_with_claims(username="xtof")
  def get(self):
    return {"hello": "world"}

api.add_resource(HelloWorld, "/api/hello")

class Token(Resource):
  def get(self):
    claims = {}
    for claim, value in request.args.items():
      if "," in value:
        value = value.split(",")
      claims[claim] = value
    token = oatk.claims(**claims).token
    return Response(response=token, status=200, mimetype="plain/text")

api.add_resource(Token, "/api/token")
