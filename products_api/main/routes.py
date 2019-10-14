from products_api.main.product_processor import ProductProcessor
from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/get_product_by_id/<string:product_id>')
def get_product_by_id(product_id):
    result = ProductProcessor.get_product_by_id(product_id)
    if result:
        return result, 200
    return jsonify({'message': "No matching records"}), 200


@main.route('/get_cheapest_products/<products_limit>')
def get_cheapest_products(products_limit):
    result = ProductProcessor.get_cheapest_products(products_limit)
    if result:
        return result, 200
    return jsonify({'message': "No records"}), 200
