#! /usr/bin/env python3
# coding: utf-8
from tkinter import Tk, Label, Button, StringVar, Entry, Toplevel, messagebox
from tkinter import *
import tkinter as tk
from database import *
import webbrowser


class Wlist_substitute():
    # This class is used to manage product's substitute
    def __init__(self, db, wParent):
        self.db_connected = db
        self.parent = wParent

    def do_select(event):
        global current_selection

        widget = event.widget
        infos = widget.grid_info()
        row = infos['row']
        master = infos['in']

        if(row > 1):
            if current_selection is not None and current_selection is not row:
                for w in master.grid_slaves(row=current_selection):
                    w.configure(font=fonts['normal'])

            for w in master.grid_slaves(row=row):
                w.configure(font=fonts['bold'])

            current_selection = row

    def open_web_page(self, code):
        url = self.db_connected.get_product_url(code)
        webbrowser.open('' + url + '')
        print(code)
        print(url)

    def show_list_substitutes(self):
        print('show_list_substitutes ...')
        fonts = {
            'normal': 'arial 14',
            'bold': 'arial 14 bold',
            'titre': 'Helvetica 15 bold',
            'titrepage': 'arial 30'
            }
        column_title = ["Name", "Code", "Score", "Store", "Substitute",
                        "Substitute name"]
        column = ["name", "code", "nutriscoreG", "store", "substitute",
                        "substitutename"]
        data = self.db_connected.load_substituted_products_from_local_db()

        root = tk.Tk()
        root.title("")
        root.geometry("1100x500")
        label = tk.Label(
            root,
            text="Liste des produits substitués",
            font=fonts['titrepage'])
        label.grid(
            row=0, column=0, columnspan=len(column_title), sticky=tk.W+tk.E)

        for i in range(len(column_title)):
            label = tk.Label(
                root, text=column_title[i], font=fonts['titre'])
            label.grid(row=1, column=i, padx=0)

        for i in range(0, len(column_title)):
            for j in range(2, len(data)+2):
                color = ['grey75', 'white'][j % 2]

                if column[i] == "code" or column[i] == "substitute":
                    btn = tk.Button(root, bg=color, text="%s\
                        " % ((data[j-2][column[i]][:50])))
                    btn.config(command=lambda x=btn.cget(
                        'text'): self.open_web_page(x), bg=color)
                    btn.grid(row=j, column=i, padx=0)
                else:
                    label = tk.Label(
                        root, text="%s" % (data[j-2][column[i]][:50]),
                        bg=color, width=20, anchor='w', font=fonts['normal'])
                    label.grid(row=j, column=i, padx=0)

        current_selection = None

        tk.mainloop()
