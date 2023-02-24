from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"


api = Api(app)

@app.route("/")
def home():
    return "hello flask"

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)


