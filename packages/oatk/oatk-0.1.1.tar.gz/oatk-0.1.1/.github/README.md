# OAuthToolKit

> A collection of useful functions for dealing with OAuth

[![Latest Version on PyPI](https://img.shields.io/pypi/v/oatk.svg)](https://pypi.python.org/pypi/oatk/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/oatk.svg)](https://pypi.python.org/pypi/oatk/)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.8.0-blue.svg)](https://github.com/christophevg/pypi-template)

## Installation

Minimal survival command...

```
% pip install oatk
```

## Rationale and Overview

Federated login using OAuth/OpenIDConnect/... is a de facto standard for authenticating and authorizing users nowadays. You simply don't want to deal with them in your application at all. The underlying principle is simple: have someone you trust tell you that you can trust a user and get your own personal token that proves you're operating for that user when accessing other resources, who can validate this token with the trusted authenticating party.

<p align="center">
  <img alt="Oauth Flow Conceptually" src="../media/oauth-flow-conceptually.png" width="400">
</p>

This OAuthTooKit brings together very basic implementations of several aspects of this flow, aiming to have this up and running quickly in a development context, without the hassle of setting up a full-fletched OAuth server or having to go through many hoops in configuring an existing service to accept your application and users.

In a nutshell, the toolkit contains:

* a Python module to create and validate tokens
* a Flask route decorator to validate tokens
* a Javascript client-library to handle an OAuth flow using PKCE
* a "fake" OAuth server
* a command line tool to work with all the functionality

Essentially, the toolkit allows 

... running a fake OAuth server ...

```console
% oatk server run
```

... creating a protected API ...

```python
from flask import Flask
from flask_restful import Resource, Api

from oatk import OAuthToolkit

app = Flask(__name__)
api = Api(app)

oatk = OAuthToolkit()
oatk.with_jwks("certs.json")

class HelloWorld(Resource):
  @oatk.authenticated_with_claims(username="xtof")
  def get(self):
    return {"hello": "world"}

api.add_resource(HelloWorld, "/api/hello")
```

... and access it with an authenticated user ...

```html
<script src="oatk.js"></script>
<script>
  oatk.with_authenticated(function(user, http){
    // at this point, the user is authenticated and we have an object with his
    // information...
    console.log(oatk.user)
  
    // ... and a way to get and post with his authenticating token:
    http.get("http://localhost:5001/api/hello", function(response) {
      console.log("authenticated response", response);
    });
  });
</script>
```

And now you can focus on your actual application functionality ;-)

Okay ... why not use a fancy-pants, big and bloathed "de facto standard" library or framework? Because initially I want to understand what I'm doing, to be able to make it work. Later, given this working and understood setup, through refactoring such 3rd party solution can be incorporated - if needed, since most of my works ends at the proof-of-concept-phase anyway ;-)

The toolkit therefore aims to be completely transparant, implementing maybe only a small "happy" path, taking you straigth from point A to B. You can read all code and easily understand it and implement the basics.

## Before we start...

You need a private key pair:

```console
% openssl genrsa -out private_key.pem 2048
Generating RSA private key, 2048 bit long modulus
.................................................................+++
..+++
e is 65537 (0x10001)

% openssl rsa -in private_key.pem -outform PEM -pubout -out public_key.pem
writing RSA key
```

> You know the drill: keep your private key safe!

## Using the CLI

Let's see what the toolkit has to offer from the command line.

With our public key, we can generate a JSON Web Key Set (JWKS), which is the typical format to publish our public key:

```console
% oatk with_public public_key.pem jwks | tee certs.json
{
  "keys": [
    {
      "n": "43CteJFzpZAa_h2-HFKCgTGTzdguocBE4FgxlqDgQdxIzD4-hTAQ3JXuu2OLt1AcDgvT5MNEJtbQzsXtbpC_HajcC5o0S-PKtZaqA-KZwNEPlL_Fi1WIb6paoJsk7k_C4q1ZBvqrMF2pLz7pgUOeXdZ6_6FiXacIrhmmSvjWOIqjcIC8SAApsxI4gjNHKp2TubTYbw6gxicFVvDk_kA1pSUdOotRD1v0mweLMkZMHORLgcajne0GulQlDuFADAFILS4tAz5BWV6zIJnS2W1Tv8zy_g_Y2N9NoN3tbn4ii7PSZgZzVbRy3bgry6EiuMC4RcPdM5AlPL29s354vPUttQ",
      "e": "AQAB",
      "kty": "RSA",
      "alg": "RS256",
      "kid": "5171a100-e4c8-49ed-94af-6bc8fa635368"
    }
  ]
}
```

With this information out in the open, we can now create tokens that can be validated:

```console
% oatk with_private private_key.pem with_jwks certs.json claims '{ "hello" : "world" }' token | tee token.txt
eyJhbGciOiJSUzI1NiIsImtpZCI6IjUxNzFhMTAwLWU0YzgtNDllZC05NGFmLTZiYzhmYTYzNTM2OCIsInR5cCI6IkpXVCJ9.eyJoZWxsbyI6IndvcmxkIn0.03XJ4MrNhhoB9ouQ6oPBehR9iSZxYUhfgZ2j0YV-_vqyBDwDV26GR0wpxhxrPu7XfnbeIRyqO8qFL_WKk6tn_32F7aMYdfK6lKtqRHIkTLDux4GtzXkpqHAuQPBZdD5W4xfrBbDQ6ItHwptMP_wVwuN0OQaR3X8Lz2UNpy3FWuMpJBbfPaaV8_E62plMIKOd92CHuafSgFOZOQMsvmxWCz-ylG2Kh4Kc77_CoDJABYsI2VbDK9bNG3C3x3oNH1KylDvmvtSgapQjhewFiYgvjVJWAMtU22TX_27BUGwbnMwni42jsJoHsI9GpQmd-IVtOnMA0wigd1A4xATfGBQF3Q
% cat token.txt | pbcopy
% oatk with_jwks certs.json from_clipboard validate
% oatk with_jwks certs.json from_file token.txt validate
% oatk from_file token.txt decode
hello: world
```

## Module

The command line tool is in fact a [fired-up](https://github.com/google/python-fire) version of the OAuthToolkit class. So everything we just did looks exactly the same...

```pycon
>>> from oatk import OAuthToolkit
>>> oauth = OAuthToolkit()
>>> oauth.with_private("private_key.pem")
<oatk.OAuthToolkit object at 0x1014c3760>
>>> oauth.with_jwks("certs.json")
<oatk.OAuthToolkit object at 0x1014c3760>
>>> oauth.claims({"hello" : "world"})
<oatk.OAuthToolkit object at 0x1014c3760>
>>> token = oauth.token
>>> token
'eyJhbGciOiJSUzI1NiIsImtpZCI6IjUxNzFhMTAwLWU0YzgtNDllZC05NGFmLTZiYzhmYTYzNTM2OCIsInR5cCI6IkpXVCJ9.eyJoZWxsbyI6IndvcmxkIn0.03XJ4MrNhhoB9ouQ6oPBehR9iSZxYUhfgZ2j0YV-_vqyBDwDV26GR0wpxhxrPu7XfnbeIRyqO8qFL_WKk6tn_32F7aMYdfK6lKtqRHIkTLDux4GtzXkpqHAuQPBZdD5W4xfrBbDQ6ItHwptMP_wVwuN0OQaR3X8Lz2UNpy3FWuMpJBbfPaaV8_E62plMIKOd92CHuafSgFOZOQMsvmxWCz-ylG2Kh4Kc77_CoDJABYsI2VbDK9bNG3C3x3oNH1KylDvmvtSgapQjhewFiYgvjVJWAMtU22TX_27BUGwbnMwni42jsJoHsI9GpQmd-IVtOnMA0wigd1A4xATfGBQF3Q'
>>> oauth.validate(token)
>>> oauth.decode(token)
{'hello': 'world'}
```

> All methods of the OAuthToolkit class return the object itself. This enables chaining method calls, which is mostly for nicer command line support ;-)

The `examples/create-and-validate.py` example presents this functionality in a ready to run format:

```console
PYTHONPATH=. python examples/create-and-validate.py
```

And no output means good output in this case ;-)

