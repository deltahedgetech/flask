import os


class Config:
    SECRET_KEY = 'MY_SECRET_KEY'
    S3_PRODUCTS_URL = \
        'https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json'
    PRODUCTS_DB = 'price.db'
    PRODUCTS_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), 'products.csv'))
    PRODUCT_COLUMNS = ['id', 'name', 'brand', 'retailer', 'price', 'in_stock']
    PRODUCTS_TABLE = 'products'
