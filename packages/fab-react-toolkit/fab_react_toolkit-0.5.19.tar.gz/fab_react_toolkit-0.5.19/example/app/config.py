import os

from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_OAUTH,
)

basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "../app.db")
# SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
# SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

# ------------------------------
# GLOBALS FOR APP Builder
# ------------------------------
APP_NAME = "FAB React Toolkit Example"
WEBAPP = False
# Uncomment to setup Setup an App icon
# APP_ICON = "/static/img/logo.jpg"

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
# AUTH_OAUTH : Is for OAuth
AUTH_TYPE = AUTH_DB

FAB_REACT_CONFIG = {'foo': 'bar'}

# Uncomment to setup Full admin role name
AUTH_ROLE_ADMIN = 'Admin'

# Disable the FAB Add security views
FAB_ADD_SECURITY_VIEWS = True

# Uncomment to setup Public role name, no authentication needed
# AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
# AUTH_USER_REGISTRATION = True

# The default user self registration role
# AUTH_USER_REGISTRATION_ROLE = "Public"

# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# REDIRECT_URI = "http://localhost:6006/"
# OAUTH_PROVIDERS = [
#     {
#         "name": "google",
#         "icon": "fa-google",
#         "token_key": "access_token",
#         "remote_app": {
#             "client_id": "CLIENTID",
#             "client_secret": "CLIENTSECRET",
#             "api_base_url": "https://www.googleapis.com/oauth2/v2/",
#             "client_kwargs": {"scope": "email profile"},
#             "request_token_url": None,
#             "access_token_url": "https://accounts.google.com/o/oauth2/token",
#             "authorize_url": "https://accounts.google.com/o/oauth2/auth",
#             "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
#         },
#     },
# ]

# Uncomment to setup OpenID providers example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = "en"
# Your application default translation path
BABEL_DEFAULT_FOLDER = "translations"
# The allowed translation for you app
LANGUAGES = {
    "en": {"flag": "gb", "name": "English"},
}

# Session Cookie settings
SESSION_COOKIE_SECURE = True
# Use "Strict" for maximum security but it breaks the OAuth workflow
SESSION_COOKIE_SAMESITE = "Lax"