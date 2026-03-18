# Monster Battle Arena
# A turn-based monster battle game
# by Jack Hartman
# 3/3/2026

import random
import os

# all the type matchups - if the attacking type is strong against the defending type
# it does 2x damage, if its weak it does 0.5x
type_chart = {
    "Fire": {"Grass": 2.0, "Ice": 2.0, "Water": 0.5, "Rock": 0.5, "Fire": 0.5},
    "Water": {"Fire": 2.0, "Rock": 2.0, "Grass": 0.5, "Water": 0.5},
    "Grass": {"Water": 2.0, "Rock": 2.0, "Fire": 0.5, "Grass": 0.5},
    "Electric": {"Water": 2.0, "Electric": 0.5, "Rock": 0.5},
    "Rock": {"Fire": 2.0, "Ice": 2.0, "Water": 0.5, "Grass": 0.5},
    "Ice": {"Grass": 2.0, "Fire": 0.5, "Ice": 0.5, "Water": 0.5},
}

# all the monsters in the game
# i tried to make the stats balanced so no one monster is way better than the others
# the stat totals are all around 310-330
monsters = {
    "Emberclaw": {
        "name": "Emberclaw",
        "type": "Fire",
        "hp": 90,
        "attack": 85,
        "defense": 60,
        "speed": 75,
        "desc": "A fierce fire lizard with claws made of flame."
    },
    "Tidalfin": {
        "name": "Tidalfin",
        "type": "Water",
        "hp": 100,
        "attack": 70,
        "defense": 80,
        "speed": 65,
        "desc": "A tough water beast that can take a lot of hits."
    },
    "Thornvine": {
        "name": "Thornvine",
        "type": "Grass",
        "hp": 85,
        "attack": 75,
        "defense": 75,
        "speed": 80,
        "desc": "A plant monster covered in sharp thorns."
    },
    "Voltfang": {
        "name": "Voltfang",
        "type": "Electric",
        "hp": 75,
        "attack": 90,
        "defense": 55,
        "speed": 95,
        "desc": "Super fast electric wolf. Hits hard but kinda fragile."
    },
    "Bouldershell": {
        "name": "Bouldershell",
        "type": "Rock",
        "hp": 120,
        "attack": 80,
        "defense": 95,
        "speed": 35,
        "desc": "A giant rock turtle. Really slow but really tanky."
    },
    "Frostbite": {
        "name": "Frostbite",
        "type": "Ice",
        "hp": 80,
        "attack": 88,
        "defense": 65,
        "speed": 82,
        "desc": "An ice wolf that freezes everything around it."
    },
}

TEAM_SIZE = 3


def clear_screen():
    # clears the terminal so it looks cleaner
    os.system("cls" if os.name == "nt" else "clear")


def make_monster(name):
    # makes a copy of the monster from the catalog so we can change its hp
    # without messing up the original
    monster = dict(monsters[name])
    monster["current_hp"] = monster["hp"]
    return monster


def is_fainted(monster):
    # check if a monster is knocked out
    return monster["current_hp"] <= 0


def get_alive(team):
    # returns list of monsters that are still alive
    alive = []
    for m in team:
        if not is_fainted(m):
            alive.append(m)
    return alive


def all_fainted(team):
    # check if the whole team is knocked out
    return len(get_alive(team)) == 0


def get_type_multiplier(atk_type, def_type):
    # looks up the type effectiveness
    # returns 2.0 if super effective, 0.5 if not effective, 1.0 if normal
    if atk_type in type_chart:
        if def_type in type_chart[atk_type]:
            return type_chart[atk_type][def_type]
    return 1.0


def calc_damage(attacker, defender):
    # damage formula - attack squared divided by (attack + defense)
    # then multiply by type effectiveness and a random number so its not
    # the same every time
    # also 10% chance of critical hit which does 1.5x damage
    base = (attacker["attack"] ** 2) / (attacker["attack"] + defender["defense"])

    # type matchup
    multiplier = get_type_multiplier(attacker["type"], defender["type"])

    # random factor between 0.85 and 1.0
    rand = random.uniform(0.85, 1.0)

    # crit chance
    crit = False
    if random.random() < 0.10:
        crit = True
        crit_bonus = 1.5
    else:
        crit_bonus = 1.0

    damage = int(base * multiplier * rand * crit_bonus)
    if damage < 1:
        damage = 1  # always do at least 1 damage

    return damage, multiplier, crit


def show_hp_bar(current, maximum):
    # makes a little health bar out of characters
    bar_length = 20
    filled = int((current / maximum) * bar_length)
    empty = bar_length - filled
    bar = "#" * filled + "-" * empty
    return "[" + bar + "] " + str(current) + "/" + str(maximum)


