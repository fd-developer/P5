#! /usr/bin/env python3
# coding: utf-8

import json
import requests
from bs4 import BeautifulSoup


class Api():
    # This class is used to manage connexion with the
    # openfoodfacts api

    def list_categories(self):
        print("Download a list of categories from OpenFoodFacts ...")
        # Download a list of french categories from OpenFoodFacts.org

        # A first method using BeautifulSoup ...
        # requete = requests.get("https://fr.openfoodfacts.org/categories")
        # page = requete.content
        # soup = BeautifulSoup(page)#,'features="html.parser"')
        # categ = soup.find_all("a", {"class": "tag known"})
        # list_categ = [elt.string.strip() for elt in categ]
        # list_categ.sort()
        # print(list_categ)
        # return list_categ
        # had been replaced by a method using json ...

        url = 'https://fr.openfoodfacts.org/categories.json'

        headers = {
            'User-Agent': 'Student openclassrooms - project 5',
            'From': 'fd-mail@laposte.net'
        }
        requete = requests.get(url, headers=headers)
        page = requete.content
        parsed_json = json.loads(page)
        p = parsed_json['tags']
        i = 0
        list_categ = []
        while i < len(p):
            list_categ.append(p[i].get('name', ""))
            i += 1
        return list_categ

    def list_products_in_a_category(self, pCateg):
        # Ask an API from openfoodfacts to return a list of products
        # of a category
        print("Download products for " + pCateg + " from OFF ...")

        url = 'https://fr.openfoodfacts.org/cgi/search.pl?' \
            'action=process&tagtype_0=categories&tag_contains_0=contains' \
            '&tag_0=' + pCateg + "" \
            '&json=true&tag_1=&page_size=500'

        headers = {
            'User-Agent': 'Student openclassrooms - project 5',
            'From': 'fd-mail@laposte.net'
        }
        requete = requests.get(url, headers=headers)
        page = requete.content
        parsed_json = json.loads(page)
        p = parsed_json['products']
        i = 0
        prods = []
        while i < len(p):
            dico = {}
            dico["code"] = p[i].get('code', "")
            dico["name"] = p[i].get('product_name', "").replace("\\", "")
            dico["score"] = p[i].get('nutriscore_grade', "")
            dico["store"] = p[i].get('stores', "").replace("\\", "")
            dico["url"] = p[i].get('url', "")
            prods.append(dico)
            i += 1
        return prods