### A validating decorator for Flask routes

The OAuthToolkit class also provides a convenient way to decorate Flask routes. Take a look at `examples/web.py`:

```python
from flask import Flask, request, Response
from flask_restful import Resource, Api

from oatk import OAuthToolkit

app = Flask(__name__)
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
```

It's a more elaborate version from the one presented above in the rationale. It adds a plain Flask route and also a Token resource. We can now request a token and use it. First launch the web application...

```console
 % gunicorn examples.web:app
[2022-10-15 13:32:29 +0200] [84085] [INFO] Starting gunicorn 20.1.0
[2022-10-15 13:32:29 +0200] [84085] [INFO] Listening at: http://127.0.0.1:8000 (84085)
[2022-10-15 13:32:29 +0200] [84085] [INFO] Using worker: sync
[2022-10-15 13:32:29 +0200] [84099] [INFO] Booting worker with pid: 84099
```

... and then call it:
- first to get a token with a claim `username=xtof`
- then call the Flask route, which requires any authenticated user
- then call the Flask-RESTful route, which requires the username=xtof claim

```console
% curl -s "http://localhost:8000/api/token?username=xtof" | pbcopy

% curl http://localhost:8000/ -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUxNzFhMTAwLWU0YzgtNDllZC05NGFmLTZiYzhmYTYzNTM2OCIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Inh0b2YifQ.Yh6EiNFzOcldoqXLi7TyFannS4LGt05v_XhKDbW8MrKR3VgbH-ZpueSNO3A_Esrupz1cIpEBfNWCnw8JaUjQhOOIt47teQI5RejQtRm8bply93DovLlPsE5Fu5gjiATYBj6KA6Hlg1MDRYOsifN4LTQoSXwcWiKo-OIl-iapFDAwkrgv9SQLexslKKuhTqLSI8PLh0jL32GLZCVULsPNs7Eqrm_-HozwMIPKyN6uX0MNt2eQiBy3BtWmL5ElX6MtbP-mz2B186VKFwpmncdEOKmy72cup77WbVOhJt8ml-XO5kDh2UPQqri6HLIS4mPuQi0cCKbLbpyoHmhGHEVNcA"
<p>Hello, World!</p>
                                                      
% curl http://localhost:8000/api/hello -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUxNzFhMTAwLWU0YzgtNDllZC05NGFmLTZiYzhmYTYzNTM2OCIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Inh0b2YifQ.Yh6EiNFzOcldoqXLi7TyFannS4LGt05v_XhKDbW8MrKR3VgbH-ZpueSNO3A_Esrupz1cIpEBfNWCnw8JaUjQhOOIt47teQI5RejQtRm8bply93DovLlPsE5Fu5gjiATYBj6KA6Hlg1MDRYOsifN4LTQoSXwcWiKo-OIl-iapFDAwkrgv9SQLexslKKuhTqLSI8PLh0jL32GLZCVULsPNs7Eqrm_-HozwMIPKyN6uX0MNt2eQiBy3BtWmL5ElX6MtbP-mz2B186VKFwpmncdEOKmy72cup77WbVOhJt8ml-XO5kDh2UPQqri6HLIS4mPuQi0cCKbLbpyoHmhGHEVNcA"
{"hello": "world"}
```

