# auth.py
from flask import Flask, redirect, session, jsonify, url_for
from authlib.integrations.flask_client import OAuth
from jose import jwt
from flask import request, abort
import json
from urllib.request import urlopen
from flask import Flask, request, redirect, session
import os
# from six.moves.urllib.parse import urlencode

print(os.urandom(16))


import os

# # Use environment variables
# AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
# AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
# AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

app = Flask(__name__)
app.secret_key = b'\xfd\xa4\x8f\xea\x0eV\x17\xad\xde\x01\x02\xb9\x03\xc5\x86\xa0\x1c\xd3\x7f\xe8\x1a\xec\xe8'
  # Replace with a secret key

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='PxaSgxxgVo3Jbh3wICgXCZr67h2JZdeK',  # Replace with your Auth0 Client ID
    client_secret='6GwQdYHETa1lU0F_tLBOOtjAAe4AU0F4fcr-4N0A3r47Navd16N67z6QhN-WJocq',  # Replace with your Auth0 Client Secret
    api_base_url='https://dev-52g2mrlpglpuz2lf.eu.auth0.com',  # Replace with your Auth0 Domain
    access_token_url='https://dev-52g2mrlpglpuz2lf.eu.auth0.com/oauth/token',
    authorize_url='https://dev-52g2mrlpglpuz2lf.eu.auth0.com/authorize',
    jwks_uri='https://dev-52g2mrlpglpuz2lf.eu.auth0.com/.well-known/jwks.json',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/')
def home():
    return 'Welcome to the auth page. <a href="/login">Log In</a>'


# Auth0 Login
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/callback')  # Replace with your callback URL

# Auth0 callback handling
@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

# Dashboard route after successful login
@app.route('/dashboard')
def dashboard():
    # Redirect to the Gradio app URL after successful login
    return redirect("http://127.0.0.1:7860") 
 
# # Logout route
# @app.route('/logout')
# def logout():
#     session.clear()
#     params = {'returnTo': url_for('home', _external=True), 'client_id': 'your_auth0_client_id'}
#     return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


if __name__ == "__main__":
    app.run(port=5000)
