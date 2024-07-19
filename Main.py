from Classes.Game import person, bcolors
from Classes.Magic import spell
from Classes.Iventory import item
import random

# available magics

fire = spell("Fire", 5, 75, "Black")
Heal = spell("heal", 20, 75, "white")
Thunder = spell("thunder", 35, 175, "Black")

# Items

potion = item("Potion", "potion", "heals you for 50hp", 50)
mana_potion = item("Mana potion", "mana potion", "restores 25mp", 25)
Restorer = item("Restorer", "elixer", "fully restores you", 999999)
mega_restorer = item("Mega Restorer", "P_elixer", "Fully restores Everyone", 999)

grenade = item("grenade", "attack", "does 300 damage", 300)

# Unit instances

player_magic = [fire, Thunder, Heal]

player_inventory = [{"item": potion, "quantity": 2}, {"item": mana_potion, "quantity": 3},
                    {"item": Restorer, "quantity": 1}, {"item": mega_restorer, "quantity": 1},
                    {"item": grenade, "quantity": 1}]

# Units

player1 = person("P_Example1", 100, 50, 15, 5, player_magic, player_inventory)
player2 = person("P_Example2", 50, 200, 10, 0, player_magic, player_inventory)
player3 = person("P_Example3", 250, 10, 25, 10, player_magic, player_inventory)

enemy1 = person("E_Example1", 450, 20, 40, 10, [fire,], [])
enemy2 = person("E_Example2", 1000, 500, 10, 0, [Thunder, Heal], [])
enemy3 = person("E_Example3", 500, 50, 60, 45, [Heal], player_inventory)

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "You failed!" + bcolors.ENDC)

while running:
    print("===========================")

    print("\n\n")
    print("Name                         HP                                   MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(enemies[enemy].name, " takes:", bcolors.FAIL + str(dmg) + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + "got destroyed")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("choose magic")) - 1
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nDon't have enough mana\n" + bcolors.ENDC)
                continue

            if spell.type == "white":
                player.reduce_mp(spell.cost)
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "healing" + bcolors.ENDC)

            elif spell.type == "Black":
                player.reduce_mp(spell.cost)

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + "got destroyed")
                    del enemies[enemy]
                print("-----------------------------------")

            if magic_choice == -1:
                continue
        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "Don't have enough" + bcolors.ENDC)
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for ", item.prop, "HP" + bcolors.ENDC)

            elif item.type == "mana potion":
                player.mana_restore(item.prop)
                print(bcolors.OKBLUE + "\n" + item.name + "restores for ", item.prop, "MP" + bcolors.ENDC)

            elif item.type == "elixer":
                player.elixir()
                print(bcolors.OKGREEN + bcolors.BOLD + "\n" + item.name, "rejuvenates you completely" + bcolors.ENDC)

            elif item.type == "P_elixer":
                for i in players:
                    i.hp = i.maxhp
                    i.mp = i.maxmp
                print(bcolors.OKGREEN + bcolors.BOLD + "\n" + item.name, "rejuvenates everyone" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + bcolors.BOLD + "\n" + "the", item.name, "did", item.prop, "damage to " +
                      enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + "got destroyed")
                    del enemies[enemy]

# Makes sure there's a defeat
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print(bcolors.FAIL + bcolors.BOLD + "Every enemy has been defeated" + bcolors.ENDC)
        running = False

    elif defeated_players == 2:
        print(bcolors.FAIL + bcolors.BOLD + "You lost" + bcolors.ENDC)
        running = False

# Enemy attacks

    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            target = random.randrange(0, 3)

            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", ""), "attacks " + players[target].name.replace(" ", "") + enemy_dmg)

        elif enemy_choice == 1:
            magic_choice = random.randrange(0, len(enemy.magic))
            e_spell = enemy.magic[magic_choice]
            magic_dmg = e_spell.generate_damage()

            if enemy.mp < e_spell.cost:
