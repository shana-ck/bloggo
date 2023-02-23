from flask import Flask, request
from flask_smorest import abort
from db import stores, details
import uuid

app = Flask(__name__)



@app.route("/")
def home():
    return "hello flask"

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "first" not in item_data
        or "store_id" not in item_data
        or "second" not in item_data
    ):
        abort(400, message="Bad request. Ensure 'first', 'second', and 'store_id' are included in the JSON payload.")
    for item in details.values():
        if (
            item_data["first"] == item["first"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item already exists.")
        
    if item_data["store_id"] not in stores:
        abort(404, message="Item not found.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    details[item_id] = item
    return item, 201

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")

@app.get("/store/<string:item_id>")
def get_items(item_id):
    try:
        return details[item_id]
    except KeyError:
        return {"message": "Store not found"}, 404