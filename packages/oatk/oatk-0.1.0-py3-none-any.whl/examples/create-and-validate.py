from oatk import OAuthToolkit

# create token

oauth = OAuthToolkit()
oauth.with_private("private_key.pem")
oauth.with_public("public_key.pem")

oauth.claims(hello="world")

token = oauth.token
oauth.validate(token)

jwks = oauth.jwks

# validate use case

oauth2 = OAuthToolkit()
oauth2.with_jwks(jwks)
oauth2.validate(token)

# or as a chained one-liner
OAuthToolkit().with_jwks(jwks).validate(token)

