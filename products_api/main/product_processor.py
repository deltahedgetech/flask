from products_api.config import Config

import json
import pandas as pd
import sqlite3


class ProductProcessor:
    TABLE_COLUMNS = ", ".join(Config.PRODUCT_COLUMNS)

    @staticmethod
    def get_product_by_id(product_id):
        """
        Method to retrieve product by id
        :param product_id:int
        :return:dataframe
        """
        clause = f' WHERE id = "{product_id}"'
        return ProductProcessor.pandas_read_db(ProductProcessor.build_query_select(clause))

    @staticmethod
    def get_cheapest_products(products_limit):
        """
        Method to retrieve N cheapest products
        :param products_limit: int
        :return:
        """
        clause = f' WHERE price IS NOT NULL ORDER BY price ASC LIMIT {products_limit}'
        return ProductProcessor.pandas_read_db(ProductProcessor.build_query_select(clause))

    @staticmethod
    def build_query_select(clause):
        """
        Method that builds simple query string for selects
        :param clause:
        :return:
        """
        return 'SELECT ' + ProductProcessor.TABLE_COLUMNS + ' FROM ' + Config.PRODUCTS_TABLE + clause

    @staticmethod
    def pandas_read_db(query_string):
        """
        Method that queries the database
        :param query_string: str
        :return: json string
        """
        db = sqlite3.connect(Config.PRODUCTS_DB)
        return ProductProcessor.df_to_json(pd.read_sql_query(query_string, db))

    @staticmethod
    def df_to_json(df):
        """
         :param df: dataframe
        :return: json
        """
        return json.loads(df[Config.PRODUCT_COLUMNS].to_json(orient='index'))
