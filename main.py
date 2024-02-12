"""FITNESS RPG"""
"""LUKE BIENEMAN"""
"""ENAE380 Section 0105"""

import pickle
import random
import matplotlib.pyplot as plt

FIGHTER = {"str": 10, "dex": 8, "con": 9, "int": 6, "wis": 6, "cha": 6}
ROGUE = {"str": 6, "dex": 12, "con": 7, "int": 7, "wis": 6, "cha": 10}
WIZARD = {"str": 4, "dex": 5, "con": 6, "int": 12, "wis": 6, "cha": 4}
SORCERER = {"str": 4, "dex": 2, "con": 7, "int": 6, "wis": 12, "cha": 8}
BARD = {"str": 6, "dex": 6, "con": 8, "int": 6, "wis": 6, "cha": 11}

JEF = {"str": 20, "dex": 20, "con": 20, "int": 20, "wis": 20, "cha": 20}

PLAYER_TYPES = {"fighter": FIGHTER, "jef": JEF, "rogue": ROGUE, "wizard": WIZARD, "sorcerer": SORCERER, "bard": BARD}

GOBLIN = {"str": 5, "dex": 7, "con": 9, "int": 4, "wis": 2, "cha": 1}
OGRE = {"str": 17, "dex": 10, "con": 18, "int": 2, "wis": 2, "cha": 2}
WITCH = {"str": 5, "dex": 5, "con": 15, "int": 14, "wis": 12, "cha": 10}
SOLDIER = {"str": 14, "dex": 14, "con": 15, "int": 8, "wis": 5, "cha": 11}
WOLF = {"str": 7, "dex": 5, "con": 12, "int": 2, "wis": 2, "cha": 14}
GIANT = {"str": 20, "dex": 14, "con": 20, "int": 6, "wis": 16, "cha": 10}
LICH = {"str": 12, "dex": 14, "con": 17, "int": 21, "wis": 19, "cha": 19}

POOP = {"str": 21, "dex": 19, "con": 24, "int": 19, "wis": 19, "cha": 22}

ENEMY_TYPES = {"goblin": GOBLIN, "ogre": OGRE, "witch": WITCH, "soldier": SOLDIER, "wolf": WOLF, "giant": GIANT,
               "lich": LICH, "poo-titan": POOP}


def save_metrics(filename, **kwargs):
    """
    Save variables to a file using pickle.

    :param filename: Name of the file to save the variables
    :param kwargs: Dictionary of variable names and their corresponding values
    """
    try:
        with open(filename, 'wb') as file:
            pickle.dump(kwargs, file)
        print(f"Variables saved to {filename} successfully.")
    except Exception as e:
        print(f"Error occurred while saving variables: {e}")


def read_file(filename):
    """
    Read variables from a file saved using pickle.

    :param filename: Name of the file containing the variables
    :return: Dictionary containing the variables and their corresponding values
    """
    try:
        with open(filename, 'rb') as file:
            variables = pickle.load(file)
        print(f"Variables loaded from {filename} successfully.")
        return variables
    except Exception as e:
        print(f"Error occurred while reading variables: {e}")
        return None


def daily_data():
    """Daily survey that takes in data about workout, sleep, etc."""
    """Also addends current human metrics if necessary"""
    health_data = {}

    print("Please enter your daily health and exercise data:")

    date = input("Enter the date (MM/DD/YYYY): ")
    health_data['Date'] = date

    weight = float(input("Enter your weight (in lbs): "))
    health_data['Weight'] = weight

    macronutrients = {}
    print("\nEnter your macronutrient intake for the day (in grams):")
    protein = float(input("Protein intake: "))
    macronutrients['Protein'] = protein
    fats = float(input("Fat intake: "))
    macronutrients['Fats'] = fats
    carbs = float(input("Carbohydrate intake: "))
    macronutrients['Carbohydrates'] = carbs
    macronutrients['Calories'] = protein * 4 + carbs * 4 + fats * 9
    health_data['Macronutrients'] = macronutrients

    sleep_length = float(input("\nEnter hours of sleep: "))
    health_data['Sleep Length (hours)'] = sleep_length

    sleep_quality = float(input("Rate your sleep quality (1-10): "))
    health_data['Sleep Quality'] = sleep_quality

    exercise = input("\nWeightlifting performed (yes/no): ")
    health_data['Exercise'] = exercise

    cardio = input("Cardio performed (yes/no): ")
    health_data['Cardio'] = cardio

    return health_data


