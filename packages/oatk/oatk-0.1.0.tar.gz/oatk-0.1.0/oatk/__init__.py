__version__ = "0.1.0"

import logging
logger = logging.getLogger(__name__)

import json
import uuid

import jwt
from authlib.jose import jwk

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from functools import wraps
from flask import request, Response

import requests

from oatk import fake

try:
  from AppKit import NSPasteboard, NSStringPboardType
  pb = NSPasteboard.generalPasteboard()
except ModuleNotFoundError:
  logger.debug("No AppKit installed, so no MacOS clipboard support!")
  pb = None

class OAuthToolkit():
  def __init__(self):
    self._encoded     = None
    self._certs       = {}
    self._private_key = None
    self._public_key  = None
    self._alg         = "RS256"
    self._kid         = str(uuid.uuid4())
    self._claims      = {}
    self._client_id   = None
    
    self.server       = fake.server
    self.server.oatk  = self

  @property
  def version(self):
    return __version__

  def with_private(self, path):
    with open(path, "rb") as fp:
      self._private_key = serialization.load_pem_private_key(
        fp.read(),
        password=None,
        backend=default_backend()
      )
    return self

  def with_public(self, path):
    with open(path, "rb") as fp:
      self._public_key = serialization.load_pem_public_key(
        fp.read(),
        backend=default_backend()
      )
    self._certs = { self._kid : self._public_key }
    return self

  def using_provider(self, provider_url):
    try:
      config = json.loads(requests.get(provider_url).content)
    except:
      logger.exception("could not retrieve openid configuration")
      return
    try:
      self.with_jwks(requests.get(config["jwks_uri"]).content)
    except:
      logger.exception("could not import jwks")
      return
    logger.info(f"succesfully configured from {provider_url}")
    return self

  def with_client_id(self, client_id):
    self._client_id = client_id
    return self

  @property
  def jwks(self):
    return json.dumps({
      "keys" : [
        jwk.dumps(self._public_key, kty="RSA", alg=self._alg, kid=self._kid)
      ]
    }, indent=2)

  def with_jwks(self, path_or_string_or_obj):
    try:
      with open(path_or_string_or_obj) as fp:
        jwks = json.load(fp)
    except:
      try:
        jwks = json.loads(path_or_string_or_obj)
      except:
        jwks = path_or_string_or_obj
    assert isinstance(jwks, dict)
    self._certs = {
      key["kid"] : jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
      for key in jwks["keys"]
    }
    if jwks["keys"]:
      self._kid = jwks["keys"][0]["kid"]
    return self
  
  def from_clipboard(self):
    encoded = pb.stringForType_(NSStringPboardType)
    if encoded[:6] == "Bearer":
      encoded = clip[7:]
    self._encoded = encoded.strip() # strip to remove trailing newline
    return self

  def from_file(self, path):
    with open(path) as fp:
      self._encoded = fp.read().strip() # strip to remove trailing newline
    return self

  def header(self, token=None):
    if not token:
      token = self._encoded
    return jwt.get_unverified_header(token)

  def claims(self, claimsdict=None, **claimset):
    if claimsdict is None: claimsdict = {}
    self._claims = claimset
    self._claims.update(claimsdict)
    return self

  @property
  def token(self):
    if self._private_key:
      return jwt.encode(
        self._claims, self._private_key, algorithm=self._alg,
        headers={ "kid": self._kid, "alg" : self._alg }
      )
    return None

  def validate(self, token=None):
    kid = self.header(token)["kid"]
    alg = self.header(token)["alg"]
    if not token:
      token = self._encoded
    jwt.decode( token, self._certs[kid], algorithms=[alg], audience=self._client_id )

  def decode(self, token=None):
    if not token:
      token = self._encoded
    return jwt.decode( token, options={"verify_signature": False} )

  def execute_authenticated(self, f, required_claims=None, *args, **kwargs):
    code = 403
    msg  = ""
    try:
      token = request.headers["Authorization"][7:]
      self.validate(token)
      if required_claims:
        claims = self.decode(token)
        for claim, value in required_claims.items():
          if not claim in claims:
            raise ValueError(f"required claim {claim} is missing")
          if callable(value):
            if not value(claims[claim]):
              raise ValueError(f"claim {claim} doesn't match required criteria")
          elif type(value) == list:
            if not value in claims[claim]:
              raise ValueError(f"claim {claim} is missing required value")
          elif value != claims[claim]:
            raise ValueError(f"claim {claim} doesn't equal required value")
      # authenticated -> execute
      return f(*args, **kwargs)
    except KeyError as ex:
      msg = "Missing Authorization"
      code = 401
    except ValueError as e:
      msg = str(e)
      logger.warning(msg)
    except Exception as e:
      msg = repr(e)
      logger.warning(f"unexpected exception: {msg}")
    return Response(msg, code)

  def authenticated(self, f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      return self.execute_authenticated(f, *args, **kwargs)
    return wrapper

  def authenticated_with_claims(self, **required_claims):
    def decorator(f):
      @wraps(f)
      def wrapper(*args, **kwargs):
        return self.execute_authenticated(f, required_claims, *args, **kwargs)
      return wrapper
    return decorator
