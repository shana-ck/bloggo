import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import details

blp = Blueprint("details", __name__, description="Operations on details")

@blp.route("/item/<string:item_id>")
class item(MethodView):
    def get(self, item_id):
        try:
            return details[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del details[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        if "first" not in item_data or "second" not in item_data:
            abort(400, message="Bad request, make sure 'first' and 'second' are included in the JSON payload.")

        try:
            item=details[item_id]
            item |= item_data
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(details.values())}
    
    def post(self):
        item_data = request.get_json()
        if "name" not in item_data:
            abort(400, message="Bad request. Make sure 'name' is in JSON payload.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        details[item_id] = item
        return item, 201
        
    