# ---- MENU AND DISPLAY STUFF ----

def show_start_screen():
    clear_screen()
    print("")
    print("  ================================")
    print("     MONSTER BATTLE ARENA")
    print("  ================================")
    print("")
    print("  1) Play")
    print("  2) View Monsters")
    print("  3) Type Chart")
    print("  4) How to Play")
    print("  5) Quit")
    print("")


def show_monsters():
    # prints out all the monsters and their stats
    print("")
    print("  === MONSTER CATALOG ===")
    print("")
    count = 1
    for name in monsters:
        m = monsters[name]
        total = m["hp"] + m["attack"] + m["defense"] + m["speed"]
        print("  " + str(count) + ") " + name + " [" + m["type"] + "]")
        print("     HP: " + str(m["hp"]) + "  ATK: " + str(m["attack"]) +
              "  DEF: " + str(m["defense"]) + "  SPD: " + str(m["speed"]) +
              "  (Total: " + str(total) + ")")
        print("     " + m["desc"])
        print("")
        count += 1


def show_type_chart():
    # displays which types are strong/weak against which
    types = ["Fire", "Water", "Grass", "Electric", "Rock", "Ice"]
    print("")
    print("  TYPE CHART (rows attack, columns defend)")
    print("  2.0 = super effective, 0.5 = not effective, - = normal")
    print("")

    # print the header
    header = "           "
    for t in types:
        header += t.rjust(10)
    print(header)
    print("  " + "-" * 70)

    # print each row
    for atk in types:
        row = "  " + atk.rjust(9) + " |"
        for defn in types:
            mult = get_type_multiplier(atk, defn)
            if mult == 2.0:
                row += "      2.0x"
            elif mult == 0.5:
                row += "      0.5x"
            else:
                row += "         -"
        print(row)
    print("")


def show_how_to_play():
    print("")
    print("  === HOW TO PLAY ===")
    print("")
    print("  - Each player picks 3 monsters for their team")
    print("  - Players cant pick the same monster")
    print("  - Each turn you can Attack or Swap to a different monster")
    print("  - Whoever has the faster monster goes first")
    print("  - Type matchups matter (like pokemon) - check the type chart!")
    print("  - When a monster hits 0 HP it faints and you pick a new one")
    print("  - You lose when all your monsters faint")
    print("  - There is a 10% chance of a critical hit each attack")
    print("")


def show_battle_state(p1_monster, p2_monster, p1_name, p2_name):
    # shows both monsters and their health bars during battle
    print("")
    print("  --------------------------------")
    print("  " + p2_name + "'s " + p2_monster["name"] + " (" + p2_monster["type"] + ")")
    print("  HP: " + show_hp_bar(p2_monster["current_hp"], p2_monster["hp"]))
    print("")
    print("  " + p1_name + "'s " + p1_monster["name"] + " (" + p1_monster["type"] + ")")
    print("  HP: " + show_hp_bar(p1_monster["current_hp"], p1_monster["hp"]))
    print("  --------------------------------")


# ---- TEAM PICKING ----

def pick_team(player_name, already_taken):
    # lets a player pick 3 monsters for their team
    # already_taken is a list of names the other player already picked
    available = []
    for name in monsters:
        if name not in already_taken:
            available.append(name)

    team = []
    while len(team) < TEAM_SIZE:
        print("")
        print("  " + player_name + ", pick monster " + str(len(team) + 1) + "/" + str(TEAM_SIZE) + ":")
        for i in range(len(available)):
            m = monsters[available[i]]
            print("    " + str(i + 1) + ") " + available[i] + " [" + m["type"] + "] - " +
                  "HP:" + str(m["hp"]) + " ATK:" + str(m["attack"]) +
                  " DEF:" + str(m["defense"]) + " SPD:" + str(m["speed"]))

        choice = input("  Enter number: ")
        try:
            idx = int(choice) - 1
            if idx >= 0 and idx < len(available):
                picked = available[idx]
                team.append(make_monster(picked))
                available.remove(picked)
                print("  " + picked + " added to " + player_name + "'s team!")
            else:
                print("  Thats not a valid choice, try again")
        except:
            print("  Please type a number")

    return team


# ---- BATTLE ACTIONS ----

