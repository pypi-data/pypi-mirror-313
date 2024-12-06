import os

from pymongo import MongoClient

connection_string = os.environ.get("MONGO_URL", "mongodb://localhost:27017/oatk")
server, db_name   = connection_string.rsplit("/", 1)
client            = MongoClient(server)
db                = client[db_name]






# https://github.com/lepture/authlib/blob/master/authlib/integrations/sqla_oauth2/client_mixin.py

# client = {
#   "id"
#   "user_id"
#   "user" : {
#     "id"
#     "username"
#     get_user_id
#     str
#   }
#
#   "client_id"
#   "client_secret"
#   "client_id_issued_at"
#   "client_secret_expires_at"
#   "client_metadata"
# }

# https://github.com/lepture/authlib/blob/master/authlib/integrations/sqla_oauth2/tokens_mixins.py

# code = {
#   "id"
#   "user_id"
#   "user" : {
#     "id"
#     "username"
#     get_user_id
#     str
#   }
#
#     "code"
#     "client_id"
#     "redirect_uri"
#     "response_type"
#     "scope"
#     "nonce"
#     "auth_time"
#     "code_challenge"
#     "code_challenge_method"
# }

# token = {
#   "id"
#   "user_id"
#   "user" : {
#     "id"
#     "username"
#     get_user_id
#     str
#   }
#
#     "client_id"
#     "token_type"
#     "access_token"
#     "refresh_token"
#     "scope"
#     "issued_at"
#     "access_token_revoked_at"
#     "refresh_token_revoked_at"
#     "expires_in"
# }
