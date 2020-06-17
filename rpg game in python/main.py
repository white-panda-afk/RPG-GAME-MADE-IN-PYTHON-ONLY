# import classes
from classes.game import Person, Bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
from time import sleep


# Create black magic abilities > name, cost, dmg, type
fire = Spell("Fire", 60, 500, "black")
thunder = Spell("Thunder", 60, 500, "black")
blizzard = Spell("Blizzard", 70, 500, "black")
Quake = Spell("Quake", 70, 500, "black")
metero = Spell("metero", 70, 500, "black")

# Create white mahic (heal) abilities > name, cost, dmg, type
cure = Spell("Cure", 40, 500, "white")
cura = Spell("Cura", 78, 500, "white")

# Create items  > name, type, description, prop
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
megaelixer = Item("MegaElixer", "elixer", "Fully restores party HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Create player inventory with items quantity
player_items = [{"item": potion, "quantity": 5},
                {"item": hipotion, "quantity": 15},
                {"item": superpotion, "quantity": 25},
                {"item":  elixer, "quantity": 13},
                {"item":  megaelixer, "quantity": 4},
                {"item": grenade, "quantity": 6}]

# Select player spells
player_spells = [fire, thunder, blizzard, metero, cure, cura]

# Select enemy spells
enemy_spells = [fire, metero, cure]

# initiate player with hp, mp, atk, df, magic, items
player1 = Person("Player1", 1000, 500, 100, 50, player_spells, player_items)
player2 = Person("Player2", 1000, 500, 100, 50, player_spells, player_items)
player3 = Person("Player3", 1000, 500, 100, 50, player_spells, player_items)

players = [player1, player2, player3]

# initiate enemies with hp, mp, atk, df, magic, items
enemy3 = Person("MicroMonster", 500, 250, 250, 25, enemy_spells, [])
enemy2 = Person("MiniMonster ", 1000, 500, 500, 50, enemy_spells, [])
enemy1 = Person("Monster     ", 2000, 1000, 200, 100, enemy_spells, [])

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

while running:

    # Print welcome message
    print("\n" + Bcolors.TITLE4 + " Simple Python RPG Battle " + Bcolors.ENDC)

    # Get All stats
    print("\n" + Bcolors.BOLD + "NAME         HP                                    MP            " + Bcolors.ENDC)
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    # Start playing
    for player in players:
        print("\n" + Bcolors.HEADER + "---------------------------" + "Your turn,", player.name + "---------------------------" + Bcolors.ENDC, "\n")
        player.get_stats()

        # Player: select attack or magic or item
        player.choose_action()
        print("Enter 0 to exit")
        choice = input("Choose Action:")
        index = int(choice) - 1

        # if player select attack > attack and print result
        if index == -1:
            exit()

        # if player select attack > attack and print result
        if index == 0:
            enemy = player.choose_target(enemies)
            dmg = player.generate_damage()
            enemies[enemy].take_damage(dmg)
            print("\n You attacked", enemies[enemy].name.replace(" ", ""), "for", dmg, "points of damage.")
            enemies[enemy].get_enemy_stats()

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name, "has died.")
                del enemies[enemy]

        # if player select magic > select spell
        elif index == 1:
            player.choose_magic()
            print("Type 0 to go back\n")
            magic_choice = int(input("Choose Magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            print("You Chose", spell.name)
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            # check if there is enough magic points for spell
            if spell.cost > current_mp:
                print(Bcolors.FAIL + "\nYou don't have enough magic points\n" + Bcolors.ENDC)
                continue

            # if player selected white magic > heal
            if spell.type == "white":
                player.heal(magic_dmg)
                print("\n You healed ! HP + ", magic_dmg, "points with ", spell.name, " And cost ", spell.cost)

            # if player selected black magic > attack
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print("\n You attacked", enemies[enemy].name.replace(" ", ""), "for", magic_dmg, "points of damage with ", spell.name, " And cost ", spell.cost, " :")
                enemies[enemy].get_enemy_stats()

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name, "has died.")
                    del enemies[enemy]

            player.reduce_mp(spell.cost)

        # if player select items > select item
        elif index == 2:
            player.choose_item()
            print("Type 0 to go back\n")
            item_choice = int(input("Choose Item:")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            # Check if player have enough quantity of this item
            if player.items[item_choice]["quantity"] == 0:
                print(Bcolors.FAIL + "\n" + "None left..." + Bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            # if player select item with type potion > heal
            if item.type == "potion":
                player.heal(item.prop)
                print(Bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + Bcolors.ENDC)

            # if player select item with type elixer > heal
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for p in players:
                        p.hp = p.maxhp
                        p.mp = p.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print("\n", item.name, ":", str(item.prop))
                print(Bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + Bcolors.ENDC)

            # if player select item with type attack > attack
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print("You attacked", enemies[enemy].name.replace(" ", ""), "for", item.prop, "points of damage with ", item.name)
                print(Bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage " + Bcolors.ENDC)
                enemies[enemy].get_enemy_stats()

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name, "has died.")
                    del enemies[enemy]

    # Check enemies & players for defeated / Battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if player won
    if defeated_enemies == 2:
        print(Bcolors.OKGREEN + "You Win!" + Bcolors.ENDC)
        running = False

        # Get team stats
        print("\n" + Bcolors.BOLD + "NAME         HP                                    MP            " + Bcolors.ENDC)
        for player in players:
            player.get_stats()
        print("\n")
        for enemy in enemies:
            enemy.get_enemy_stats()

    # Check if Enemy won
    elif defeated_players == 2:
        print(Bcolors.TITLE2 + "You enemies have defeated you!" + Bcolors.ENDC)
        running = False

        # Get team stats
        print("\n" + Bcolors.BOLD + "NAME         HP                                    MP            " + Bcolors.ENDC)
        for player in players:
            player.get_stats()
        print("\n")
        for enemy in enemies:
            enemy.get_enemy_stats()

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if len(players) == 1:
            target = 1
        elif len(players) > 1:
            target = random.randrange(0, (len(players) - 1))
        else:
            print(Bcolors.TITLE2 + "You enemies have defeated you!" + Bcolors.ENDC)
            running = False

        if enemy.get_mp() < 25:
            enemy_choice = 0

        # if enemy choice is 0 {attack} then attack
        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print("\n" + Bcolors.FAIL +
                  enemy.name.replace(" ", ""), "attacks", players[target].name, "for", enemy_dmg, "points of damage :"
                  + Bcolors.ENDC)
            players[target].get_stats()

            if players[target].get_hp() == 0:
                print(players[target].name, "has died.")
                del players[target]

        # if enemy choice is 0 {magic} then select spell
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            # if enemy spell is white magic > heal
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print("\n", enemy.name.replace(" ", ""), "Enemy healed ! HP +", magic_dmg, "points. with ", spell.name, " And cost ", spell.cost)
                enemy.get_stats()

            # if enemy spell is black magic > attack
            elif spell.type == "black":
                players[target].take_damage(magic_dmg)
                print("\n", Bcolors.FAIL +
                      enemy.name.replace(" ", ""), "'s attacked", players[target].name, "for", magic_dmg,
                      "points of damage, with", spell.name + Bcolors.ENDC)
                players[target].get_stats()

                if players[target].get_hp() == 0:
                    print(players[target].name, "has died.")
                    del players[target]

            enemy.reduce_mp(spell.cost)
