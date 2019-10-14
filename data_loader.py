from products_api.config import Config

import logging
import numpy as np
import pandas as pd
import sqlite3
import sys

logging.basicConfig(level=logging.DEBUG)


class ProductLoader:

    def __init__(self, db_name, table_name, csv_file, json_file):
        self.db_name = db_name
        self.table_name = table_name
        self.csv_file = csv_file
        self.json_file = json_file

    def create_db(self):
        """
        Method that create a database
        :param :
        :return:
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
        except Exception as e:
            logging.error("Exception occurred in create_db", e, exc_info=True)
        else:
            logging.info(f"{self.db_name} db created")
        finally:
            if conn:
                conn.close()

    def pandas_read_json(self):
        """
        Method that uses pandas to read json data into a dataframe
        :param self
        :return: dataframe
        """
        try:
            df = pd.read_json(self.json_file)
        except Exception as e:
            logging.error("Exception occurred in pandas_read_json", e, exc_info=True)
        else:
            rows, cols = df.shape
            logging.info(f"Products data read from s3 {rows} by {cols}")
            return df

    def pandas_read_csv(self):
        """
        Method that uses pandas to read csv data into a dataframe
        :param self
        :return:dataframe
        """
        try:
            df = pd.read_csv(self.csv_file)
        except Exception as e:
            logging.error("Exception occurred in pandas_read_csv", e, exc_info=True)
        else:
            rows, cols = df.shape
            logging.info(f"Products data read from file {rows} by {cols}")
            return df

    def persist_database(self, df):
        """
        Method that uses pandas to_sql function to write data to a database
        :param df:
        :return:
        """
        conn = sqlite3.connect(self.db_name)
        try:
            df.to_sql(Config.PRODUCTS_TABLE, con=conn, if_exists='replace', chunksize=10000)
        except Exception as e:
            logging.error("Exception occurred in persist_database", e, exc_info=True)
        else:
            rows, cols = df.shape
            logging.info(f"Products inserted into db {rows} by {cols}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def clean_up_products_data(df):
        """
        Method that cleans up and normalises product data
        :param df: dataframe
        :return: dataframe
        """
        df = df.replace('"', '', regex=True)
        df = df.applymap(lambda x: x.lstrip() if isinstance(x, str) else x)
        df.columns = [col.lstrip().lower() for col in df.columns]
        df['price'] = df['price'].replace('', np.nan).replace('None', np.nan).astype(float)
        df.rename(columns={"instock": "in_stock"}, inplace=True)
        df['in_stock'] = df['in_stock'].replace('no', False).replace('n', False).replace('yes', True).replace('y', True)
        return df[Config.PRODUCT_COLUMNS]

    @staticmethod
    def concat_dataframes(df1, df2):
        """
        Method that concatenates two dataframes
        Note that it might be advisable to persist the two files sepately
        :param df1:
        :param df2:
        :return: dataframe
        """
        return pd.concat([df1, df2], axis=0)

    def run(self):
        """
        Method which orchestrates the db creation, data load and persistence
        :return:
        """
        df1 = self.clean_up_products_data(self.pandas_read_json())
        df2 = self.clean_up_products_data(self.pandas_read_csv())
        self.persist_database(self.concat_dataframes(df1, df2))


if __name__ == '__main__':
    # Need to refactor - total hack.
    if len(sys.argv) == 2:
        PRODUCTS_DB = sys.argv[1] + Config.PRODUCTS_DB
    else:
        PRODUCTS_DB = Config.PRODUCTS_DB
    logging.info('Running product loader job')
    ProductLoader(PRODUCTS_DB, Config.PRODUCTS_TABLE, Config.PRODUCTS_CSV, Config.S3_PRODUCTS_URL).run()