With any other token, or no token, the calls fail...

```console
% curl -s "http://localhost:8000/api/token?username=notxtof" | pbcopy

% curl http://localhost:8000/api/hello -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUxNzFhMTAwLWU0YzgtNDllZC05NGFmLTZiYzhmYTYzNTM2OCIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im5vdHh0b2YifQ.mjkspQOyUm1yMimd2CMkRsMO-O5Yrrm4B7v32_dJYhYOFnsqcwLD3fD0LBa3kxLsUaSRutdj8Q7PtRyKXmpLxBcW6N7LoIaCqHHVuy8fAiP74bDfSZ5UbXUFE1xmesipCEf_1XyNUiIuHWmariv5Auzfs4iV_VpQLG2qdz09zEDKMZ2_mpjv2PCX6hPRlv7iwmDyp8SZ2gin8QnN3ZW4D5Ki7i3jeHK4eUcVxdy1OZPkUWisbbFbrkjqBxLmio2l2jkImhhHSq8dHB6O9rk7Etel9FTCXhhxE-RRR-l8ygoMXLjMmYrKqJfLPMWulv7w7Mat_TPWcJ5b4IF_meII3Q"
ValueError("claim username hasn't required value")% 

% curl http://localhost:8000
Missing Authorization%      
```

## Fake Server

The toolkit includes a fake OAuth server that allows testing applications you build without the need for a full-fletched setup. The fake server implements a minimum flow with little real blocking aspects, and allows you to focus on your application, not the OAuth flow by itself ;-)

The server runs by default as `http://localhost:5000` and essentially provides the following service routes:

<dl>
  <dt>/oauth/well-known</dt>
  <dd>returning a well-known configuration set, with all other URLs of service routes it offers, as described by the following - so you only need to configure this one.</dd>
  <dt>/oauth/certs</dt>
  <dd>providing the (public) key(s) that can be used to validate signatures in JSON Web Key Set (JWKS) format.</dd>
  <dt>/oauth/authorize</dt>
  <dd>used to obtain an authorization code from the authenticated end user</dd>
  <dt>/oauth/token</dt>
  <dd>used to exchange an authorization code for an access token</dd>
  <dt>/oauth/userinfo</dt>
  <dd>provides a user information record, given an access token</dd>
