from dataclasses import dataclass
import random


@dataclass
class Hero:
    """A super-class for heroes"""
    base_attack_time: float
    basic_attack_speed: int
    basic_damage: int
    basic_armor: float
    basic_hit_point: int
    basic_regeneration: int
    main_attribute: str  # Intelligence or Strength or Agility

    basic_strength: float
    basic_agility: float
    strength_level_growth: float
    agility_level_growth: float

    bonus_strength: int
    bonus_agility: int
    bonus_damage_without_main_attribute: int
    # there are more than 1 skill can grant evasion ability
    evasion_list: dict  # key: skill name, value: int, evasion possibility

    bonus_attack_speed_without_agility: int
    bonus_armor_without_agility: int
    bonus_regeneration_without_strength: int
    bonus_hit_point_without_strength: int

    skill_list: dict
    attack_attachment: dict
    other_positive_effect: dict
    other_negative_effect: dict
    # there are more than 1 skill can grant critical attack ability
    critical_list: dict  # key: skill name, value: list, [possibility, critical rate]

    hero_level: int

    status: dict

    def learn_skill_book(self, skill_name: str, qty_of_books: int):
        """
        This function is a common function when a skill book is consumed.
        This function determines how many levels the skill will improve.

        :param skill_name: the skill that this Skill Book is bounded to.
        :param qty_of_books: how many skill books -Attribute Bonus- are consumed
        :return: [original_level, new_level]
                 original_level: how many levels this skill was before consuming the skill book(s);
                 new_level: after consuming the skill book(s), the skill comes to which level
        """
        if skill_name in self.skill_list.keys():
            # learned before
            original_level = self.skill_list[skill_name]
            new_level = min(10, original_level + qty_of_books)
            self.skill_list[skill_name] = new_level
            return [original_level, new_level]
        else:
            # a new skill
            new_level = min(10, qty_of_books)
            self.skill_list[skill_name] = new_level
            return [0, new_level]

    def check_able_to_learn_skill_book(self, skill_name: str):
        """
        To judge if the hero can learn this Skill Book.

        :param skill_name: the skill name that this skill book is bounded to
        :return: boolean value, True means hero can consume this book
        """
        if skill_name in self.skill_list.keys():
            if self.skill_list[skill_name] == 10:
                return False
            else:
                return True
        elif len(self.skill_list.keys()) >= 4:
            return False
        else:
            return True

    def learn_skill_attribute_bonus(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Attribute Bonus-.

        :param qty_of_books: how many skill books -Attribute Bonus- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Attribute Bonus"):
            return None
        original_level, new_level = self.learn_skill_book("Attribute Bonus", qty_of_books)
        self.bonus_strength += 5 * (new_level - original_level)
        self.bonus_agility += 5 * (new_level - original_level)

    def learn_skill_evasion(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Evasion-.

        :param qty_of_books: how many skill books -Evasion- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Evasion"):
            return None
        _, new_level = self.learn_skill_book("Evasion", qty_of_books)
        self.evasion_list["Evasion"] = 30 + 5 * new_level

    def learn_skill_corruption(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Corruption-.

        :param qty_of_books: how many skill books -Corruption- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Corruption"):
            return None
        _, new_level = self.learn_skill_book("Corruption", qty_of_books)
        self.other_positive_effect["Reduce Enemy Armor"] = 2 * new_level

    def learn_skill_armor_bonus(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Armor Bonus-.

        :param qty_of_books: how many skill books -Armor Bonus- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Armor Bonus"):
            return None
        original_level, new_level = self.learn_skill_book("Armor Bonus", qty_of_books)
        if original_level == 0:
            self.bonus_armor_without_agility += 5 + 2 * new_level
        else:
            self.bonus_armor_without_agility += 2 * new_level

    def learn_skill_thorn_armor(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Thorn Armor-.

        :param qty_of_books: how many skill books -Thorn Armor- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Thorn Armor"):
            return None
        original_level, new_level = self.learn_skill_book("Thorn Armor", qty_of_books)
        self.bonus_armor_without_agility += (new_level - original_level)
        self.other_positive_effect["Physical Damage Reflection"] = 5 * new_level

    def learn_curse_of_death(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Curse of Death-.

        :param qty_of_books: how many skill books -Curse of Death- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Curse of Death"):
            return None
        _, new_level = self.learn_skill_book("Curse of Death", qty_of_books)
        if new_level <= 4:
            self.other_positive_effect["Curse Damage"] = new_level * 10
        elif new_level <= 8:
            self.other_positive_effect["Curse Damage"] = new_level * 20 - 40
        elif new_level == 9:
            self.other_positive_effect["Curse Damage"] = 150
        else:
            self.other_positive_effect["Curse Damage"] = 200
        self.other_positive_effect["Curse Reg Reduction"] = 20 + 5 * new_level

    def learn_fire(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Fire!-.

        :param qty_of_books: how many skill books -Fire!- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Fire!"):
            return None
        _, new_level = self.learn_skill_book("Fire!", qty_of_books)
        self.other_positive_effect["Ignore Armor"] = 10 + 5 * new_level

    def learn_crushing(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Crushing-.

        :param qty_of_books: how many skill books -Crushing- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Crushing"):
            return None
        _, new_level = self.learn_skill_book("Crushing", qty_of_books)
        self.attack_attachment["Crushing"] = new_level

    def learn_damage_bonus(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Damage Bonus-.

        :param qty_of_books: how many skill books -Damage Bonus- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Damage Bonus"):
            return None
        original_level, new_level = self.learn_skill_book("Damage Bonus", qty_of_books)
        if original_level == 0:
            self.bonus_damage_without_main_attribute += 30 + 25 * new_level
        else:
            self.bonus_damage_without_main_attribute += 25 * (new_level - original_level)

    def learn_life_steal(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Life Steal-.

        :param qty_of_books: how many skill books -Life Steal- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Life Steal"):
            return None
        _, new_level = self.learn_skill_book("Life Steal", qty_of_books)
        self.attack_attachment["Life Steal"] = new_level

    def learn_smash(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Smash-.

        :param qty_of_books: how many skill books -Smash- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Smash"):
            return None
        _, new_level = self.learn_skill_book("Smash", qty_of_books)
        self.attack_attachment["Smash"] = new_level

    def equip_monkey_king_bar(self, equip_or_take_off: int) -> None:
        """
        When hero equips MKB

        :param equip_or_take_off: 1 means equip MKB, -1 means take off MKB, could be 2 or more
        :return: None
        """
        self.basic_attack_speed += 45 * equip_or_take_off
        self.bonus_damage_without_main_attribute += 40 * equip_or_take_off
        if "MKB" in self.attack_attachment.keys():
            self.attack_attachment["MKB"] += equip_or_take_off
        else:
            self.attack_attachment["MKB"] = equip_or_take_off

    def equip_heart_of_tarrasque(self, equip_or_take_off: int) -> None:
        """
        When hero equips Heart of Tarrasque

        :param equip_or_take_off: 1 means equip Heart of Tarrasque,
                                  -1 means take off Heart of Tarrasque, could be 2 or more
        :return: None
        """
        self.bonus_strength += 45 * equip_or_take_off
        self.bonus_hit_point_without_strength += 250 * equip_or_take_off
        if "Heart" in self.other_positive_effect.keys():
            self.other_positive_effect["Heart"] += equip_or_take_off
        else:
            self.other_positive_effect["Heart"] = equip_or_take_off

    def calculate_status(self):
        """
        All parameters are set, calculate attack, armor and other attributes.
        The final attributes are described through a dict, status

        :return: None
        """
        self.status["Strength"] = self.basic_strength + self.hero_level * self.strength_level_growth \
                                  + self.bonus_strength
        self.status["Agility"] = self.basic_agility + self.hero_level * self.agility_level_growth + self.bonus_agility
        if self.main_attribute == 'Strength':
            damage_from_attribute = self.status["Strength"]
        elif self.main_attribute == 'Agility':
            damage_from_attribute = self.status["Agility"]
        else:
            raise Exception("Main Attribute Error, should be Strength or Intelligence or Agility")
        self.status['Damage'] = self.basic_damage + self.bonus_damage_without_main_attribute + damage_from_attribute
        self.status["Max HP"] = self.basic_hit_point + self.status["Strength"] * 20 \
                                + self.bonus_hit_point_without_strength
        self.status["Armor"] = self.basic_armor + 0.16 * self.status["Agility"] + self.bonus_armor_without_agility
        self.status["Attack Speed"] = self.basic_attack_speed + self.status["Agility"] \
                                      + self.bonus_attack_speed_without_agility
        # Base Attack Time ÷ (1 + (Increased Attack Speed ÷ 100)) = Attack Speed
        self.status["Attack Interval"] = self.base_attack_time / (1 + self.status["Attack Speed"] / 100)
        self.status["Current HP"] = self.status["Max HP"]
        self.status["Regeneration"] = self.basic_regeneration + self.status["Strength"] / 10
        if "Heart" in self.other_positive_effect.keys():
            self.status["Regeneration"] += self.other_positive_effect["Heart"] * 0.016 * self.status["Max HP"]
        self.status["Physical Resistance"] = 1 - (0.052 * self.status["Armor"]) / (
                0.9 + 0.048 * abs(self.status["Armor"]))
        self.status["Magic Resistance"] = 0.25
        self.status["Pierce"] = {}
        if "MKB" in self.attack_attachment.keys():
            self.status["Pierce"]["MKB"] = pierce_possibility_mkb(self.attack_attachment["MKB"]) * 100

    def taken_physical_damage(self, physical_damage_amount: float) -> int:
        """


        :param physical_damage_amount: Damage Amount before calculating Armor
        :return: Actual damage caused
        """
        actual_damage = physical_damage_amount * self.status["Physical Resistance"]
        actual_damage = round(actual_damage)
        self.status["Current HP"] -= actual_damage
        return actual_damage

    def taken_magical_damage(self, magical_damage_amount: float) -> int:
        """


        :param magical_damage_amount: Damage Amount before calculating Armor
        :return: Actual damage caused
        """
        actual_damage = magical_damage_amount * (1 - self.status["Magic Resistance"])
        actual_damage = round(actual_damage)
        self.status["Current HP"] -= actual_damage
        return actual_damage

    def taken_true_damage(self, true_damage_amount: float) -> int:
        """


        :param true_damage_amount: Damage Amount
        :return: Actual damage caused
        """
        actual_damage = round(true_damage_amount)
        self.status["Current HP"] -= actual_damage
        return actual_damage

    def regenerate_and_curse(self, time_second: float) -> None:
        """
        Calculate hit point regenerate during time period.

        :param time_second: how mang seconds have passed
        :return: None
        """
        regenerate_hp = self.status["Regeneration"] * time_second

        if "Curse" in self.other_negative_effect.keys():
            # other_negative_effect["Curse"] : level of curse
            # other_negative_effect["Curse Reg Reduction"] : how many percent regenerate reduced
            # other_negative_effect["Curse Damage"] : curse damage per second
            regenerate_hp = self.other_negative_effect["Curse Reg Reduction"] / 100 * regenerate_hp
            regenerate_hp -= self.other_negative_effect["Curse Damage"] * time_second

        self.status["Current HP"] = min(self.status["Max HP"], self.status["Current HP"] + regenerate_hp)


def attack(attack_hero: Hero, defend_hero: Hero):
    attack_damage = attack_hero.status['Damage']
    # evadable physical damage, evadable magic damage, evadable true damage
    # un-evadable physical damage, un-evadable magic damage, un-evadable true damage
    # self-taken physical damage (comes from skills like Thorn Armor), self-taken magic damage
    damage_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    evaded = False
    pierce = False

    if attack_hero.status["Current HP"] <= 0 or defend_hero.status["Current HP"] <= 0:
        # one side has already been killed before attack
        # for example, die because of the damage from Curse of Death
        return damage_list

    # calculate un-evadable damage first
    # in our model, only Smash is un-evadable
    if 'Smash' in attack_hero.skill_list.keys():
        skill_level = attack_hero.skill_list['Smash']
        damage_list[3] += 100 * skill_level  # Basic damage
        damage_list[3] += 0.01 * skill_level * defend_hero.status["Max HP"]  # decided by enemy max HP

    # calculate if this attack is evaded
    random_num = random.randint(0, 100)

    for key in attack_hero.status["Pierce"].keys():
        if random_num < attack_hero.attack_attachment["Pierce"][key]:
            pierce = True
            if key == "MKB":
                # un-evadable magic damage from MKB
                damage_list[4] += 70

    if pierce:
        # MKB pierced, cannot evade
        pass
    else:
        # MKB not triggered, can evade
        if len(defend_hero.evasion_list.keys()) != 0:
            for evasion_skill in defend_hero.evasion_list:
                evasion_possibility = defend_hero.evasion_list[evasion_skill]
                if random.randint(0, 100) < evasion_possibility:
                    # evade successfully
                    evaded = True
                    break
    if evaded:
        damage_calculation(attack_hero, defend_hero, damage_list)
        return damage_list

    highest_critical_rate = 100

    # attack might be critical
    # each critical is independent, the final damage only counts the highest critical rate
    if len(attack_hero.critical_list.keys()) != 0:
        for critical_skill in attack_hero.critical_list:
            if random.randint(0, 100) <= attack_hero.critical_list[critical_skill][0]:
                highest_critical_rate = max(highest_critical_rate, attack_hero.critical_list[critical_skill][1])

    damage_list[0] += highest_critical_rate / 100 * attack_damage

    # TODO
    # Other attack attachments


def damage_calculation(attack_hero: Hero, defend_hero: Hero, damage_list) -> None:
    """

    :param attack_hero:
    :param defend_hero:
    :param damage_list:
        # evadable physical damage, evadable magic damage, evadable true damage
        # un-evadable physical damage, un-evadable magic damage, un-evadable true damage
        # self-taken physical damage (comes from skills like Thorn Armor), self-taken magic damage
    :return: None
    """
    defend_hero.taken_physical_damage(damage_list[0] + damage_list[3])
    defend_hero.taken_magical_damage(damage_list[1] + damage_list[4])
    defend_hero.taken_true_damage(damage_list[2] + damage_list[5])
    attack_hero.taken_physical_damage(damage_list[6])
    attack_hero.taken_magical_damage(damage_list[7])
    attack_hero.taken_true_damage(damage_list[8])


def pierce_possibility_mkb(amount_of_mkb: int) -> float:
    """
    If MKB is equipped, each MKB will grant 80% chance to pierce through evasion and deal 70 magic damage
    Equipping 2 MKB, possibility of piercing is: 80% + (1-80%)*80%

    :param amount_of_mkb:
    :return: the possibility of triggering mkb
    """
    if amount_of_mkb == 1:
        return 0.8
    else:
        return 0.8 + 0.2 * pierce_possibility_mkb(amount_of_mkb - 1)


def duel(hero_1: Hero, hero_2: Hero):
    hero_1_attack_time_axis = hero_1.status["Attack Interval"]
    hero_2_attack_time_axis = hero_1.status["Attack Interval"]
    last_hit_time_axis = 0
    hero_1_attacked = False
    hero_2_attacked = False

    while True:
        if hero_1_attack_time_axis < hero_2_attack_time_axis:
            # before attack, calculate regeneration and curse damage
            time = hero_1_attack_time_axis - last_hit_time_axis
            hero_1.regenerate_and_curse(time)
            hero_2.regenerate_and_curse(time)
            last_hit_time_axis = hero_1_attack_time_axis

            # attack
            attack(hero_1, hero_2)
            hero_1_attacked = True

        elif hero_1_attack_time_axis > hero_2_attack_time_axis:
            time = hero_2_attack_time_axis - last_hit_time_axis
            hero_1.regenerate_and_curse(time)
            hero_2.regenerate_and_curse(time)
            last_hit_time_axis = hero_2_attack_time_axis
            attack(hero_2, hero_1)
            hero_2_attacked = True
        else:
            # attack at same time, randomly decide sequence of attack
            time = hero_1_attack_time_axis - last_hit_time_axis
            hero_1.regenerate_and_curse(time)
            hero_2.regenerate_and_curse(time)
            last_hit_time_axis = hero_2_attack_time_axis
            if random.randint(0, 1) == 0:
                attack(hero_1, hero_2)
                hero_1_attacked = True
            else:
                attack(hero_2, hero_1)
                hero_2_attacked = True

        if hero_1.status["Current HP"] <= 0 or hero_2.status["Current HP"] <= 0:
            break

        if not hero_1_attacked:
            hero_1_attack_time_axis += hero_1.status["Attack Interval"]
            hero_1_attacked = False
        if not hero_2_attacked:
            hero_2_attack_time_axis += hero_2.status["Attack Interval"]
            hero_2_attacked = False

    return hero_1, hero_2