def pick_action(player_name, active_monster, team):
    # lets the player choose to attack or swap
    # returns a tuple like ("attack", None) or ("swap", monster_to_swap_to)
    bench = []
    for m in team:
        if not is_fainted(m) and m is not active_monster:
            bench.append(m)

    print("")
    print("  " + player_name + "'s turn - Active: " + active_monster["name"] +
          " (HP: " + str(active_monster["current_hp"]) + "/" + str(active_monster["hp"]) + ")")
    print("    1) Attack")
    if len(bench) > 0:
        print("    2) Swap")

    while True:
        choice = input("  What do you want to do? ")

        if choice == "1":
            return ("attack", None)
        elif choice == "2" and len(bench) > 0:
            # show the swap options
            print("")
            print("  Pick a monster to swap to:")
            for i in range(len(bench)):
                m = bench[i]
                print("    " + str(i + 1) + ") " + m["name"] + " [" + m["type"] + "] - HP: " +
                      str(m["current_hp"]) + "/" + str(m["hp"]))
            while True:
                swap_pick = input("  Enter number: ")
                try:
                    si = int(swap_pick) - 1
                    if si >= 0 and si < len(bench):
                        return ("swap", bench[si])
                    else:
                        print("  Invalid choice")
                except:
                    print("  Please type a number")
        else:
            print("  Invalid choice, try again")


def forced_swap(player_name, team):
    # when your monster faints you have to pick a new one
    alive = get_alive(team)
    if len(alive) == 0:
        return None

    # if theres only one left just send it out automatically
    if len(alive) == 1:
        print("  " + player_name + " sends in " + alive[0]["name"] + "!")
        return alive[0]

    print("")
    print("  " + player_name + ", your monster fainted! Pick a new one:")
    for i in range(len(alive)):
        m = alive[i]
        print("    " + str(i + 1) + ") " + m["name"] + " [" + m["type"] + "] - HP: " +
              str(m["current_hp"]) + "/" + str(m["hp"]))

    while True:
        choice = input("  Enter number: ")
        try:
            idx = int(choice) - 1
            if idx >= 0 and idx < len(alive):
                print("  " + player_name + " sends in " + alive[idx]["name"] + "!")
                return alive[idx]
            else:
                print("  Invalid choice")
        except:
            print("  Please type a number")


def do_attack(attacker, defender, attacker_name):
    # does the attack and prints what happened
    damage, multiplier, crit = calc_damage(attacker, defender)

    # subtract the hp
    defender["current_hp"] = defender["current_hp"] - damage
    if defender["current_hp"] < 0:
        defender["current_hp"] = 0

    # print the battle log
    print("  " + attacker_name + "'s " + attacker["name"] + " attacks " +
          defender["name"] + " for " + str(damage) + " damage!")

    if crit:
        print("  *** CRITICAL HIT! ***")
    if multiplier > 1.0:
        print("  Its super effective!")
    elif multiplier < 1.0:
        print("  Its not very effective...")

    print("  " + defender["name"] + " HP: " + show_hp_bar(defender["current_hp"], defender["hp"]))

    if is_fainted(defender):
        print("  " + defender["name"] + " fainted!")


def do_turn(p1_action, p2_action, p1_active, p2_active, p1_name, p2_name):
    # resolves one full turn
    # swaps always go first, then attacks in speed order

    new_p1 = p1_active
    new_p2 = p2_active

    # do swaps first (they happen before attacks)
    if p1_action[0] == "swap":
        new_p1 = p1_action[1]
        print("")
        print("  " + p1_name + " swaps to " + new_p1["name"] + "!")
    if p2_action[0] == "swap":
        new_p2 = p2_action[1]
        print("")
        print("  " + p2_name + " swaps to " + new_p2["name"] + "!")

    # now do attacks
    p1_attacks = (p1_action[0] == "attack")
    p2_attacks = (p2_action[0] == "attack")

    if p1_attacks and p2_attacks:
        # both players attack - faster one goes first
        if new_p1["speed"] > new_p2["speed"]:
            # player 1 is faster
            do_attack(new_p1, new_p2, p1_name)
            if not is_fainted(new_p2):
                do_attack(new_p2, new_p1, p2_name)
        elif new_p2["speed"] > new_p1["speed"]:
            # player 2 is faster
            do_attack(new_p2, new_p1, p2_name)
            if not is_fainted(new_p1):
                do_attack(new_p1, new_p2, p1_name)
        else:
            # same speed - pick randomly
            if random.random() < 0.5:
                do_attack(new_p1, new_p2, p1_name)
                if not is_fainted(new_p2):
                    do_attack(new_p2, new_p1, p2_name)
            else:
                do_attack(new_p2, new_p1, p2_name)
                if not is_fainted(new_p1):
                    do_attack(new_p1, new_p2, p1_name)
    elif p1_attacks:
        do_attack(new_p1, new_p2, p1_name)
    elif p2_attacks:
        do_attack(new_p2, new_p1, p2_name)

    return new_p1, new_p2


# ---- SCOREBOARD ----

