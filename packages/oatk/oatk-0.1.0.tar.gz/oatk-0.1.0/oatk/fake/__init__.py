import logging
logger = logging.getLogger(__name__)

from flask import Flask
from flask_cors import CORS
import flask_restful

import json
from datetime import datetime

class OATKFlask(Flask):
  def __init__(self, *args, **kwargs):
    Flask.__init__(self, *args, **kwargs)
    self._oatk = None

  @property
  def oatk(self):
    return self._oatk

  @oatk.setter
  def oatk(self, o):
    self._oatk = o
    from . import routes # since our routes refer to server.oath ;-)

server = OATKFlask(__name__)
CORS(server, resources={r"*": {"origins": "*"}})
api = flask_restful.Api(server)

server.secret_key = "sikrit" # to enable sessions

class Encoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, datetime):
      return o.isoformat()
    if isinstance(o, set):
      return list(o)
    return super().default(o)

server.config['RESTFUL_JSON'] =  {
  "indent" : 2,
  "cls"    : Encoder
}