def log_health_data_to_file(filename, new_health_data):
    try:
        try:
            with open(filename, 'rb') as file:
                existing_data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            existing_data = {}

        if 'health_data' in existing_data:
            existing_data['health_data'].append(new_health_data)
        else:
            existing_data['health_data'] = [new_health_data]

        with open(filename, 'wb') as file:
            pickle.dump(existing_data, file)
            print("Health data logged successfully.")
    except Exception as e:
        print(f"Error occurred while logging health data: {e}")


def daily_data_experience(saved_data, health_data):
    """Experience gain based on daily data inputs and previous day gameplay"""
    daily_macros = health_data['Macronutrients']
    daily_cals = daily_macros['Calories']
    daily_protein = daily_macros['Protein']
    daily_fat = daily_macros['Fats']
    daily_carbs = daily_macros['Carbohydrates']
    daily_sleep_length = health_data['Sleep Length (hours)']
    daily_sleep_quality = health_data['Sleep Quality']
    daily_exercise = health_data['Exercise']
    daily_cardio = health_data['Cardio']

    goal_macros = saved_data['macros']
    goal_cals = goal_macros[0]
    goal_protein = goal_macros[1]
    goal_fat = goal_macros[2]
    goal_carbs = goal_macros[3]
    goal_sleep_length = 8
    goal_exercise = "yes"
    goal_cardio = "yes"
    goal = saved_data['metrics']['goal']

    experience = 0

    if goal.lower() == "bulk":
        if daily_cals >= goal_cals:
            experience += 3
        else:
            experience += 0

        if daily_protein >= goal_protein * .7:
            experience += 2
        else:
            experience += 0

        if (goal_fat * .9 <= daily_fat) and (daily_fat <= goal_fat * 1.6):
            experience += 1
        else:
            experience += 0

        if goal_carbs * .9 <= daily_carbs:
            experience += 1
        else:
            experience += 0

    elif goal.lower() == "cut":
        if daily_cals <= goal_cals:
            experience += 3
        else:
            experience += 0

        if daily_protein >= goal_protein * .7:
            experience += 2
        else:
            experience += 0

        if (goal_fat * .9 <= daily_fat) and (daily_fat <= goal_fat * 1.2):
            experience += 1
        else:
            experience += 0

        if (goal_carbs * .9 <= daily_carbs) and (goal_carbs * 1.2 >= daily_carbs):
            experience += 1
        else:
            experience += 0
    else:
        if (daily_cals <= goal_cals * 1.2) and (daily_cals >= goal_cals * .8):
            experience += 3
        else:
            experience += 0

        if daily_protein >= goal_protein * .7:
            experience += 2
        else:
            experience += 0

        if (goal_fat * .9 <= daily_fat) and (daily_fat <= goal_fat * 1.5):
            experience += 1
        else:
            experience += 0

        if (goal_carbs * .9 <= daily_carbs) and (goal_carbs * 1.4 >= daily_carbs):
            experience += 1
        else:
            experience += 0

    if daily_sleep_length >= goal_sleep_length:
        experience += 4
    elif daily_sleep_length >= goal_sleep_length - 2:
        experience += 2
    else:
        experience += 0

    experience += daily_sleep_quality * .5 - 1

    if daily_exercise == goal_exercise:
        experience += 8
    else:
        experience += 0

    if daily_cardio == goal_cardio:
        experience += 3
    else:
        experience += 0

    return experience


