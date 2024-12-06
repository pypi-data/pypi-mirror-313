import logging
logger = logging.getLogger(__name__)

import time
import random
import string
import uuid
import json

from flask import request, session, redirect
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt

from . import server
from .db import db

@server.route("/", methods=["GET", "POST"])
def home():
  """
  The root/home page allows a user to login (POST) and manage its clients.
  Nothing OAuth to see here, just to server's own functionality.
  From this page a link to the /oauth/create-cient route is provided.
  """
  if request.method == "POST":
    username = request.form.get("username")
    user = db["users"].find_one({"username" : username})
    if not user:
      user = { "username": username, "_id" : str(uuid.uuid4()) }
      db["users"].insert_one(user)
    session["id"] = user["_id"]
    return redirect("/")

  # GET
  user = current_user()
  if user:
    clients = list(db["clients"].find({"user_id" : user["_id"]}))
    for client in clients:
      client["_id"] = str(client["_id"]) # turn Mongo ObjectID into string
    return render_template("home.html", user=user, clients=clients)
  else:
    return render_template("login.html")

@server.route("/oauth/create-client", methods=["GET", "POST"])
def create_client():
  """
  The Create Client page allows a user to create a new client registration.
  Client registration is required for an external application to interact and
  act on behalf of our user.
  In itself also no real OAuth shizzle here. Just administrative functionality.
  """
  user = current_user()
  if not user:
    return redirect("/")

  if request.method == "GET":
    return render_template(
      "create_client.html", client_id=gen_salt(24), client_secret=gen_salt(48)
    )

  # POST
  form = request.form
  try:
    db["clients"].insert_one({
      "client_id"           : form["client_id"],
      "user_id"             : user["_id"],
      "client_id_issued_at" : int(time.time()),
      "client_secret"       : form["client_secret"],
      "metadata" : {
        "client_name"               : form["client_name"],
        "client_uri"                : form["client_uri"],
        "grant_types"               : split_by_crlf(form["grant_type"]),
        "redirect_uris"             : split_by_crlf(form["redirect_uri"]),
        "response_types"            : split_by_crlf(form["response_type"]),
        "scope"                     : form["scope"],
        "allowed-origins"           : split_by_crlf(form["allowed_origins"]),
        "permission_groups"         : split_by_crlf(form["permission_groups"])
      }
    })
  except Exception as ex:
    logger.exception("failed to register client")
  return redirect("/")

@server.route("/oauth/authorize", methods=["GET", "POST"])
def authorize():
  """
  The first real OAuth route, and the first to hit in the flow. The application
  redirects the browser here to receive back an authoriation code. If the user
  isn't logged in yet, she will have to do so first. When logged in, she can
  effectively authorize the application to handle on its behalf.
  """
  if request.method == "POST":
    logger.info("processing post to auth route")
    username = request.form.get("username")
    logger.info(f"got {username}")
    if username:
      user = db["users"].find_one({"username" : username})
      logger.info(f"found user in db: {user}")
      if user:
        session["id"] = user["_id"]

  client_id = request.args["client_id"]
  scope     = request.args["scope"]

  # retrieve client for user
  user = current_user()
  logger.info(f"current_user: {user}")
  if user:
    client = db["clients"].find_one({
      "user_id"   : user["_id"],
      "client_id" : client_id
    })
    assert scope == "openid profile"
    assert request.args["response_type"] == "code"
    nonce = request.args["nonce"]
    logger.info(f"got client: {client}")
  else:
    return render_template("login.html", args=str(request.query_string.decode()))

  if "confirm" in request.form:
    logger.info("got confirmation: f{request.form['confirm']}")
    if request.form["confirm"]:
      logger.info("get positive confirmation... redirecting with code...")
      redirect_uri = client["metadata"]["redirect_uris"][0]
      code = generate_token()
      db["codes"].insert_one({
        "code"         : code,
        "client_id"    : client["client_id"],
        "user_id"      : client["user_id"],
        "redirect_uri" : redirect_uri,
        "scope"        : "openid"
      })
      goto = f"{redirect_uri}?code={code}"
      logger.debug(goto)
      return redirect(goto, 302)

  try:
    grants = client["metadata"]["grant_types"]
    assert "authorization_code" in grants
    grant = {
      "client"  : { "client_name" : client["metadata"]["client_name"] },
      "request" : { "scope"       : scope }
    }
  except Exception as error:
    logger.exception(error)
    return jsonify({"error" : str(error)})
  return render_template("authorize.html", grant=grant)

@server.route("/oauth/token", methods=["POST"])
def issue_token():
  try:
    code = db["codes"].find_one({"code" : request.json["code"] })
    client = db["clients"].find_one({
      "user_id"   : code["user_id"],
      "client_id" : code["client_id"]
    })
    user = db["users"].find_one({"_id" : code["user_id"]})
    username = user["username"]

    now = round(time.time())
    token = {
      "iat"              : now,
      "exp"              : now + 300,
      "auth_time"        : now,
      "jti"              : str(uuid.uuid4()),
      "iss"              : request.url_root.rstrip("/"),
      "sub"              : f"f:{str(uuid.uuid4())}:{client['metadata']['client_name']}",
      "typ"              : "Bearer",
      "azp"              : "development",
      "nonce"            : "nonce-TODO",
      "session_state"    : "52ad15e0-4afb-4b04-8897-8e08b262a73d",
      "acr"              : "0",
      "allowed-origins"  : client["metadata"]["allowed-origins"],
      "scope"            : "openid profile permission_groups",
      "sid"              : "52ad15e0-4afb-4b04-8897-8e08b262a73d",
      "permission_groups": client["metadata"]["permission_groups"],
      "username"         : username
    }
    
    encoded = server.oatk.claims(token).token
    return {
      "access_token": encoded,
      "expires_in": 300,
      "refresh_expires_in": 0,
      "token_type": "Bearer",
      "id_token": "TODO:id_token",
      "not-before-policy": str(time.time()),
      "scope": "openid permission_groups profile"
    }

  except Exception as ex:
    logger.exception("failed to provide token")
  return {}


@server.route("/oauth/userinfo")
@server.oatk.authenticated_with_claims(scope="profile")
def api_me():
  logger.warn("TODO implement actual userinfo")
  return { "hello" : "world", "STILL": "TODO" }

@server.route("/oauth/certs")
def certs():
  return json.dumps(server.oatk.jwks, indent=2)

@server.route("/oauth/well-known")
def well_known():
  me = request.url_root.rstrip("/")
  return json.dumps({
    "issuer"                 : f"{me}",
    "jwks_uri"               : f"{me}/oauth/certs",
    "authorization_endpoint" : f"{me}/oauth/authorize",
    "token_endpoint"         : f"{me}/oauth/token",
    "userinfo_endpoint"      : f"{me}/oauth/userinfo",
    "end_session_endpoint"   : f"{me}/oauth/logout",
    "registration_endpoint"  : f"{me}/oauth/create-client",
  }, indent=2)

@server.route("/oauth/logout")
def logout():
  session.pop("id", None)
  goto = "/"
  return redirect(goto, 302)

# helper functions

def current_user():
  if "id" in session:
    uid = session["id"]
    return db["users"].find_one({"_id" : uid})
  return None

def split_by_crlf(s):
  return [v for v in s.splitlines() if v]

UNICODE_ASCII_CHARACTER_SET = string.ascii_letters + string.digits

def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
  rand = random.SystemRandom()
  return ''.join(rand.choice(chars) for _ in range(length))
