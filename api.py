#! /usr/bin/env python3
# coding: utf-8

import json
import requests
from bs4 import BeautifulSoup


class Api():
    # def __init__(self):

    def list_categories(self):
        print("Download a list of categories from OpenFoodFacts ...")
        # requete = requests.get("https://fr.openfoodfacts.org/categories")
        # page = requete.content
        # soup = BeautifulSoup(page)#,'features="html.parser"')
        # categ = soup.find_all("a", {"class": "tag known"})
        # liste_categ = [elt.string.strip() for elt in categ]
        # liste_categ.sort()
        # print(liste_categ)
        # return liste_categ

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
        liste_categ = []
        while i < len(p):
            liste_categ.append(p[i].get('name', ""))
            i += 1
        return liste_categ

    def list_products_in_a_category(self, pCateg):
        print("Download products for " + pCateg + " from OFF ...")

        url = 'https://fr.openfoodfacts.org/cgi/search.pl?' \
            'action=process&tagtype_0=categories&tag_contains_0=contains' \
            '&tag_0=' + pCateg + "" \
            '&json=true&tag_1=&page_size=500'

        headers = {
            'User-Agent': 'Student openclassrooms - project 5',
            'From': 'fd-mail@laposte.net'
        }
        # requete = requests.get("https://fr.openfoodfacts.org/categorie/"
        # +pCateg+".json")
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
