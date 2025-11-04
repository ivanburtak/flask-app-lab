from . import products_bp

from flask import render_template, abort

products = [
    {"id": 1, "name": "Laptop", "description": "High-performance laptop for work and gaming.", "price": 1200},
    {"id": 2, "name": "Smartphone", "description": "Latest smartphone with amazing camera.", "price": 900},
    {"id": 3, "name": "Headphones", "description": "Noise-cancelling wireless headphones.", "price": 250}
]


@products_bp.route('/')
def get_products():
    return render_template("products.html", products=products)


@products_bp.route('/<int:id>')
def detail_product(id):
    if id > len(products) or id < 1:
        abort(404)
    product = products[id - 1]
    return render_template("detail_product.html", product=product)