</dl>

These service routes enable the following OAuth workflow between your application and an OAuth server:

1. get the `well-known` configuration
2. (optionally) get the `jwks_uri`, with public key(s)
3. visit the `authorization_endpoint`, providing a `client_id`, `scope`, `response_type`, a `redirect_uri` and `nonce`. 
4. after succesfull authorization, you're redirected to your `redirect_uri` (if it was previously registered as an acceptable one), along with a `code` query parameter, containing your authorization code.
5. post to the `token_endpoint` with JSON fragment containing `grant_type` ("authorization_code") and a `code` (containing the obtained code)
6. the response is a JSON fragment containing an `access_token`.
7. get the `userinfo_endpoint` with the `access_token` as a `Bearer` `Authorization` header

Visually:

![Oauth Flow Visually](../media/oauth-flow-visually.png)

### Bringing everything together...

Let's fire up our fake OAuth server, our minimal web API and create a web application to interact with the user.

> The root-level Makefile contains targets that automate the require command line instructions. Make will also output these, so you can inspect what is done for you on the first line of the output.

```console
% make server
python -m oatk with_private private_key.pem with_jwks certs.json server run
 * Serving Flask app 'oatk.fake'
 * Debug mode: off
[2022-10-15 16:23:31 +0200] [werkzeug] [INFO] WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
[2022-10-15 16:23:31 +0200] [werkzeug] [INFO] Press CTRL+C to quit
```

```console
% make app
gunicorn -b 0.0.0.0:5001 -k eventlet -w 1 examples.client.app:server
[2022-10-15 16:15:26 +0200] [98606] [INFO] Starting gunicorn 20.1.0
[2022-10-15 16:15:26 +0200] [98606] [INFO] Listening at: http://0.0.0.0:5001 (98606)
[2022-10-15 16:15:26 +0200] [98606] [INFO] Using worker: eventlet
[2022-10-15 16:15:26 +0200] [98620] [INFO] Booting worker with pid: 98620
```

```console
% make api
gunicorn -b 0.0.0.0:5002 -k eventlet -w 1 examples.web:app
[2022-10-15 16:26:13 +0200] [99984] [INFO] Starting gunicorn 20.1.0
[2022-10-15 16:26:13 +0200] [99984] [INFO] Listening at: http://0.0.0.0:5002 (99984)
[2022-10-15 16:26:13 +0200] [99984] [INFO] Using worker: eventlet
[2022-10-15 16:26:13 +0200] [99998] [INFO] Booting worker with pid: 99998
```

Three servers are up and running now:

