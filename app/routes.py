from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from flask import request, render_template, redirect, url_for
import requests
import json

@app.route('/')
@app.route('/index')
def index():
    opinion1 = Opinion()
    return str(opinion1)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ProductForm()
    if request.method == 'POST' and form.validate():
        product = Product(request.form['productId'])
        respons = requests.get(product.opinionsPageUrl())
        if respons.status_code == 200:
            product.extractProduct()
            product.exportProduct()
            return redirect(url_for('product', productId=product.productId))
        else:
            form.productId.errors.append("For given productId there is no product")
    return render_template('extract.html', form=form)

@app.route('/product/<productId>')
def product(productId):
    pass

@app.route('/products')
def products():
    pass

@app.route('/author')
def author():
    pass