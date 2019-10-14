### Install Instructions

1. git clone https://github.com/deltahedgetech/flask.git
2. Run pip install virtualenv
3. Navigate to the products directory 
4. run virtualenv venv --python=python3.7
5. run pip install -r requirements.txt


### Run instructions
1. To read the products files and load the database, navigate to the products directory and run ./load_db.sh. 
Once completed a price.db will be created in the products_api directory.
2. To run Flask, navigate to products_api directory and run python app.py
3. A flask application should be running on http://127.0.0.1:5000


### Usage instructions
1. To find products by an id, http://127.0.0.1:5000/get_product_by_id/6067181
2. To find cheapest N products, http://127.0.0.1:5000/get_cheapest_products/5
2. A suite of test cases are available in the tests package

### Additional Information
1. I decided to use a database as I wanted to explore Pandas to_sql functionality. For more complex schemas, i would use
an ORM such as SQLAlchemy.
