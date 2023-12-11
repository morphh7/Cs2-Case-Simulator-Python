# script data
# @ authors: balve entertainment
# @ dev: Bilguun, Peter

from kivy.app import App as app
from kivy.uix.label import Label as label
from kivy.uix.button import Button as button
from kivy.uix.gridlayout import GridLayout as grid_layout
from kivy.uix.boxlayout import BoxLayout as box_layout
from kivy.uix.image import Image as image
from kivy.config import Config as config

import random as math
import os

# lua things
false = False
true = True

# bools
_DEBUG = true
_FULLSCREEN = false

# helpers
class helpers():
    def security(self, use):
        if not use:
            return true
        
        username = input("Username: ")
        password = input("Password: ")

        if username == "123" and password == "123":
            return true
        
        return false
        
    def in_between(self, min_, max_, actual):
        if actual > min_ and actual < max_:
            return true
        
        return false
    
    def get_weapon_wear(self, float_):
        if self.in_between(0, 0.07, float_):
            return 1
        
        if self.in_between(0.07, 0.15, float_):
            return 2
        
        if self.in_between(0.15, 0.37, float_):
            return 3
        
        if self.in_between(0.37, 0.44, float_):
            return 4
        
        if self.in_between(0.44, 1, float_):
            return 5

    def chance(self, probability):
        random_number = math.randrange(probability)

        return {
            "result": random_number == 1,
            "odds": random_number,
            "chance": (1 / probability)
        }

        
helpers = helpers()

# main functions
class ctx(app):
    def _init_(self):
        if _FULLSCREEN: config.set('graphics', 'fullscreen', 'auto')

        self.knife_odds = false
        self.glove_odds = false
        self.is_stattrack = false

        self.weapon_type = 0
        self.weapon_name = 0
        self.weapon_amount = 0
        self.data_label = label(text = '', font_size = 20, size_hint=(1, 0.5))
        self.header_label = label(text = 'CS:GO Case Opener Simulator', font_size = 20, size_hint=(1, 0.5))
        self.image_format = image(source = "Glove.png", size_hint=(1, 2))
        
        self.get_wear = {
            1: "Factory New", 2: "Minimal Wear", 
            3: "Field Tested", 4: "Well Worn", 5: "Battle Scarred"
        }
        self.get_weapon_type = {
            1: "Pistol", 2: "Rifle", 3: "SMG", 4: "Heavy Weapon", 5: "Knife", 6: "Glove"
        }

        # weapons
        self.weapon_class_amount = {
            1: 10, 2: 11, 3: 7, 4: 6, 5: 19, 6: 8
        } # 10 pistol, 11 rifle, 7 smg, 6 heavy, 19 knives, 8 gloves

        self.pistol_types = {
            1: "CZ75-Auto", 2: "Desert Eagle", 3: "Dual Berettas", 4: "Five SeveN", 5: "Glock-18", 6: "P2000",
            7: "P250", 8: "R8 Revolver", 9: "Tec-9", 10: "USP-S"
        }
        self.rifle_types = {
            1: "AK-47", 2: "AUG", 3: "AWP", 4: "FAMAS", 5: "G3SG1", 6: "Galil AR",
            7: "M4A1-S", 8: "M4A4", 9: "SCAR-20", 10: "SG 553", 11: "SSG 08"
        }
        self.smg_types = {
            1: "MAC-10", 2: "MP5-SD", 3: "MP7", 4: "MP9", 5: "PP-Bizon", 6: "P90", 7: "UMP-45",
        }
        self.heavy_types = {
            1: "MAG-7", 2: "Nova", 3: "Sawed-Off", 4: "XM1014", 5: "M249", 6: "Negev",
        }
        self.knife_types = {
            1: "Bayonet", 2: "Bowie Knife", 3: "Butterfly Knife", 4: "Classic Knife", 5: "Falchion Knife", 6: "Flip Knife",
            7: "Gut Knife", 8: "Huntsman Knife", 9: "Karambit", 10: "M9 Bayonet", 11: "Navaja Knife", 12: "Nomad Knife",
            13: "Ursus Knife", 14: "Paracord Knife", 15: "Shadow Daggers", 16: "Skeleton Knife", 17: "Stiletto Knife",
            18: "Survival Knife", 19: "Talon Knife"
        }
        self.glove_types = {
            1: "Hand Wraps", 2: "Moto Gloves", 3: "Specialist Gloves", 4: "Sport Gloves", 
            5: "Bloodhound Gloves", 6: "Hydra Gloves", 7: "Broken Fang Gloves", 8: "Driver Gloves",
        }

    # helper
    def seperate_weapon_arrays(self):
        if self.weapon_name == "Pistol":
            return self.pistol_types[self.weapon_amount]
        if self.weapon_name == "Rifle":
            return self.rifle_types[self.weapon_amount]
        if self.weapon_name == "SMG":
            return self.smg_types[self.weapon_amount]
        if self.weapon_name == "Heavy Weapon":
            return self.heavy_types[self.weapon_amount]
        if self.weapon_name == "Knife":
            return self.knife_types[self.weapon_amount]
        if self.weapon_name == "Glove":
            return self.glove_types[self.weapon_amount]

    def generate_data(self):
        # fetch weapon data
        self.knife_odds = helpers.chance(385) # 1 in 385 = knife
        self.glove_odds = helpers.chance(400) # 1 in 400 = glove
        self.is_stattrack = helpers.chance(10) # 1 in 10 = stattrack

        if self.knife_odds["result"]: self.weapon_type = 5
        elif self.glove_odds["result"]: self.weapon_type = 6
        else: self.weapon_type = math.randint(1, 4)

        self.weapon_name = self.get_weapon_type[self.weapon_type]
        self.weapon_amount = math.randint(1, self.weapon_class_amount[self.weapon_type])

        # get weapon float
        _float = math.uniform(0, 1)

        # get weapon wear
        _wear = helpers.get_weapon_wear(_float)

        # get weapon stattrack
        _stattrack = helpers.chance(10)

        return {
            "float": _float,
            "wear": self.get_wear[_wear],
            "stat-track": _stattrack["result"],
            "weapon_index": self.weapon_type,
            "weapon_class": self.weapon_name,
            "weapon": self.seperate_weapon_arrays()
        }
    
    def callback(self, instance):
        data = self.generate_data()

        # format it to png from folder
        self.image_format.source = (self.weapon_name == "Glove" and "Glove" or str(self.seperate_weapon_arrays())) + ".png"

        self.header_label.text = f'{self.is_stattrack["result"] == true and "StatTrack™" or ""} {data["weapon"]} | weapon_skin: null'
        self.data_label.text = str(data)

        if _DEBUG: print(f'Image: {self.image_format.source}, weapon: {data["weapon"]}, knife chance: {self.knife_odds}')

    # core functions
    def build(self):
        self._init_()
        self.generate_data()
        os.system('cls')

        if not helpers.security(false):
            exit()

        layout_widget = box_layout(orientation = 'vertical')
        
        btn = button(text = "Open Case", size_hint = (1, 0.1))
        btn.bind(on_press = self.callback)
        
        layout_widget.add_widget(self.data_label)
        layout_widget.add_widget(self.header_label)
        layout_widget.add_widget(self.image_format)
        layout_widget.add_widget(btn)

        return layout_widget
    
# run the app
ctx().run()