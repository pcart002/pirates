####################################################################################################
# Imports
####################################################################################################

from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random

class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['south'] = self

    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()

class Wet_Cave (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "cave"
        self.verbs['north'] = self

    def enter (self):
        display.announce ("You and your pirate crew stand at the entrance of a dark, dripping cave. Your ship is at anchor in a small bay north.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()

class Spooky_Tavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Tavern"
        self.verbs['east'] = self

    def enter (self):
        display.announce ("You and your pirate crew enter a dimly lit tavern on a stormy night. The wooden sign above reads \"The Black Mariner\". A chill fills the spines of you and your crewmates.... Your ship is at anchored east.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            display.announce ("You return to your ship in fear.")
            self.main_location.end_visit()

class Reef (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "reef"
        self.verbs['west'] = self

    def enter (self):
        display.announce ("The pirate crew finds themselves floating in the tranquil waters of the coral reef, mes,erized by the beauty surrounding them. Sunlight filters through the crystal-clear waves, creating dancing patterns on the sea floor. Your crew is in awe.... Your ship is anchored west.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()

class puzzle:
    #def __init__
    def nums(self, fruits):
        result = {}
        for fruit in fruits:
            if fruit == "🍌":
                result["🍌"] = random.randint(5, 10)
            elif fruit == "🍑":
                result["🍑"] = random.randint(1, 15)
            elif fruit == "🍉":
                result["🍉"] = random.randint(1, 5)
        return result

    def minigame(self):
        fruits = ["🍌", "🍑", "🍉"]
        result = self.nums(fruits)

        print("🍌 + 🍌 + 🍌 =",int(result["🍌"]) + int(result["🍌"]) + int(result["🍌"]))
        print("🍌 + 🍑 + 🍑 =",int(result["🍌"]) + int(result["🍑"]) + int(result["🍑"]))
        print("🍌 - 🍉 =",int(result["🍌"]) - int(result["🍉"]))

        fruitpunch = int(result["🍌"]) + int(result["🍑"]) + int(result["🍉"])

        player_ans = int(input("Whats 🍌 + 🍑 + 🍉 = ? "))
        if player_ans == fruitpunch:
            print('You have found food!')
            return False
        
        else:
            play_again = input('Incorrect, Play Again? (y/n)').strip().lower()
            if play_again != "y":
                print('Thanks For Playing!')
                return False
            
            else:
                return True

    def main(self):
        play = True
        while play:
            play = self.minigame()

class Crabs(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["pinch"] = ["pinches",random.randrange(60,100), (0,3)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(3,5), attacks, 75 + random.randrange(-10,11))
        self.type_name = "Crab"

class Angry_Crabs (event.Event):
    #small low health crabs that attack the pirates randomly

    def __init__ (self):
        self.name = "Angry Crab Ambush"
        self.event_chance = 65
        self.events.append(Angry_Crabs())

    def process (self, world):
        '''Process the event. Populates a combat with Crabs.'''
        result = {}
        result["message"] = "All the Crabs have perished"
        monsters = []
        min = 7
        uplim = 13
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.Crabs("Crabs "+str(n)))
            n += 1
        display.announce ("You are attacked by a consortium of Crabs!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result

class Bomb(items.Item):
    def __init__(self):
        super().__init__("Pirate Bomb", 803) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (90,99)
        self.skill = "bombs"
        self.verb = "explode"
        self.verb2 = "explodes"
        self.usedUp = False

    def pickTargets(self, action, attacker, allies, enemies):
        return [enemies]
    
    def resolve(self, action, moving, chosen_targets):
        super().resolve(action, moving, chosen_targets)
        self.usedUp = True

class sparkle(items.Item):
    def __init__(self):
        super().__init__("Diamonds and Pearls", random.radint(100,300))

class Treasure:
    display.announce ("You have found Treasure!")
    def __init__ (self):
        chance = random.randint(1,100)
        if chance < 10:
            self.loot = Bomb
        elif chance < 30:
            self.loot = item.Flintlock
        elif chance < 40:
            self.loot = item.Cutlass
        elif chance < 50:
            self.loot = item.BelayingPin
        else:
            self.loot = sparkle

        config.the_player.add_to_inventory([self.loot])