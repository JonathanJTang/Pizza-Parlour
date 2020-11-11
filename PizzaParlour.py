from flask import Flask, jsonify, request
from jsonschema import ValidationError, validate

import data_formats
from cart import Cart
from order import Order

app = Flask("Assignment 2")

orders = {}
next_order_no = 1


@app.route('/pizza', methods=["GET", "POST"])
def welcome_pizza():
    """ We will put order to server or get the current order from server
    in order to modify it."""
    try:
        if request.method == "GET":  # We want to change
            print("Got GET request")
            request.args.get("name")
        elif request.method == "POST":
            print("Got POST request")
            # request.files.
    except Exception:
        pass  # fail silently for now
    return 'Welcome to Pizza Planet!'


@app.route('/api/orders', methods=["POST"])
def create_order():
    """Receive an order made by a client."""
    global next_order_no
    current_order_no = next_order_no
    next_order_no += 1
    new_cart = Cart()

    try:
        order_data = request.get_json(silent=True)
        if order_data is None or order_data.get(
                "data_format") not in ("json_tree", "csv"):
            raise ValidationError()
        # Otherwise, we got a JSON object we can try to call validate() on
        if order_data["data_format"] == "json_tree":
            validate(order_data, data_formats.order_schema_json_tree)
            print("JSON validation success")
            # TODO: use JSON parser to resolve products in
            # order_data["products"] to the cart
        elif order_data["data_format"] == "csv":
            validate(order_data, data_formats.order_schema_csv)
            # TODO: use CSV parser to add the products in
            # order_data["products"] to the cart
    except ValidationError as err:
        print(err)
        print("JSON validation failed")
        return "No valid JSON payload", 400
    except Exception as err:
        print(err)
        return "An error occurred on the server", 500

    orders[current_order_no] = Order(current_order_no, new_cart)
    response = {"order_no": current_order_no,
                "total_price": new_cart.get_total_price()}
    return jsonify(response)


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def edit_order(order_id):
    return order_id


if __name__ == "__main__":
    app.run()
