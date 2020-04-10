#! /usr/bin/env python3
# coding: utf-8
from tkinter import Tk, Label, Button, StringVar, Entry, Toplevel, \
    messagebox, ttk
from tkinter import *
import tkinter as tk
import json


class Wconfig():
    # This class is used to manage the configuration parameters 
    # of the application
    def __init__(self, caninit, db):
        self.db_connected = db
        # cainit = 1 if we need to display a checkbutton in
        # configuration window to create the database
        self.can = caninit
        self.btn_save_clicked = False
        self.db_created = False

    def show_config(self):
        # Display config window
        self.fen = tk.Tk()

        self.fen.title("Configuration générale de l'application")
        self.fen.geometry("400x380")

        for i in range(0, 11):
            self.fen.rowconfigure(i, weight=1)
        for i in range(4):
            self.fen.columnconfigure(i, weight=1)

        self.fen.lbl1 = Label(self.fen, text="Server : ")
        self.fen.lbl1.grid(row=0, column=1, sticky="w")
        self.fen.server = Entry(self.fen, width=20)
        self.fen.server.grid(row=0, column=2, sticky="ew")

        self.fen.lbl2 = Label(self.fen, text="Login (root) : ")
        self.fen.lbl2.grid(row=1, column=1, sticky="w")
        self.fen.loginroot = Entry(self.fen, width=20)
        self.fen.loginroot.grid(row=1, column=2, sticky="ew")

        self.fen.lbl3 = Label(self.fen, text="Password (root) : ")
        self.fen.lbl3.grid(row=2, column=1, sticky="w")
        self.fen.passwordroot = Entry(self.fen, width=20, show="*")
        self.fen.passwordroot.grid(row=2, column=2, sticky="ew")

        self.fen.lbl4 = Label(self.fen, text="Database : ")
        self.fen.lbl4.grid(row=3, column=1, sticky="w")
        self.fen.database = Entry(self.fen, width=20)
        self.fen.database.grid(row=3, column=2, sticky="ew")

        self.fen.lbl5 = Label(self.fen, text="Login : ")
        self.fen.lbl5.grid(row=4, column=1, sticky="w")
        self.fen.login = Entry(self.fen, width=20)
        self.fen.login.grid(row=4, column=2, sticky="ew")

        self.fen.lbl6 = Label(self.fen, text="Password : ")
        self.fen.lbl6.grid(row=5, column=1, sticky="w")
        self.fen.password = Entry(self.fen, width=20, show="*")
        self.fen.password.grid(row=5, column=2, sticky="ew")

        self.fen.lbl7 = Label(self.fen, text="Nb. categories : ")
        self.fen.lbl7.grid(row=6, column=1, sticky="w")
        self.fen.nbcateg = Entry(self.fen, width=20)
        self.fen.nbcateg.grid(row=6, column=2, sticky="ew")
        
        # Display a checkbutton to allow database creation
        self.fen.v = BooleanVar() 
        if self.can == 1:
            self.fen.lbl8 = Label(self.fen, text="Create database")
            self.fen.lbl8.grid(row=7, column=1, sticky="w")
            self.fen.case = Checkbutton(
                self.fen, var=self.fen.v, command=self.callBackCheck)
            self.fen.case.grid(row=7, column=2, sticky="w")

        btn_save = Button(
            self.fen, text="Enregistrer", command=self.write_config)
        btn_save.grid(row=9, column=1, sticky="nsew")

        btn_cancel = Button(
            self.fen, text="Annuler", command=self.fen.destroy)
        btn_cancel.grid(row=9, column=2, sticky="nsew")

        self.load_config()

        self.fen.mainloop()

    def callBackCheck(self):
        self.fen.v.set(not self.fen.v.get())

    def load_config(self):
        # Display configuration saved in connect.json
        print("Load config ...")
        with open('ressources/connect.json') as f:
            self.key = json.load(f)

        try:
            self.fen.server.insert(0, self.key["server"])
            self.fen.database.insert(0, self.key["database"])
            self.fen.login.insert(0, self.key["login"])
            self.fen.password.insert(0, self.key["password"])
            self.fen.loginroot.insert(0, self.key["loginroot"])
            self.fen.passwordroot.insert(0, self.key["passwordroot"])
            self.fen.nbcateg.insert(0, int(self.key["nbcateg"]))

        except IOError as e:
            print("Error with connect.json", e)

    def write_config(self):
        # Save configuration
        dico = {}
        dico["server"] = self.fen.server.get()
        dico["database"] = self.fen.database.get()
        dico["login"] = self.fen.login.get()
        dico["password"] = self.fen.password.get()
        dico["loginroot"] = self.fen.loginroot.get()
        dico["passwordroot"] = self.fen.passwordroot.get()
        dico["nbcateg"] = int(self.fen.nbcateg.get())

        with open("ressources/connect.json", "w") as f:
            json.dump(dico, f)
        
        if self.fen.v.get():    
            if messagebox.askyesno(
                "?", "Souhaitez-vous vraiment réinitialiser la base " \
                "de données ?"):
                self.db_created = self.db_connected.destroy_db();

        self.btn_save_clicked = True

        if self.db_created is False:
            self.fen.destroy()
        else:
            self.fen.quit()

    @property
    def config_ok(self):
        # To know if user quit this window with button "enregistrer"
        return self.btn_save_clicked

    @property
    def create_db_asked(self):
        # To know if user asked to create database
        return self.db_created
