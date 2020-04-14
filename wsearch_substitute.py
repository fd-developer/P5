#! /usr/bin/env python3
# coding: utf-8
from tkinter import Tk, Label, Button, StringVar, Entry, Toplevel, \
    messagebox, ttk
from tkinter import *
import tkinter as tk
from database import *
import json
from api import *
from wproduct_sheet import *


class Wsearch_substitute():
    # This class is used to search product's substitute

    def __init__(self, db, wparent):
        self.db_connected = db
        self.parent = wparent
        self.category_selected = ""
        self.nbcateg = 0
        self.indexcateg = 0

        with open('ressources/connect.json') as f:
            self.key = json.load(f)
        try:
            self.nbcateg = int(self.key.get("nbcateg", ""))
        except IOError as e:
            print("Error with nbcateg", e)

    def show_list_categories(self):
        # Display a list of categories on left part and
        # a liste of products on the right when we choose
        # a category
        self.parent.fen = Toplevel()
        self.fen = self.parent.fen

        self.fen.title("Quel aliment souhaitez-vous remplacer ?")
        self.fen.geometry("800x500")

        self.fen.rowconfigure(0, weight=0)
        for i in range(1, 10):
            self.fen.rowconfigure(i, weight=1)
        for i in range(6):
            self.fen.columnconfigure(i, weight=1)

        lbl1 = Label(self.fen, text="Sélectionner une catégorie")
        lbl1.grid(row=1, column=1, sticky="sw")

        self.fen.listCateg = Listbox(self.fen, selectmode=SINGLE)
        self.fen.listCateg.grid(
            row=2, column=1, rowspan=6, columnspan=2, sticky="nsew")

        self.fen.sbar = ttk.Scrollbar(
            self.fen, orient=tk.VERTICAL, command=self.fen.listCateg.yview)
        self.fen.sbar.grid(row=2, column=0, rowspan=6, sticky=tk.NS)
        self.fen.listCateg.config(yscrollcommand=self.fen.sbar.set)

        self.text = StringVar()
        self.text.set("Sélectionner un produit")
        self.fen.lbl2 = Label(self.fen, textvariable=self.text)
        self.fen.lbl2.grid(row=1, column=3, sticky="sw")

        self.fen.listProd = Listbox(self.fen, selectmode=SINGLE)
        self.fen.listProd.grid(
            row=2, column=3, rowspan=6, columnspan=2, sticky="nsew")

        self.btnFicheProd = Button(
            self.fen, text="Voir la fiche produit",
            command=self.show_product_sheet)
        self.btnFicheProd.grid(
            row=8, column=1, columnspan=1, sticky="nsew")

        self.btnRechCateg = Button(
            self.fen, text="Rechercher un produit de substitution",
            command=self.search_substitut_from_database)
        self.btnRechCateg.grid(
            row=8, column=2, columnspan=3, sticky="nsew")

        # Load list of categories from database or init from API
        # if no product found in the database
        if (self.list_categories_from_database() == 0):
            nb = self.db_connected.create_list_categories_from_api(
                self.nbcateg)
            messagebox.showinfo("Maj catégories", str(nb) + " catégories ont"
                                " été importées depuis openfoodfacts.org")

            nb = self.db_connected.create_list_products_by_category_from_api()
            messagebox.showinfo("Maj produits", str(nb) + " produits ont"
                                " été importés depuis openfoodfacts.org")

            self.list_categories_from_database()

        self.fen.listCateg.bind('<<ListboxSelect>>', self.show_products)
        self.fen.mainloop()

    def show_products(self, event):
        # From database
        # Display a list of products of the category selected
        print("show products ...")
        if self.fen.listCateg.curselection() is not ():
            index = self.fen.listCateg.curselection()[0]
            if index > 0:
                self.indexcateg = index
                self.list_products_category()

    def show_product_sheet(self):
        # From database
        # Display the product sheet of the product selected
        print("show product sheet ...")
        index = self.fen.listProd.curselection()[0]
        prodsheet = Wproduct_sheet(self.get_product_selected(index))
        prodsheet.display_product_sheet()

    def list_categories_from_api(self):
        # From openfoodfacts
        # Display a list of products of the category selected
        print("show products ...")
        ap = Api()
        cpt = 0
        for category in ap.list_categories():
            self.fen.listCateg.insert(cpt, category)
            cpt += 1
        print(ap.list_categories())

    def list_categories_from_database(self):
        # Display a list of categories found in database
        print("List categories")
        cpt = 0
        for category in self.db_connected.load_category():
            self.fen.listCateg.insert(cpt, category[0])
            cpt += 1
        return cpt

    def list_products_category(self):
        # Display a list of products of the category selected
        self.fen.listProd.delete(0, END)
        index = self.fen.listCateg.curselection()[0]
        self.category_selected = self.fen.listCateg.get(index)
        self.text.set("liste des produits de "+self.category_selected)

        cpt = 0
        for name in self.db_connected.list_products_in_a_category(
        self.category_selected):
            self.fen.listProd.insert(
                cpt, str(cpt) + " : " + name['name'] +
                " (" + name['score'] + ")")
            cpt += 1

        # No product in the database, we will search the openfoodfacts
        if cpt == 0:
            ap = Api()
            for name in ap.list_products_in_a_category(self.category_selected):
                self.fen.listProd.insert(
                    cpt, str(cpt) + " : " + name['name'] + " (" +
                    name['score'] + ")")
                cpt += 1
        return cpt

    def search_substitut_from_database(self):
        # Search product' substitute
        print("Finding the substitute product")
        selProduct = {}
        substituteProduct = {}
        substituteFound = False
        index = self.fen.listProd.curselection()[0]
        selectedProduct = self.fen.listProd.get(index).split(":")
        score = selectedProduct[1].split("(")
        score = score[1].replace(")", "")

        if len(score) == 1:
            # Search for the product to replace
            selProduct = self.get_product_selected(index)

            # Finding the substitute product
            for substituteProduct in self.db_connected.list_products_in_a_category(
                    self.category_selected):

                if len(substituteProduct['score']) == 1:
                    print(ord(substituteProduct['score'].upper()), ord(score.upper()))
                    if ord(substituteProduct['score'].upper()) < ord(score.upper()):

                        # substituteProduct = {
                        #     'code': product['code'],
                        #     'name': product['name'],
                        #     'score': product['score'],
                        #     'store': product['store'],
                        #     'url': product['url']
                        #     }

                        substituteFound = True
                        if messagebox.askyesno(
                            "info", "Le produit >>" + selectedProduct[1] +
                            " <<" + "\npeut être substitué par : \n\n \
                            Nom : " + substituteProduct['name'] + "\n \
                            Code : " + substituteProduct['code'] + "\n \
                            Score : " + substituteProduct['score'] + "\n \
                            Store : " + substituteProduct['store'] + "\n \
                            URL : " + substituteProduct['url'] + "\n" + "\n \
                                Souhaitez-vous enregistrer le substitut ?"):

                            self.db_connected.update_substitut(
                                selProduct, substituteProduct)
                        break

        if substituteFound is not True:
            messagebox.showinfo("", "Aucun substitut n'a été trouvé"
                                " pour \n>> " + selectedProduct[1] + " <<")

    def get_product_selected(self, index):
        # Search for the product select in the list
        i = -1
        selProduct = {}
        for product in self.db_connected.list_products_in_a_category(
        self.category_selected):
            i = i + 1
            if i == index:
                selProduct = product
                break
        return selProduct
