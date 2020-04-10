#! /usr/bin/env python3
# coding: utf-8
from tkinter import Tk, Label, Button, StringVar, Entry, Toplevel, messagebox
from tkinter import *
from database import *
import json
from api import *
from wsearch_substitute import *
from wlist_substitute import *
from wconfig import *
import webbrowser


class Wmenu():
    # This class is used to display the menu of the application

    def __init__(self, db):
        self.db_connected = db

    def show_menu(self):
        self.root = Tk()
        self.root.geometry("600x300")
        self.wsearch_s = Wsearch_substitute(self.db_connected, self.root)
        self.wlist_s = Wlist_substitute(self.db_connected, self.root)
        self.wconfig = Wconfig(1, self.db_connected)

        self.root.title("OCR - P5 - Fred DESCHAMPS")

        for i in range(6):
            self.root.rowconfigure(i, weight=1)
        for i in range(7):
            self.root.columnconfigure(i, weight=1)

        btn1 = Button(
            self.root, bitmap="ressources/logo.png",
            borderwidth=5, command=lambda:
            webbrowser.open('https://fr.openfoodfacts.org/'))
        btn1.grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nsew")

        btn2 = Button(
            self.root,
            text="Configuration de l'application",
            command=self.go_config)
        btn2.grid(row=4, column=1, rowspan=1, columnspan=2, sticky="nsew")

        btn3 = Button(
            self.root, text="1 - Quel aliment souhaitez-vous remplacer ?",
            command=self.wsearch_s.show_list_categories)
        btn3.grid(row=1, column=5, sticky="nsew")

        btn4 = Button(
            self.root, text="2 - Retrouver mes aliments substitués",
            command=self.wlist_s.show_list_substitutes)
        btn4.grid(row=2, column=5, sticky="nsew")

        btn5 = Button(
            self.root, text="Fin de programme", command=self.root.destroy)
        btn5.grid(row=4, column=5, sticky="nsew")

        self.root.mainloop()

    def go_config(self):
        # Display config window and quit if database had been recreate
        self.wconfig.show_config()
        if self.wconfig.create_db_asked:
            print("Quit ...")
            self.root.quit()

