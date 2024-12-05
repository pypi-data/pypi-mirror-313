import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA, IndexView as FABIndexView
from flask_cors import CORS
from fab_react_toolkit import FABReactToolkit, IndexView

import app.config

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, origins=["*"])
app.config.from_object(config)
db = SQLA(app)
appbuilder = AppBuilder(app=app, session=db.session, indexview=IndexView if app.config.get("WEBAPP") else FABIndexView)
fab_rtk = FABReactToolkit(appbuilder)

from . import  apis
