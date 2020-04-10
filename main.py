#! /usr/bin/env python3
# coding: utf-8
from tkinter import Tk, Label, Button, StringVar, \
    Entry, Toplevel, messagebox, ttk
from tkinter import *
import tkinter as tk
from wmenu import *
from database import *
from wconfig import *


class Application():
    def __init__(self):
        self.db = Database()
        if self.db.connected is False:

            self.wconfig = Wconfig(0, self.db)
            self.wconfig.show_config()

            if self.wconfig.config_ok:
                self.db.create_db()
                
            self.db = Database()

        self.menu = Wmenu(self.db)
        self.menu.show_menu()

    def __del__(self):
        self.db.disconnect()
        print("Fin de programme")

app = Application()