1. the fake OAuth server on [http://localhost:5000](http://localhost:5000)
2. the web application on [http://localhost:5001](http://localhost:5001)
3. the api application on [http://localhost:5002](http://localhost:5002)

We first visit the fake OAuth server to setup a user and a client registration:

<p align="center">
  <img alt="Step 1: Login/Signup" src="../media/step1.png" width="800">
</p>

Let's login/signup as `xtof`:

<p align="center">
  <img alt="Step 2: Logged in" src="../media/step2.png" width="800">
</p>

Now, create a client registration...

<p align="center">
  <img alt="Step 3: Create Client Registration" src="../media/step3.png" width="800">
</p>

The defaults are all set for this demo, so just submit them...

<p align="center">
  <img alt="Step 4: All set" src="../media/step4.png" width="800">
</p>

So we now have an OAuth server, with a user `xtof` and a client registration for an application known by the clientId `test`.

> If you hit the "log out" link now, you get back to the first screenshot. If you actually do this, in a few moments you'll have to log in again, else, since you're still logged in, you will see nothing really happen at first... ;-)

Our web application is very simple: it requires and authenticated user and once it has it, it calls our protected web API to say hello...

```html
<div id="app" style="display:none;">
  <a style="float:right" id="logout" href="#">logout</a>
  <h1>My App</h1>
  <div id="output"></div>  
</div>

<script src="static/jquery-3.6.1.min.js"></script>
<script src="http://localhost:5000/static/oatk.js"></script>
<script>
  oatk.with_authenticated_user(function(user, http, logout) {
    console.log("👩 user is authenticated...", user);
    $("#app").show();            // time to show the application
    $("#logout").click(logout);  // wire the logout action

    // call our API to say hello
    http.getJSON("http://localhost:5002/api/hello", function(result) {
      $("#output").text(JSON.stringify(result));
    });
  });
</script>
```

Let's visit it...

<p align="center">
  <img alt="Step 5: Login/Signup" src="../media/step5.png" width="800">
</p>

Did we go to the wrong server? No, our application redirected us to the (fake) OAuth server, based on its known configuration. It could get the URLs, but didn't have an authorization code, so it redirected to the authorization endpoint. And since we're not logged in, because we logged out earlier, we now have to log in again, as `xtof`.

<p align="center">
  <img alt="Step 6: Give consent" src="../media/step6.png" width="800">
</p>

We explicitly have to give consent for the application to use our information and act on our behalf. After that, we are again redirected to our application that now continues the OAuth flow...

<p align="center">
  <img alt="Step 7: Hello" src="../media/step7.png" width="800">
</p>

... and calls our API that requires authentication and authorization using our OAuth token.

> I've checked the console log preservation flag, to see the entire flow more clearly as it happens behind the scenes. You can see that upon returning to our app we now do have an authorization code, start another call to the server to exchange the code for a token, which results in a full set of URLs, code and token, so we can call our API and display the result.

## Google

The `examples/` folder contains another example, which is targetting Google as an authentication provider. The implicit flow is a little different, providing an access token (called `id_token`) immediately after logon and consent. The `id_token` kan be used as a JWT access token, yet it cannot be refreshed from the javascript client side.

> So for now, I use it to authenticate the user once and set up an application-level session.

The `examples/google/templates/home.html` file shows the minimal client-side HTML/javascript implementation:

```html
<div id="landing">
  <a id="login" href="#">login with google</a>
</div>

<div id="app" style="display:none;">
  <a style="float:right" id="logout" href="#">logout</a>
  <h1>My App</h1>
  <div id="output"></div>  
</div>

<script src="/static/jquery-3.6.1.min.js"></script>
<script src="/oatk.js"></script>
<script>
  oatk.using_provider("{{ OAUTH_PROVIDER }}");
  oatk.using_client_id("{{ OAUTH_CLIENT_ID }}");
  oatk.apply_flow("implicit");
  
  function show_landing() {
    $("#app").hide();
    $("#landing").show();    
  }
  
  function show_app() {
    $("#app").show();
    $("#landing").hide();
  }

  function login() {
    oatk.with_authenticated_user(function(user, http, logout) {
      console.log("👩 user is authenticated...", user);
      $("#logout").click(function() { logout(show_landing); });
      show_app();
      
      // call our API to say hello
      http.getJSON("http://localhost:8000/api/hello", function(result) {
        $("#output").text(JSON.stringify(result));
      }, function(result) {
        if(result.status == 403) {
          console.log(result);
          $("#output").text("You were authenticated by Google, yet you don't have the correct claims.");
        }
      });
    });
  }

  $("#login").click(login);
  
  if(oatk.have_authenticated_user()) {
    login();
  }
</script>
```

At the server-side of our application we need to:

- serve oatk.js from the package (e.g. using Flask)
- protect our endpoints with authorisation logic (e.g. using Flask_restful)

```python
from flask import Flask, render_template, Response
from flask_restful import Resource, Api

import oatk.js
from oatk import OAuthToolkit

server = Flask(__name__)

# route to load web app
@server.route("/", methods=["GET"])
def home():
  return render_template("home.html", **os.environ)

# route for oatk.js from the oatk package
@server.route("/oatk.js", methods=["GET"])
def oatk_script():
  return Response(oatk.js.as_src(), mimetype="application/javascript")

# API set up
api = Api(server)

# setup oatk
auth = OAuthToolkit()
auth.using_provider(os.environ["OAUTH_PROVIDER"]);
auth.with_client_id(os.environ["OAUTH_CLIENT_ID"])

def validate_name(name):
  return name == "Christophe VG"

class HelloWorld(Resource):
  @auth.authenticated_with_claims(name=validate_name)
  def get(self):
    return {"hello": "world"}

api.add_resource(HelloWorld, "/api/hello")
```

If you [register an application with Google](https://console.cloud.google.com/apis/dashboard) and add `localhost:8000` as a authorized Javascript source and redirect URL for the credentials, you can run the example using `gunicorn -k eventlet -w 1 examples.google.app:server`, which triggers the following flow:

<p align="center">
  <img alt="Step 1: request login" src="../media/google-step1.png" width="800">
</p>

<p align="center">
  <img alt="Step 2: authenticate and give consent (implicitly)" src="../media/google-step2.png" width="800">
</p>

<p align="center">
  <img alt="Step 3: show protected content" src="../media/google-step3.png" width="800">
</p>
