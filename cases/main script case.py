# script data §
# @ authors: balve entertainment
# @ game: conter strik global offensive (csgo)

# import kivy modules
from kivy.app import App as app
from kivy.uix.label import Label as label
from kivy.uix.button import Button as button
from kivy.uix.boxlayout import BoxLayout as box_layout
from kivy.uix.image import Image as image
from kivy.config import Config as config

# other essential python modules
import json
import random as math
import os
import steammarket

# lua things
false = False
true = True

# others
folder_path = "Images/"

# bools
_DEBUG = true
_FULLSCREEN = true
_DETAILS = false
_GOLDPRICE = true

# generate new match for gold
with open("data.json", "w") as f:
    json.dump({
        "match": math.randrange(400)
    }, f)

with open("data.json", "r") as f:
    current_match = json.load(f)

# helpers
class helpers():
    def log(self, string_):
        print(f"[DEBUG] - {string_}")

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
        self.log(f"calculating weapon skin wear with {float_} float")
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

    def chance(self, probability, gold):
        random_number = math.randrange(probability)

        if not gold:
            self.log("generating new chances")
            return {
                "result": random_number == current_match["match"],
                "odds": random_number,
                "chance": str((1 / probability) * 100) + "%",
            }

        self.log("generating new chances for gold")
        return {
            "result": random_number == 1,
            "odds": random_number,
            "chance": str((1 / probability) * 100) + "%",
        }

helpers = helpers()

# main functions
class case_simpulator(app):
    def _init_(self):
        # fullscreen?
        if _FULLSCREEN: config.set('graphics', 'fullscreen', 'auto')
        helpers.log(f"fullscreen? {_FULLSCREEN}")
        helpers.log(f"starting _init_ function...")

        # update bools
        self.cant_procced = false
        self.gold_odds = false
        helpers.log(f"successfully generated new booleans")

        # update string
        self.gold_item = "nil"

        # update ints
        ## weapon things
        self.weapon_type = 0
        self.weapon_name = 0
        self.weapon_amount = 0

        ## case things
        self.case_count = 0
        self.spent_on_key = 0
        self.spent_on_case = 0

        ## cause price indexing
        self.balve_original_case = 3
        self.default_price = 1.5
        helpers.log(f"successfully generated new intergers")

        # update items
        self.data_label = label(text = '', font_size = 20, size_hint=(1, 0.5))
        self.header_label = label(text = 'CS2 Case Simulator', font_size = 20, size_hint=(1, 0.5))
        self.image_format = image(source = folder_path + "Case.png", size_hint=(1, 2))
        helpers.log(f"fully generated/reset app items")
        
        # update data arrays
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
        helpers.log(f"successfully generated new array/tables")

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
        self.gold_odds = helpers.chance(400, true) # 1 in 400 = gold?
        helpers.log(f"gold? {self.gold_odds}")

        is_stattrack = helpers.chance(10, false) # 1 in 10 = stattrack
        helpers.log(f"stat-track? {is_stattrack}")

        if self.gold_odds["result"]: 
            self.weapon_type = 5
            _wear = 1
            self.cant_procced = true
        else: 
            self.weapon_type = math.randint(1, 4)

        self.weapon_name = self.get_weapon_type[self.weapon_type]
        self.weapon_amount = math.randint(1, self.weapon_class_amount[self.weapon_type])
        self.skin_name = self.seperate_weapon_arrays()
        helpers.log(f"weapon - {self.skin_name}({self.weapon_amount})")

        # get weapon float
        _float = math.uniform(0, 1)
        helpers.log(f"float - {_float}")

        # get weapon wear
        _wear = helpers.get_weapon_wear(_float)
        helpers.log(f"wear - {_wear}")

        item_name = f"★ {self.skin_name} | Fade ({self.get_wear[_wear]})"
        if _DETAILS: item = steammarket.get_csgo_item(item_name, currency='EUR')
        helpers.log(f"calculate real-time price? {_DETAILS}")

        if _GOLDPRICE and self.cant_procced: self.gold_item = steammarket.get_csgo_item(item_name, currency="EUR")
        helpers.log(f"gold price - {self.gold_item}")

        return {
            "float": _float,
            "wear": self.get_wear[_wear],
            "stat-track": is_stattrack["result"],
            "weapon_index": self.weapon_type,
            "weapon_class": self.skin_name,
            "weapon": self.seperate_weapon_arrays(),
            "item_name": item_name,
            "item_price": self.gold_item != "nil" and self.gold_item or (_DETAILS == true and item or "N/A")
        }
    
    def callback(self, instance):
        data = self.generate_data()
        print("\n")
        helpers.log(f"new case - index {self.case_count + 1}")
        helpers.log(f"successfully generated new data")
        self.case_count += 1

        # format it to png from folder
        self.image_format.source = folder_path + (self.weapon_name == "Glove" and "Glove" or str(self.seperate_weapon_arrays())) + ".png"
        helpers.log(f"formating index names to .png")

        self.header_label.text = f'{data["stat-track"] == true and "StatTrack™" or ""} {data["weapon"]} | Skin Name ({data["wear"]}) {self.cant_procced and "- " + str(self.gold_item) or ""}'
        self.data_label.text = str(data)
        helpers.log(f"new header texts")

        # disable button so we dont skip a knife or a glove
        instance.disabled = self.cant_procced == true
        helpers.log(f"gold and cant procced? {instance.disabled}")

        # rename text to how many cases we've opened
        instance.text = str(self.case_count)
        helpers.log(f"new instance text")

        # rename text to how much we've spent on cases
        self.spent_on_key = self.case_count * 2.35
        self.spent_on_case = self.case_count * self.balve_original_case
        if instance.disabled == true:
            instance.text = f"{round(self.spent_on_key)}€ spent on keys\n{round(self.spent_on_case)}€ spent on cases\n{round(self.spent_on_case + self.spent_on_key)}€ spent in total\nopened {self.case_count} cases"
            helpers.log(f"calculated money spent")

        if _DEBUG: print(f'Image: {self.image_format.source}, weapon: {data["weapon"]}, current_match: {current_match["match"]}, gold chance: {self.gold_odds}')
        helpers.log(f"debug? {_DEBUG}")

    # core functions
    def build(self):
        os.system("cls")
        self._init_()
        self.generate_data()

        if not helpers.security(false):
            exit()

        layout_widget = box_layout(orientation = 'vertical')
        helpers.log(f"create layout widget {layout_widget}")
        
        btn = button(text = "Open Case", size_hint = (1, 0.3))
        btn.bind(on_press = self.callback)
        helpers.log(f"create button and bindings")
        
        layout_widget.add_widget(self.data_label)
        layout_widget.add_widget(self.header_label)
        layout_widget.add_widget(self.image_format)
        layout_widget.add_widget(btn)
        helpers.log(f"successfully added all item widgets")

        return layout_widget
    
# run the app
case_simpulator().run()