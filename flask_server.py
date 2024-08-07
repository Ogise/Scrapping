from flask import Flask, request, jsonify

app = Flask(__name__)

deals = []

@app.route('/add_deal', methods=['POST'])
def add_deal():
    deal = request.get_json()
    deals.append(deal)
    return jsonify({"message": "Deal added successfully!"}), 201

@app.route('/deals', methods=['GET'])
def get_deals():
    return jsonify(deals)

@app.route('/')
def index():
    html = "<h1>Deals</h1><ul>"
    for deal in deals:
        html += f"<li><b>{deal['title']}</b><br>Regular Price: {deal['regular_price']}<br>Price: {deal['price']}<br>Promo Discount: {deal['promo_discount']}<br>Promo Code: {deal['promo_code']}<br><img src='{deal['image']}' width='100'><br><a href='{deal['product_link']}'>Buy Now</a><br>ASIN: {deal['asin']}</li><br><br>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    app.run(debug=True)