def show_scoreboard(p1_team, p2_team, p1_name, p2_name):
    # shows who won and the final stats
    print("")
    print("  ================================")
    print("       FINAL SCOREBOARD")
    print("  ================================")

    p1_alive = get_alive(p1_team)
    p2_alive = get_alive(p2_team)

    # score is total hp remaining
    p1_score = 0
    for m in p1_alive:
        p1_score += m["current_hp"]
    p2_score = 0
    for m in p2_alive:
        p2_score += m["current_hp"]

    # print player 1 team
    print("")
    print("  " + p1_name + ": " + str(len(p1_alive)) + "/" + str(len(p1_team)) +
          " monsters alive (HP remaining: " + str(p1_score) + ")")
    for m in p1_team:
        if is_fainted(m):
            print("    - " + m["name"] + ": FAINTED")
        else:
            print("    - " + m["name"] + ": " + str(m["current_hp"]) + "/" + str(m["hp"]) + " HP")

    # print player 2 team
    print("")
    print("  " + p2_name + ": " + str(len(p2_alive)) + "/" + str(len(p2_team)) +
          " monsters alive (HP remaining: " + str(p2_score) + ")")
    for m in p2_team:
        if is_fainted(m):
            print("    - " + m["name"] + ": FAINTED")
        else:
            print("    - " + m["name"] + ": " + str(m["current_hp"]) + "/" + str(m["hp"]) + " HP")

    # announce winner
    print("")
    print("  ================================")
    if all_fainted(p2_team):
        print("  " + p1_name + " WINS!!!")
    elif all_fainted(p1_team):
        print("  " + p2_name + " WINS!!!")
    print("  Score: " + p1_name + " " + str(p1_score) + " - " + str(p2_score) + " " + p2_name)
    print("  ================================")


# ---- MAIN GAME ----

def play_battle():
    # this runs a full battle from start to finish
    clear_screen()
    print("")
    print("  Enter player names:")
    p1_name = input("  Player 1: ").strip()
    if p1_name == "":
        p1_name = "Player 1"
    p2_name = input("  Player 2: ").strip()
    if p2_name == "":
        p2_name = "Player 2"

    # player 1 picks their team
    clear_screen()
    show_monsters()
    print("  " + p1_name + ", build your team!")
    p1_team = pick_team(p1_name, [])

    # player 2 picks (cant pick what p1 already took)
    clear_screen()
    show_monsters()
    taken = []
    for m in p1_team:
        taken.append(m["name"])
    print("  " + p2_name + ", build your team!")
    print("  (Already taken: " + ", ".join(taken) + ")")
    p2_team = pick_team(p2_name, taken)

    # start the battle
    clear_screen()
    print("")
    print("  ================================")
    print("       BATTLE START!")
    print("  ================================")

    # first monster on each team starts
    p1_active = p1_team[0]
    p2_active = p2_team[0]
    print("  " + p1_name + " sends out " + p1_active["name"] + "!")
    print("  " + p2_name + " sends out " + p2_active["name"] + "!")

    turn = 1

    # main battle loop - keeps going until one team is all fainted
    while not all_fainted(p1_team) and not all_fainted(p2_team):
        print("")
        print("  ======== TURN " + str(turn) + " ========")
        show_battle_state(p1_active, p2_active, p1_name, p2_name)

        # both players pick what they want to do
        p1_action = pick_action(p1_name, p1_active, p1_team)
        print()
        p2_action = pick_action(p2_name, p2_active, p2_team)

        # resolve the turn
        print("")
        print("  --- Turn " + str(turn) + " Results ---")
        p1_active, p2_active = do_turn(
            p1_action, p2_action,
            p1_active, p2_active,
            p1_name, p2_name
        )

        # if someones monster fainted, they have to swap
        if is_fainted(p1_active) and not all_fainted(p1_team):
            p1_active = forced_swap(p1_name, p1_team)
        if is_fainted(p2_active) and not all_fainted(p2_team):
            p2_active = forced_swap(p2_name, p2_team)

        turn += 1
        input("\n  Press Enter to continue...")

    # game over - show results
    clear_screen()
    show_scoreboard(p1_team, p2_team, p1_name, p2_name)
    input("\n  Press Enter to go back to menu...")


def main():
    # main menu loop
    while True:
        show_start_screen()
        choice = input("  Enter choice: ")

        if choice == "1":
            play_battle()
        elif choice == "2":
            clear_screen()
            show_monsters()
            input("  Press Enter to go back...")
        elif choice == "3":
            clear_screen()
            show_type_chart()
            input("  Press Enter to go back...")
        elif choice == "4":
            clear_screen()
            show_how_to_play()
            input("  Press Enter to go back...")
        elif choice == "5":
            print("  Thanks for playing!")
            break
        else:
            print("  Invalid choice")
            input("  Press Enter to continue...")


# run the game
if __name__ == "__main__":
    main()