def graph_health_data(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            health_data = data.get('health_data', [])

        dates = []
        sleep_lengths = []
        macros = []
        protein = []
        fat = []
        carbs = []
        calories = []
        sleep_quality = []
        lifting = []
        cardio = []
        weight = []

        i = 0
        for entry in health_data:
            weight.append(entry.get('Weight'))
            dates.append(entry.get('Date'))
            sleep_lengths.append(entry.get('Sleep Length (hours)', 0))
            macros.append(entry.get('Macronutrients', 0))
            protein.append(macros[i]["Protein"])
            fat.append(macros[i]["Fats"])
            carbs.append(macros[i]["Carbohydrates"])
            calories.append(macros[i]["Calories"])
            sleep_quality.append(entry.get('Sleep Quality', 0))
            lifting.append(entry.get('Exercise'))
            cardio.append(entry.get('Cardio'))
            i += 1

        plt.figure(figsize=(10, 6))
        plt.plot(dates, weight, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Weight (lbs)')
        plt.title('Weight Over Time')
        plt.xticks(rotation=45)
        plt.ylim(min(weight) - 10, max(weight) + 10)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(dates, sleep_lengths, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Sleep Length (hours)')
        plt.title('Sleep Length Over Time')
        plt.xticks(rotation=45)
        plt.ylim(0, max(sleep_lengths) + 1)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(dates, sleep_quality, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Sleep Quality')
        plt.title('Sleep Quality Over Time')
        plt.xticks(rotation=45)
        plt.ylim(0, 11)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(dates, protein, marker='o', linestyle='-', label='protein')
        plt.plot(dates, fat, marker='v', linestyle='-', label='fats')
        plt.plot(dates, carbs, marker='^', linestyle='-', label='carbs')
        plt.xlabel('Date')
        plt.ylabel('Macros (g)')
        plt.legend()
        plt.title('Macros Over Time')
        plt.xticks(rotation=45)
        plt.ylim(0, max(carbs) + 100)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(dates, calories, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Calories')
        plt.title('Calories Over Time')
        plt.xticks(rotation=45)
        plt.ylim(0, max(calories) + 200)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(dates, lifting, marker='o', linestyle='-', label='weightlifting')
        plt.plot(dates, cardio, marker='^', linestyle='-', label='cardio')
        plt.xlabel('Date')
        plt.ylabel('Lifting or Cardio (yes/no')
        plt.title('Weightlifting and Cardio Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


    except FileNotFoundError:
        print("File not found. Please log data first.")
    except Exception as e:
        print(f"Error occurred while graphing data: {e}")


def level_up(saved_data, health_data):
    """"Controls if and when a character levels up based on experience"""
    experience = saved_data["experience"]
    gained_experience = daily_data_experience(saved_data, health_data)
    print(f"You gained {gained_experience} experience!")
    level = saved_data["level"]
    experience_to_level = level * 10
    total_experience = experience + gained_experience
    type_dict = saved_data['type_dict']
    if total_experience >= experience_to_level:
        experience = total_experience - experience_to_level
        level += 1
        print(f"You leveled up to level {level}!")
        print(f"Your current skill levels are: {type_dict}")
        skill_level_up = input("Choose which skill you want to level up (str / dex / con / int / wis / cha): ")
        type_dict[skill_level_up] += 1
    else:
        level = level
        experience = total_experience
    return level, experience, type_dict


def tdee_calculator(saved_data):
    """
    Calculate daily caloric needs based on height, weight, sex, age, and activity factor.

    Formula used: Harris-Benedict equation for BMR"""

    sex = saved_data['metrics']['sex']
    weight = float(saved_data['metrics']['weight'])
    height = float(saved_data['metrics']['height'])
    age = float(saved_data['metrics']['age'])
    activity = float(saved_data['metrics']['activity'])

    if sex.lower() == 'm':
        bmr = 66.4730 + (13.7516 * weight / 2.205) + (5.0033 * height / .3937) - (6.7550 * age)
    elif sex.lower() == 'f':
        bmr = 655.0955 + (9.5634 * weight / 2.205) + (1.8496 * height / .3937) - (4.6756 * age)
    else:
        return "Invalid sex input. Please provide 'm' or 'f'."

    tdee = bmr * activity
    return tdee


def macro_and_needs_calc(saved_data):
    goal = saved_data['metrics']['goal']
    tdee = saved_data['tdee']
    weight = saved_data['metrics']['weight']
    if goal.lower() == 'bulk':  # bulk
        calories = tdee + weight * 2.5
        protein = weight * 1.2
        fat = weight * .3
        carbs = (calories - protein * 4 - fat * 9) / 4
    elif goal.lower() == 'cut':  # cut
        calories = tdee - weight * 5
        protein = weight * 1.2
        fat = weight * .3
        carbs = (calories - protein * 4 - fat * 9) / 4
    else:  # maintain
        calories = tdee
        protein = weight
        fat = weight * .3
        carbs = (calories - protein * 4 - fat * 9) / 4

    macros = [calories, protein, fat, carbs]
    return macros


def workout_planner():
    """Workout Planner"""


class MainCharacter:
    """"Player Character stats and etc"""

    _str = 0
    _dex = 0
    _con = 0
    _int = 0
    _wis = 0
    _cha = 0

    level = 1
    experience = 0
    health = _con * 10 + _str * 2
    melee_atk = _str * 4 + _dex * 2
    ranged_atk = _str * 2 + _dex * 4
    fireball = _int * 5 + _wis * 2
    magic_missle = _int * 2 + _cha * 2
    heal = _wis + _cha + _int

    def __init__(self):
        self.char_type = None
        self.name = None

    def _assign_attributes(self):
        self.type_dict = PLAYER_TYPES[self.char_type]
        self._str = self.type_dict["str"]
        self._dex = self.type_dict["dex"]
        self._con = self.type_dict["con"]
        self._int = self.type_dict["int"]
        self._wis = self.type_dict["wis"]
        self._cha = self.type_dict["cha"]

    def character_creation(self):
        self.name = input("What is your name?: ")
        self.char_type = input("Enter your character type (fighter/rogue/wizard/sorcerer/bard): ")
        self._assign_attributes()


class HumanMetrics:
    """Human data like height, weight, etc"""
    _height = 0
    _weight = 0
    _age = 0
    _sex = 0
    _activity = 0

    def __init__(self):
        self.macros = None
        self._assign_metrics()
        self._tdee_calculator()
        self.macro_and_needs_calc()

    def _assign_metrics(self):
        self._goal = input("What are your goals? (Bulk/Maintain/Cut): ")
        self._height = float(input("Enter your height in inches: "))
        self._weight = float(input("Enter your weight in lbs: "))
        self._age = float(input("Enter your age in years: "))
        self._sex = input("Enter your sex (m/f): ")
        self._activity = float(input("""Enter your activity factor (examples below):
            Basal Metabolic Rate (BMR): 1
            Sedentary (little or no exercise): 1.2
            Lightly active (light exercise/sports 1-3 days/week): 1.375
            Moderately active (moderate exercise/sports 3-5 days/week): 1.55
            Very active (hard exercise/sports 6-7 days a week): 1.725
            Super active (very hard exercise & physical job or 2x training): 1.9
            ------> """))
        self.metrics = {"goal": self._goal, "height": self._height, "weight": self._weight, "age": self._age,
                        "sex": self._sex, "activity": self._activity}

    def _tdee_calculator(self):
        """
        Calculate daily caloric needs based on height, weight, sex, age, and activity factor.

        Formula used: Harris-Benedict equation for BMR"""

        if self._sex.lower() == 'm':
            self._bmr = 66.4730 + (13.7516 * self._weight / 2.205) + (5.0033 * self._height / .3937) - (
                    6.7550 * self._age)
        elif self._sex.lower() == 'f':
            self._bmr = 655.0955 + (9.5634 * self._weight / 2.205) + (1.8496 * self._height / .3937) - (
                    4.6756 * self._age)
        else:
            return "Invalid sex input. Please provide 'm' or 'f'."

        self._tdee = self._bmr * self._activity

    def macro_and_needs_calc(self):
        if self._goal.lower() == 'bulk':  # bulk
            calories = self._tdee + self._weight * 2.5
            protein = self._weight * 1.2
            fat = self._weight * .3
            carbs = (calories - protein * 4 - fat * 9) / 4
        elif self._goal.lower() == 'cut':  # cut
            calories = self._tdee + self._weight * 5
            protein = self._weight * 1.2
            fat = self._weight * .3
            carbs = (calories - protein * 4 - fat * 9) / 4
        else:  # maintain
            calories = self._tdee
            protein = self._weight
            fat = self._weight * .3
            carbs = (calories - protein * 4 - fat * 9) / 4

        self.macros = [calories, protein, fat, carbs]
        return self.macros


class Player:
    def __init__(self, name, level, str, dex, con, int, wis, cha):
        self.name = name
        self.level = level

        self.health = con * 10 + str * 2 + level * 5
        self.melee_atk = str * 4 + dex * 2
        self.ranged_atk = str * 2 + dex * 4
        self.fireball = int * 5 + wis * 2
        self.magic_missle = int * 2 + cha * 2 + wis * 2
        self.heal = wis + cha + int
        self.run = dex

    def melee_attack(self, enemy):
        damage = random.randint(5, 15) / 5 * self.melee_atk
        enemy.health -= damage
        print(f"{self.name} performs a physical attack and deals {damage} damage to the {enemy.name}!")

    def ranged_attack(self, enemy):
        damage = random.randint(1, 20) / 5 * self.ranged_atk
        enemy.health -= damage
        print(f"{self.name} uses a ranged attack and deals {damage} damage to the {enemy.name}!")

    def fireball_attack(self, enemy):
        damage = random.randint(10, 20) / 6 * self.fireball
        enemy.health -= damage
        print(f"{self.name} casts a fireball and deals {damage} damage to the {enemy.name}!")

    def magic_missle_attack(self, enemy):
        damage = self.magic_missle
        enemy.health -= damage
        print(f"{self.name} casts magic missle and deals {damage} damage to the {enemy.name}!")

    def heal_self(self):
        heal_amount = random.randint(15, 25) / 5 * self.heal
        self.health += heal_amount
        print(f"{self.name} heals for {heal_amount} health points!")

    def flee(self, enemy):
        flee = False
        run_chance = random.randint(1, 20) + self.run
        block_chance = random.randint(1, 20) + enemy.block
        if run_chance >= block_chance:
            print(f"{self.name} evades {enemy.name} and flees!")
            flee = True
            return flee
        if run_chance < block_chance:
            print(f"{enemy.name} blocks {self.name}'s escape!")
            return flee

class enemy:
    def __init__(self, name, str, dex, con, int, wis, cha):
        self.name = name
        self.health = con * 10 + str * 2
        self.melee_atk = str * 4 + dex * 2
        self.ranged_atk = str * 2 + dex * 4
        self.fireball = int * 5 + wis * 2
        self.magic_missle = int * 2 + cha * 2
        self.heal = wis + cha + int
        self.block = max(dex, int)

    def melee_attack(self, player):
        damage = random.randint(5, 15) / 6 * self.melee_atk
        player.health -= damage
        print(f"{self.name} performs a physical attack and deals {damage} damage to the {player.name}!")

    def ranged_attack(self, player):
        damage = random.randint(1, 20) / 6 * self.ranged_atk
        player.health -= damage
        print(f"{self.name} uses a ranged attack and deals {damage} damage to the {player.name}!")

    def fireball_attack(self, player):
        damage = random.randint(10, 20) / 8 * self.fireball
        player.health -= damage
        print(f"{self.name} casts a fireball and deals {damage} damage to the {player.name}!")

    def magic_missle_attack(self, player):
        damage = self.magic_missle / 1.2
        player.health -= damage
        print(f"{self.name} casts magic missle and deals {damage} damage to the {player.name}!")

    def heal_self(self):
        heal_amount = random.randint(15, 25) / 8 * self.heal
        self.health += heal_amount
        print(f"{self.name} heals for {heal_amount} health points!")


def battle(player, enemy):
    print(f"A wild {enemy.name} appears!\n")
    flee = False

    while player.health > 0 and enemy.health > 0 and flee is False:
        print(f"{player.name}'s Health: {player.health}")
        print(f"{enemy.name}'s Health: {enemy.health}\n")

        print("Choose your action:")
        print("1. Physical Attack")
        print("2. Ranged Attack")
        print("3. Fireball")
        print("4. Magic Missile")
        print("5. Heal")
        print("6. Run (Attempt to flee)")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            player.melee_attack(enemy)
        elif choice == '2':
            player.ranged_attack(enemy)
        elif choice == '3':
            player.fireball_attack(enemy)
        elif choice == '4':
            player.magic_missle_attack(enemy)
        elif choice == '5':
            player.heal_self()
        elif choice == '6':
            flee = player.flee(enemy)
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

        if enemy.health > 0 and flee is False:
            print("Enemy's turn")
            choice = random.randint(1, 5)
            if choice == 1:
                enemy.melee_attack(player)
            elif choice == 2:
                enemy.ranged_attack(player)
            elif choice == 3:
                enemy.fireball_attack(player)
            elif choice == 4:
                enemy.magic_missle_attack(player)
            elif choice == 5:
                enemy.heal_self()

    if player.health <= 0:
        print(f"{player.name} was defeated! Game Over.")
    elif flee is True:
        print(f"{player.name} escaped the {enemy.name}!")
    else:
        print(f"{player.name} defeated the {enemy.name}! Victory!")


def character_creation(filename):
    Character = MainCharacter()
    Character.character_creation()
    HumanData = HumanMetrics()
    save_metrics(filename, name=Character.name, level=Character.level, experience=Character.experience,
                 player_class=Character.char_type, metrics=HumanData.metrics, type_dict=Character.type_dict,
                 tdee=HumanData._tdee, macros=HumanData.macros)


def fitness_rpg_menu(filename, saved_data):
    print("Welcome to Fitness RPG!")
    health_log_filename = "Health_log_" + filename
    while True:
        print("\n===== Menu =====")
        print("1. Battle")
        print("2. Log Health Data")
        print("3. Change Player Data")
        print("4. Check Health Goals")
        print("5. Check Player Data")
        print("6. Check Health Graphs")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])

            print("Starting Battle...")
            player1 = Player(saved_data['name'], saved_data['level'], saved_data['type_dict']['str'],
                             saved_data['type_dict']['dex'], saved_data['type_dict']['con'],
                             saved_data['type_dict']['int'], saved_data['type_dict']['wis'],
                             saved_data['type_dict']['cha'])
            """Enemy Scaling"""
            lvl = float(saved_data['level'])
            enemy_list = ["goblin", "ogre", "witch", "soldier", "wolf", "giant", "lich", "poo-titan"]
            challenge_rating = [1, 6, 5, 4, 3, 8, 10]
            cr_sum = 0
            inv_cr = [(1 / number) for number in challenge_rating]
            for number in inv_cr: cr_sum += number
            normal_cr = [number / cr_sum for number in inv_cr]
            scaling = [pow(lvl, (1 + number / 10)) for number in challenge_rating]
            cr = []
            for i in range(len(challenge_rating)):
                cr.append(normal_cr[i] * scaling[i])
            cr_sum = 0
            for number in cr: cr_sum += number
            normal_cr = [number/cr_sum for number in cr]
            normal_cr.append(.01)
            """Enemy Choice"""
            enemy_name = random.choices(enemy_list, normal_cr, k=1)
            enemy_name = enemy_name[0]
            opponent = enemy(enemy_name, ENEMY_TYPES[enemy_name]['str'], ENEMY_TYPES[enemy_name]['dex'],
                             ENEMY_TYPES[enemy_name]['con'], ENEMY_TYPES[enemy_name]['int'],
                             ENEMY_TYPES[enemy_name]['wis'], ENEMY_TYPES[enemy_name]['cha'])
            battle(player1, opponent)

        elif choice == '2':
            print("Logging Health Data...")
            health_data = daily_data()
            level, experience, type_dict = level_up(saved_data, health_data)
            log_health_data_to_file(health_log_filename, health_data)

            saved_data['level'] = level
            saved_data['experience'] = experience
            saved_data['type_dict'] = type_dict
            saved_data['metrics']['weight'] = health_data['Weight']
            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])


        elif choice == '3':
            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])

            print("Changing Player Data...")
            change_items_list = ['goal', 'height', 'weight', 'age', 'sex', 'activity', 'esc']
            change_item = str(input(
                "What data do you want to change? (goal [Bulk/Maintain/Cut] / height [in] / weight [lbs] / age [yrs] / sex [m/f] / activity [range 1 to 2] / (esc to escape): "))
            while change_item.lower() not in change_items_list:
                print("Incorrect data type entered, please try again.")
                change_item = str(input(
                    "What data do you want to change? (goal [Bulk/Maintain/Cut] / height [in] / weight [lbs] / age [yrs] / sex [m/f] / activity [range 1 to 2] / (esc to escape)): "))
            if change_item.lower() == 'esc':
                break
            if change_item.lower() == 'sex' or 'goal':
                change = str(input("What would you like to change this to? "))
            else:
                change = float(input("What would you like to change this to? "))
            saved_data['metrics'][f'{change_item.lower()}'] = change

            tdee = tdee_calculator(saved_data)
            saved_data['tdee'] = tdee
            macros = macro_and_needs_calc(saved_data)
            saved_data['macros'] = macros
            print(f"Your new macros are {macros}")

            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])

        elif choice == '4':
            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])

            print("Check Health goals...")
            macros = saved_data['macros']
            # tdee calculator
            print(
                f"For Macro goals are => Calories: {macros[0]}, Protein: {macros[1]}, Fats: {macros[2]}, Carbs: {macros[3]}")
            print("Your sleep goal is 8 hours of great sleep")
            print("Your goal is to lift weights everyday")
            print("Your goal is to do cardio everyday")

        elif choice == '5':
            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])

            print("Checking Player Data")
            loaded_variables = read_file(filename)
            # Check the loaded variables
            saved_data = {}
            if loaded_variables:
                print("Saved Data:")
                for key, value in loaded_variables.items():
                    print(f"{key}: {value}")
                    saved_data[key] = value

        elif choice == '6':
            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])

            print("Checking Health Graphs")
            graph_health_data(health_log_filename)

        elif choice == '7':
            save_metrics(filename, name=saved_data['name'], level=saved_data['level'],
                         experience=saved_data['experience'],
                         player_class=saved_data['player_class'], metrics=saved_data['metrics'],
                         type_dict=saved_data['type_dict'],
                         tdee=saved_data['tdee'], macros=saved_data['macros'])

            print("Exiting Fitness RPG. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


def main():
    """Main Function"""
    main_menu = input("New or Load Game?: ")
    if main_menu.lower() == "new":
        filename = input("Enter a name for your savefile: ")
        filename += ".pkl"
        character_creation(filename)
        # create new file with character information
        print("Character Created: Please Load File")

    else:
        # loads existing save file
        filename = input("Enter a name of your savefile: ")
        filename += ".pkl"
        loaded_variables = read_file(filename)
        if loaded_variables is None:
            filename = input("Enter a name of your savefile: ")
            filename += ".pkl"
            loaded_variables = read_file(filename)
        # Check the loaded variables
        saved_data = {}
        if loaded_variables:
            print("Saved Data:")
            for key, value in loaded_variables.items():
                print(f"{key}: {value}")
                saved_data[key] = value

        Player = MainCharacter()
        Player.type_dict = saved_data['type_dict']
        Player.level = saved_data['level']
        Player.experience = saved_data['experience']

        """Menu"""
        fitness_rpg_menu(filename, saved_data)


if __name__ == "__main__":
    main()
