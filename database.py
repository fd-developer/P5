#! /usr/bin/env python3
# coding: utf-8
from tkinter import messagebox 
import mysql.connector
from mysql.connector import Error
import json
import requests
from bs4 import BeautifulSoup
from api import *
import os.path


class Database():
    # This class is used to manage the database
    def __init__(self):
        self.c = False
        self.bdd = self.connect()
        self.bd_connected = self.bdd[0]
        self.cursor = self.bdd[1]

    def create_db(self):
        # CREATE DATABASE WITH CONNECT.JSON info
        # CONNECTION TO MYSQL SERVER WITH ROOT USER
        print("CreateDB ...")
        with open('ressources/connect.json') as f:
            self.key = json.load(f)

        try:
            self.connection = mysql.connector.connect(
                host=self.key["server"],
                user=self.key["loginroot"],
                password=self.key["passwordroot"])

            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                # added server, database, login ... data to scriptSQL
                print("Connected to Mysql Server ...")
                path = open('ressources/createdb.sql', 'rt')
                scriptSQL = path.read()
                scriptSQL = scriptSQL.replace("dbserver", self.key["server"])
                scriptSQL = scriptSQL.replace("database", self.key["database"])
                scriptSQL = scriptSQL.replace("dbuser", self.key["login"])
                scriptSQL = scriptSQL.replace(
                    "dbpassword", self.key["password"])
                print(scriptSQL)
                for reqsql in scriptSQL.split(";"):
                    sql = reqsql + ';'
                    if sql != ";":
                        try:
                            self.cursor.execute(sql)
                        except OSError as e:
                            print("Error while creating database", e)
                            pass
                self.cursor.close()

        except OSError as e:
            print("Error while connecting to MySQL", e)
            pass

    def connect(self):
        # OPEN DATABASE WITH CONNECT.JSON info
        self.verify_connect_exists()

        with open('ressources/connect.json') as f:
            self.key = json.load(f)

        try:
            self.connection = mysql.connector.connect(
                host=self.key["server"],
                database=self.key["database"],
                user=self.key["login"],
                password=self.key["password"])

            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.c = True
                print("Connected to database ...")

            return [self.connection, self.cursor]

        except Error as e:
            print("Error while connecting to MySQL", e)
            pass
        return ["", ""]

    def destroy_db(self):
        # Destroy database and user attached
        # Used when we need to init database from wconfig window
        with open('ressources/connect.json') as f:
            self.key = json.load(f)
        try:
            print("Destroy database " + self.key["database"])
            # We need to connect with root to destroy database and user
            self.disconnect()
            self.connection = mysql.connector.connect(
                host=self.key["server"],
                user=self.key["loginroot"],
                password=self.key["passwordroot"])

            if self.connection.is_connected():
                self.cursor = self.connection.cursor()

                try:
                    print("Drop database " + self.key["database"])
                    self.cursor.execute("DROP DATABASE IF EXISTS \
                        " + self.key["database"] + ";")
                    self.bd_connected.commit()
                except:
                    pass

                try:
                    print("Drop user " + self.key["login"])
                    self.cursor.execute("DROP USER IF EXISTS \
                        " + self.key["login"] + "@" + self.key["server"] + ";")
                    self.bd_connected.commit()
                except:
                    pass

                self.cursor.close()
                messagebox.showinfo(
                    "info", "La base de données a été supprimée. Elle sera" \
                    " recrée lors du prochain lancement de l'application ...")
                return True

        except IOError as e:
            print("Error while connecting to MySQL", e)
        return False

    def disconnect(self):
        # Close connection with database
        if (self.bd_connected.is_connected()):
            self.cursor.close()
            self.bd_connected.close()
            self.c = False
        print("Disconnected from database ...")

    def load_category(self):
        # Load categories from database
        mySql_select_query = """SELECT name from categorie order by name"""
        self.cursor.execute(mySql_select_query)
        record = self.cursor.fetchall()
        return record

    def load_substituted_products_from_local_db(self):
        # Load substituted product saved in database
        mySql_select_query = """SELECT code, name, nutriscoreG, \
            store, url, substitute from product \
            where product.substitute<>'' order by name"""
        self.cursor.execute(mySql_select_query)
        record = self.cursor.fetchall()
        data = []
        for e in record:
            dico = {}
            dico["code"] = e[0]
            dico["name"] = e[1]
            dico["nutriscoreG"] = e[2]
            dico["store"] = e[3]
            dico["url"] = e[4]
            dico["substitute"] = e[5]
            data.append(dico)
        return data

    def get_product_name(self, pCode):
        # Retrieve the name of a product from its code
        mySql_select_query = """SELECT name from product \
            WHERE product.code = \""""+pCode+"""\" """
        self.cursor.execute(mySql_select_query)
        product_name = self.cursor.fetchone()
        if (product_name is not None):
            return product_name[0]
        else:
            return "?"

    def get_nutriscore(self, pCode):
        # Retrieve the nutriscore of a product from its code
        mySql_select_query = """SELECT nutriscoreG from product \
            WHERE product.code = \""""+pCode+"""\" """
        self.cursor.execute(mySql_select_query)
        score = self.cursor.fetchone()
        if (score is not None):
            return score[0]
        else:
            return "?"

    def exists_category(self, pCateg):
        # test if a category exists in database
        mySql_select_query = """SELECT name from Categorie \
            WHERE Categorie.name = \""""+pCateg+"""\" """
        self.cursor.execute(mySql_select_query)
        res = self.cursor.fetchone()
        if (res is not None):
            return True
        else:
            return False

    def get_category_id(self, pCateg):
        # Retrieve the id of a category from its name
        mySql_select_query = """SELECT id from Categorie \
            WHERE Categorie.name = \""""+pCateg+"""\" """
        self.cursor.execute(mySql_select_query)
        res = self.cursor.fetchone()
        if (res is not None):
            return res[0]
        else:
            return 0

    def exists_product(self, pCode):
        # test if product exists in database
        mySql_select_query = """SELECT id from Product \
            WHERE Product.code = \""""+pCode+"""\" """
        self.cursor.execute(mySql_select_query)
        res = self.cursor.fetchone()
        if (res is not None):
            return True
        else:
            return False

    def insert_product_in_local_database(self, pProduct, pSubstitute):
        # Create a new product in database
        mySql_insert_query = """INSERT INTO product (code, name, \
            nutriscoreG, store, url, substitute) \
            VALUES (""""'" + pProduct.get('code', "") + "','" \
            + pProduct.get('name', "").replace("'", "''") + "','" \
            + pProduct.get('score', "").upper() + "','" \
            + pProduct.get('store', "").replace("'", "''")+"','" \
            + pProduct.get('url', "")+"','" \
            + pSubstitute + "'"") """
        print("\n", mySql_insert_query)
        self.cursor = self.bd_connected.cursor()
        self.cursor.execute(mySql_insert_query)
        self.bd_connected.commit()

    def update_substitut(self, pProduct, pSubstitute):
        # Update product substitut in database 
        mySql_update_query = """UPDATE product \
            set substitute = '""" + pSubstitute + "'" \
            """WHERE code = '""" + pProduct.get('code', "") + "'"
        print("\n", mySql_update_query)
        self.cursor = self.bd_connected.cursor()
        self.cursor.execute(mySql_update_query)
        self.bd_connected.commit()

    def insert_category(self, pCategory):
        # Create a new catogery in database
        mySql_insert_query = """INSERT INTO Categorie (name) \
            VALUES (""""'" + pCategory.replace("'", "''") + "'"") """
        print("\n", mySql_insert_query)
        self.cursor = self.bd_connected.cursor()
        self.cursor.execute(mySql_insert_query)
        self.bd_connected.commit()

    def insert_rel_product_categorie(
        # Create a new relation between product and category
        # in database
            self, id_product, id_categorie):
        mySql_insert_query = """INSERT INTO REL_Product_Categorie \
            (id_product, id_categorie) \
            VALUES ("""+str(id_product) + "," \
            + str(id_categorie) + ")"""""""
        print("\n", mySql_insert_query)
        self.cursor = self.bd_connected.cursor()
        self.cursor.execute(mySql_insert_query)
        self.bd_connected.commit()

    def get_product_url(self, pCode):
        # Retrieve the url of a product from its code
        mySql_select_query = """SELECT url from product \
            WHERE product.code = \"""" + pCode + """\" """
        self.cursor.execute(mySql_select_query)
        product_url = self.cursor.fetchone()
        if (product_url is not None):
            return product_url[0]
        else:
            return "_blank"

    def get_product_id(self, pCode):
        # Retrieve the id of a product from its code
        mySql_select_query = """SELECT id from product \
            WHERE product.code = \"""" + pCode + """\" """
        self.cursor.execute(mySql_select_query)
        product_id = self.cursor.fetchone()
        if (product_id is not None):
            return product_id[0]
        else:
            return 0

    def list_products_in_a_category(self, pCateg):
        # Search a list of product of a category from database
        print("Download products for "+pCateg+" from database ...")
        prods = []
        # Search for category ID
        mySql_select_query = """SELECT id from Categorie \
            WHERE Categorie.name = \"""" + pCateg + """\" """
        self.cursor.execute(mySql_select_query)
        category_id = self.cursor.fetchone()
        if (category_id is not None):
            # Search for products in the category
            # Adding each product to a dictionary

            mySql_select_query = """SELECT code, name, nutriscoreG, \
                store, url, substitute from \
                Product, REL_Product_Categorie \
                where product.id = REL_Product_Categorie.Id_Product and \
                REL_Product_Categorie.Id_Categorie = \
                """ + str(category_id[0]) + """ \
                order by Product.code"""
            self.cursor.execute(mySql_select_query)
            record = self.cursor.fetchall()
            for e in record:
                dico = {}
                dico["code"] = e[0]
                dico["name"] = e[1]
                dico["score"] = e[2]
                dico["store"] = e[3]
                dico["url"] = e[4]
                prods.append(dico)
        return prods

    def create_list_categories_from_api(self, pnbcateg):
        # Create a list of categories from openfoodfacts
        ap = Api()
        cpt = 0
        for category in ap.list_categories():
            print(category)
            if not self.exists_category(category):
                self.insert_category(category)
                cpt += 1
                if cpt == pnbcateg and pnbcateg != 0:
                    break
        return cpt

    def create_list_products_by_category_from_api(self):
        # Create a list of categorie's products from openfoodfacts
        ap = Api()
        cpt = 0

        mySql_select_query = """SELECT id, name from Categorie"""
        self.cursor.execute(mySql_select_query)
        record = self.cursor.fetchall()
        for category in record:
            list_products = ap.list_products_in_a_category(category[1])
            for product in list_products:
                print(category[1] + " / " + product["code"])
                if not self.exists_product(product["code"]):
                    self.insert_product_in_local_database(product, "")
                    self.insert_rel_product_categorie(
                        self.get_product_id(product["code"]), category[0])
                    cpt += 1
        return cpt

    def verify_connect_exists(self):
        # Verify if connect.json file exists. If no, we create it
        if not os.path.isfile('ressources/connect.json'):
            dico = {}
            dico["server"] = ""
            dico["database"] = ""
            dico["login"] = ""
            dico["password"] = ""
            dico["loginroot"] = ""
            dico["passwordroot"] = ""
            dico["nbcateg"] = 0
            with open("connect.json", "x") as f:
                json.dump(dico, f)

    @property
    def connected(self):
        return self.c
