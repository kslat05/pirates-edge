from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
from game.items import Item
import random

#Thief guy
class Thief(combat.Monster):
    def __init__(self, name):
        attacks = {
            "steal": ["steals some food", random.randrange(10, 25), (5, 10)],
            "throw": ["throws leftover food", random.randrange(20, 35), (1, 5)]
        }
        super().__init__(name, random.randrange(10, 21), attacks, 100 + random.randrange(-10, 21))
        self.type_name = "Food Thief"

#Event with theives
class KitchenRaid(event.Event):
    def __init__(self):
        self.name = "food thieves attack"

    def process(self, world):
        result = {}
        result["message"] = "The food thieves have been dealt with!"
        thieves = []
        n_appearing = random.randrange(2, 6)
        for i in range(n_appearing):
            thieves.append(Thief(f"Food Thief {i + 1}"))
        display.announce("The kitchen is under attack by food thieves!")
        combat.Combat(thieves).combat()
        result["newevents"] = [self]
        return result

# Rowdy Diners
class AngryDiner(combat.Monster):
    def __init__(self, name):
        attacks = {
            "yell": ["yells loudly", random.randrange(15, 30), (1, 5)],
            "throw chair": ["throws a chair", random.randrange(20, 40), (5, 10)]
        }
        # 15 to 25 health, disruptive behavior, 70 to 90 speed
        super().__init__(name, random.randrange(15, 26), attacks, 80 + random.randrange(-10, 11))
        self.type_name = "Angry Diner"

#Event with diners
class DiningRoomChaos(event.Event):
    def __init__(self):
        self.name = "dining room chaos"

    def process(self, world):
        result = {}
        result["message"] = "The dining room has been restored to order!"
        diners = []
        n_appearing = random.randrange(3, 7)
        for i in range(n_appearing):
            diners.append(AngryDiner(f"Angry Diner {i + 1}"))
        display.announce("Angry diners are causing chaos in the dining room!")
        combat.Combat(diners).combat()
        result["newevents"] = [self]
        return result

class PantryPuzzle(event.Event):

    def __init__(self):
        self.name = "organize the pantry"

    def process(self, world):
        result = {}
        result["message"] = "The pantry is organized!"
        display.announce("The pantry is messy and needs to be organized!")
        boxes = [1, 2, 3]
        for x in boxes:
            r = random.randrange(1, 5)
            inp =  input(f"Pick which shelf to place box{x} on! (1-5)")
            while inp != r:
                inp = input(f"Try again! Which shelf should box{x} go on? (1-5)")
        
        result["newevents"] = [self]
        return result

# Restaurant Definition
class McDonalds(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "McDonald's"
        self.symbol = 'M'
        self.visitable = True
        self.locations = {
            "kitchen": Kitchen(self),
            "dining_area": DiningArea(self),
            "pantry": Pantry(self),
            "storage": Storage(self),
            "reception": Reception(self)
        }
        self.starting_location = self.locations["reception"]

    def enter(self, ship):
        display.announce("Welcome to McDonald's! I hope you're using the mobile app because I can't work the register.", pause=False)

class Wallet(Item):
    def __init__(self):
        super().__init__("green-flower", 10)

class Kitchen(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "kitchen"
        self.event_chance = 50
        self.events.append(KitchenRaid())

    def enter(self):
        display.announce("You step into the kitchen filled with frozen food.")

class DiningArea(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "dining area"
        self.event_chance = 50
        self.events.append(DiningRoomChaos())

    def enter(self):
        display.announce("You walk into the dining area, it is very dirty.")

class Pantry(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "pantry"
        self.event_chance = 30
        self.events.append(PantryPuzzle())

    def enter(self):
        display.announce("You enter the pantry, stocked with frozen food.")

class Storage(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "storage"
        self.event_chance = 20

    def enter(self):
        game = config.the_player
        game.add_to_inventory([Wallet()])
        display.announce(f"You pick up a wallet off the storage room ground, maybe you'll get some extra points😊.")
        display.announce("You explore the storage area where the employees take their breaks.")

class Reception(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "reception"
        self.event_chance = 10

    def enter(self):
        display.announce("You arrive at the reception area, it isn't very welcoming.")
