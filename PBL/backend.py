from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # CORS must be applied after the correct 'app' is defined


# In-memory structures
CARTS = {}
ORDERS = []
COUPONS = {
    "FIRST20": {
        "condition": lambda total, user: total > 0 and user not in [o['user'] for o in ORDERS],
        "discount": lambda total: total * 0.20
    },
    "SAVE10": {
        "condition": lambda total, user: total >= 300,
        "discount": lambda total: total * 0.10
    },
    "FLAT100": {
        "condition": lambda total, user: total >= 1000,
        "discount": lambda total: 100
    }
}
ITEM_COUNT = defaultdict(int)

@app.route("/submit_order", methods=["POST"])
def submit_order():
    data = request.get_json()
    user = data.get("user")
    cart = data.get("cart")

    if not user or not cart:
        return jsonify({"success": False, "message": "Missing user or cart"}), 400

    for item in cart:
        ITEM_COUNT[item['name']] += item['quantity']

    ORDERS.append({"user": user, "cart": cart})
    return jsonify({"success": True, "message": "Order placed"})

@app.route("/validate_coupon", methods=["POST"])
def validate_coupon():
    data = request.get_json()
    code = data.get("code", "").upper()
    total = float(data.get("total", 0))
    user = data.get("user")

    if code not in COUPONS:
        return jsonify({"valid": False, "message": "Invalid coupon"})

    rule = COUPONS[code]
    if not rule["condition"](total, user):
        return jsonify({"valid": False, "message": "Coupon conditions not met"})

    discount = round(rule["discount"](total), 2)
    return jsonify({"valid": True, "discount": discount, "message": f"Coupon {code} applied. You saved ₹{discount}"})

@app.route("/most_added_items", methods=["GET"])


def most_added_items():
    sorted_items = sorted(ITEM_COUNT.items(), key=lambda x: x[1], reverse=True)
    return jsonify(sorted_items[:5])
#@app.route("/all_orders", methods=["GET"])
#def all_orders():
   # return jsonify(ORDERS)

if __name__ == "__main__":
    app.run(debug=True)
