from dataclasses import dataclass
import random


@dataclass
class Hero:
    """A super-class for heroes"""
    name: str

    base_attack_time: float
    basic_attack_speed: int
    basic_lowest_damage: int
    basic_highest_damage: int
    basic_armor: float
    basic_hit_point: int
    basic_regeneration: float
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
    main_skill_list: dict

    hero_level: int
    life_steal_rate: int

    status: dict

    def __init__(self):
        self.bonus_strength = 0
        self.bonus_agility = 0
        self.bonus_damage_without_main_attribute = 0
        # there are more than 1 skill can grant evasion ability
        self.evasion_list = {}  # key: skill name, value: int, evasion possibility

        self.bonus_attack_speed_without_agility = 0
        self.bonus_armor_without_agility = 0
        self.bonus_regeneration_without_strength = 0
        self.bonus_hit_point_without_strength = 0

        self.skill_list = {}
        self.attack_attachment = {}
        self.other_positive_effect = {}
        self.other_negative_effect = {}
        # there are more than 1 skill can grant critical attack ability
        self.critical_list = {}  # key: skill name, value: list, [possibility, critical rate]
        self.status = {}
        self.main_skill_list = {}
        self.hero_level = 1
        self.life_steal_rate = 0

    def set_name(self, name):
        self.name = name

    def set_hero_level(self, hero_level: int) -> None:
        """
        Setting the level of the Hero object.

        :param hero_level: hero's level
        :return: None
        """
        self.hero_level = hero_level

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

    def learn_skill_curse_of_death(self, qty_of_books: int):
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

    def learn_skill_fire(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Fire!-.

        :param qty_of_books: how many skill books -Fire!- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Fire!"):
            return None
        _, new_level = self.learn_skill_book("Fire!", qty_of_books)
        self.other_positive_effect["Ignore Armor"] = 10 + 5 * new_level

    def learn_skill_crushing(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Crushing-.

        :param qty_of_books: how many skill books -Crushing- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Crushing"):
            return None
        _, new_level = self.learn_skill_book("Crushing", qty_of_books)
        self.attack_attachment["Crushing"] = new_level

    def learn_skill_damage_bonus(self, qty_of_books: int):
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

    def learn_skill_life_steal(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Life Steal-.

        :param qty_of_books: how many skill books -Life Steal- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Life Steal"):
            return None
        _, new_level = self.learn_skill_book("Life Steal", qty_of_books)
        self.attack_attachment["Life Steal"] = new_level

    def learn_skill_smash(self, qty_of_books: int):
        """
        When a hero consumes Skill Book -Smash-.

        :param qty_of_books: how many skill books -Smash- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Smash"):
            return None
        _, new_level = self.learn_skill_book("Smash", qty_of_books)
        self.attack_attachment["Smash"] = new_level

    def get_random_skill_book(self, amount_of_skill_book):
        """

        :param amount_of_skill_book:
        :return:
        """
        skill_book_list = [0] * 11
        for i in range(0, amount_of_skill_book):
            skill_book_list[random.randint(0, 10)] += 1

        list_max = [0] * 11
        count = 0
        last_count = 0
        dict_random = {}
        max_level = -1
        list_result = [0] * 11
        while True:
            if count >= 4:
                for i in range(0, 11):
                    if list_max[i] == max_level:
                        dict_random[i] = max_level
                    elif list_max[i] > max_level:
                        list_result[i] = list_max[i]
                for i in range(0, 4 - last_count):
                    k = random.choice(list(dict_random.keys()))
                    list_result[k] = max_level
                    dict_random.pop(k)

                break
            last_count = count
            max_level = max(skill_book_list)
            if max_level == 0:
                break

            for i in range(0, 11):
                if max_level == skill_book_list[i]:
                    list_max[i] = max_level
                    skill_book_list[i] = 0
                    count += 1

        if list_result[0] > 0:
            self.learn_skill_attribute_bonus(list_result[0])
        if list_result[1] > 0:
            self.learn_skill_corruption(list_result[1])
        if list_result[2] > 0:
            self.learn_skill_armor_bonus(list_result[2])
        if list_result[3] > 0:
            self.learn_skill_thorn_armor(list_result[3])
        if list_result[4] > 0:
            self.learn_skill_curse_of_death(list_result[4])
        if list_result[5] > 0:
            self.learn_skill_evasion(list_result[5])
        if list_result[6] > 0:
            self.learn_skill_fire(list_result[6])
        if list_result[7] > 0:
            self.learn_skill_smash(list_result[7])
        if list_result[8] > 0:
            self.learn_skill_damage_bonus(list_result[8])
        if list_result[9] > 0:
            self.learn_skill_life_steal(list_result[9])
        if list_result[10] > 0:
            self.learn_skill_crushing(list_result[10])

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

    def equip_satanic(self, equip_or_take_off: int) -> None:
        """
        When hero equips Satanic

        :param equip_or_take_off: 1 means equip Satanic, -1 means take off Satanic, could be 2 or more
        :return: None
        """
        self.bonus_strength += 25 * equip_or_take_off
        self.life_steal_rate += 25 * equip_or_take_off
        self.bonus_damage_without_main_attribute += 45 * equip_or_take_off

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
        self.status[
            'Lowest Damage'] = self.basic_lowest_damage + self.bonus_damage_without_main_attribute + damage_from_attribute
        self.status[
            'Highest Damage'] = self.basic_highest_damage + self.bonus_damage_without_main_attribute + damage_from_attribute
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
        The hero takes physical damage, need to consider effect of Armor.

        :param physical_damage_amount: Damage Amount before calculating Armor
        :return: Actual damage caused
        """
        actual_damage = physical_damage_amount * self.status["Physical Resistance"]
        self.status["Current HP"] -= actual_damage
        actual_damage = round(actual_damage)
        return actual_damage

    def taken_magical_damage(self, magical_damage_amount: float) -> int:
        """
        The hero takes magic damage, need to consider effect of Magic Resistance.

        :param magical_damage_amount: Damage Amount before calculating Armor
        :return: Actual damage caused
        """
        actual_damage = magical_damage_amount * (1 - self.status["Magic Resistance"])
        self.status["Current HP"] -= actual_damage
        actual_damage = round(actual_damage)
        return actual_damage

    def taken_true_damage(self, true_damage_amount: float) -> int:
        """
        The hero takes true damage, the damage will not be reduced or increased.

        :param true_damage_amount: Damage Amount
        :return: Actual damage caused
        """
        self.status["Current HP"] -= true_damage_amount
        actual_damage = round(true_damage_amount)
        return actual_damage

    def life_steal_regenerate(self, life_steal_amount: float) -> int:
        self.status["Current HP"] += life_steal_amount
        actual_amount = round(life_steal_amount)
        return actual_amount

    def regenerate_and_curse(self, time_second: float, show_all_the_details=False) -> int:
        """
        Calculate hit point regenerate during time period.

        :param time_second: how mang seconds have passed
        :param show_all_the_details: show details of regenerate and damage in detail or not
        :return: None
        """
        regenerate_hp = self.status["Regeneration"] * time_second
        if show_all_the_details:
            print("{} regenerates HP {}".format(self.name, regenerate_hp))

        if "Curse of Death" in self.other_negative_effect.keys():
            # other_negative_effect["Curse"] : level of curse
            # other_negative_effect["Curse Reg Reduction"] : how many percent regenerate reduced
            # other_negative_effect["Curse Damage"] : curse damage per second
            regenerate_hp = (100 - self.other_negative_effect["Curse Reg Reduction"]) / 100 * regenerate_hp
            curse_damage = self.other_negative_effect["Curse Damage"] * time_second
            if show_all_the_details:
                print("{} Affected by Curse of Death, actual regenerates HP {}, lose {} HP due to curse."
                      .format(self.name, regenerate_hp, curse_damage))
            regenerate_hp -= curse_damage

        self.status["Current HP"] = min(self.status["Max HP"], self.status["Current HP"] + regenerate_hp)
        regenerate_hp = round(regenerate_hp)
        return regenerate_hp

    def learn_main_skill_feast(self):
        self.main_skill_list["Feast"] = min(4, (self.hero_level + 1) // 2)

    def learn_main_skill_blade_dance(self):
        skill_level = min(4, (self.hero_level + 1) // 2)
        self.main_skill_list["Blade Dance"] = skill_level
        # critical_list: dict  # key: skill name, value: list, [possibility, critical rate]
        self.critical_list["Blade Dance"] = [15 + 5 * skill_level, 180]

    def learn_main_skill_jingu_mastery(self):
        skill_level = min(4, (self.hero_level + 1) // 2)
        self.main_skill_list["JinGu Mastery"] = skill_level
        self.other_positive_effect["JinGu Mastery Attack Times"] = -5

    # Coup de Grace
    def learn_main_skill_coup_de_grace(self):
        if self.hero_level < 6:
            return None
        skill_level = min(3, self.hero_level // 6)
        self.main_skill_list["Coup de Grace"] = skill_level
        # critical_list: dict  # key: skill name, value: list, [possibility, critical rate]
        self.critical_list["Coup de Grace"] = [15, 75 + 125 * skill_level]

    def learn_main_skill_grow(self):
        if self.hero_level < 6:
            return None
        skill_level = min(3, self.hero_level // 6)
        self.main_skill_list["Grow"] = skill_level
        self.bonus_armor_without_agility += 6 + 6 * skill_level
        self.bonus_damage_without_main_attribute += 40 * skill_level - 10
        self.bonus_attack_speed_without_agility -= 10 + 10 * skill_level

    def learn_main_skill_moment_of_courage(self):
        skill_level = min(4, (self.hero_level + 1) // 2)
        self.main_skill_list["Moment of Courage"] = skill_level


def attack(attack_hero: Hero, defend_hero: Hero, show_log_or_not=False, show_all_the_details=False) -> list:
    """
    One hero attacks another hero once.

    :param show_log_or_not: weather or not show the details of attack in log
    :param show_all_the_details: weather or not show the details of attack damage composition in log
    :param attack_hero: the hero who attacks
    :param defend_hero: the hero who defends the attack
    :return: damage_list: the list of the attack result
    """
    attack_damage = random.uniform(attack_hero.status['Lowest Damage'], attack_hero.status['Highest Damage'])
    # evadable physical damage, evadable magic damage, evadable true damage
    # un-evadable physical damage, un-evadable magic damage, un-evadable true damage
    # self-taken physical damage (comes from skills like Thorn Armor), self-taken magic damage
    # life-steal, attack_damage_without_attachments
    damage_list = [0] * 11

    life_steal_rate = attack_hero.life_steal_rate
    evaded = False
    pierce = False

    un_evadable_physical_damage = 0
    un_evadable_magic_damage = 0
    un_evadable_true_damage = 0
    evadable_physical_damage = 0
    evadable_magic_damage = 0
    evadable_true_damage = 0
    attacker_take_physical_damage = 0
    attacker_take_magic_damage = 0
    attacker_take_true_damage = 0
    normal_attack_damage = 0
    life_steal_amount = 0

    attack_result = [0, 0, 0]

    if attack_hero.status["Current HP"] <= 0 or defend_hero.status["Current HP"] <= 0:
        # one side has already been killed before attack
        # for example, die because of the damage from Curse of Death
        return attack_result

    # calculate un-evadable damage first
    # in our model, only Smash is un-evadable
    if 'Smash' in attack_hero.skill_list.keys():
        if random.randint(1, 100) <= 20:
            skill_level = attack_hero.skill_list['Smash']
            smash_damage = 80 + 20 * skill_level  # Basic damage
            smash_damage += 0.01 * skill_level * defend_hero.status["Max HP"]  # decided by enemy max HP
            un_evadable_physical_damage += smash_damage
            if show_all_the_details:
                print("{} triggered Smash, deal damage {}".format(attack_hero.name, smash_damage))

    # calculate if this attack is evaded
    for key in attack_hero.status["Pierce"].keys():
        if random.randint(1, 100) <= attack_hero.attack_attachment["Pierce"][key]:
            pierce = True
            if key == "MKB":
                # un-evadable magic damage from MKB
                if show_all_the_details:
                    print("{} triggered MKB, deal damage {}".format(attack_hero.name, 70))
                un_evadable_magic_damage += 70

    damage_list[3] = un_evadable_physical_damage
    damage_list[4] = un_evadable_magic_damage
    damage_list[5] = un_evadable_true_damage

    if not pierce:
        # MKB not triggered, can evade
        if len(defend_hero.evasion_list.keys()) != 0:
            for evasion_skill in defend_hero.evasion_list:
                evasion_possibility = defend_hero.evasion_list[evasion_skill]
                if random.randint(0, 100) < evasion_possibility:
                    # evade successfully
                    evaded = True
                    break
    if evaded:
        if show_log_or_not:
            print("{} evaded successfully.".format(defend_hero.name))
        attack_result = damage_calculation(attack_hero, defend_hero, damage_list, show_log_or_not, show_all_the_details)
        return attack_result

    highest_critical_rate = 100

    # attack might be critical
    # each critical is independent, the final damage only counts the highest critical rate
    if len(attack_hero.critical_list.keys()) != 0:
        for critical_skill in attack_hero.critical_list.keys():
            if random.randint(1, 100) <= attack_hero.critical_list[critical_skill][0]:
                highest_critical_rate = max(highest_critical_rate, attack_hero.critical_list[critical_skill][1])
    if show_all_the_details:
        if highest_critical_rate != 100:
            print("{} triggered critical, critical rate {}".format(attack_hero.name, highest_critical_rate))
    normal_attack_damage += highest_critical_rate / 100 * attack_damage
    evadable_physical_damage += normal_attack_damage

    if 'Crushing' in attack_hero.skill_list.keys():
        if random.randint(1, 100) <= 15:
            skill_level = attack_hero.skill_list['Crushing']
            crush_damage = 50 + 50 * skill_level  # Basic damage
            crush_damage += 0.5 * skill_level * attack_hero.status["Strength"]  # decided by enemy max HP
            evadable_true_damage += crush_damage
            if show_all_the_details:
                print("{} triggered Crushing, deal damage {}".format(attack_hero.name, crush_damage))

    if "Feast" in attack_hero.main_skill_list.keys():
        # Feast cause evadable physical damage
        feast_life_steal = (0.01 + 0.006 * attack_hero.main_skill_list["Feast"]) * defend_hero.status["Max HP"]
        feast_extra_damage = (0.004 + 0.002 * attack_hero.main_skill_list["Feast"]) * defend_hero.status["Max HP"]
        life_steal_amount += feast_life_steal
        if show_all_the_details:
            print("{} triggered Feast, deal damage {}, life steal amount {}."
                  .format(attack_hero.name, feast_extra_damage, feast_life_steal))
        evadable_physical_damage += feast_extra_damage

    if "Life Steal" in attack_hero.skill_list.keys():
        # Life Steal only consider actual damage from normal attack (affected by defend hero's physical resistance)
        if random.randint(1, 100) <= 30:
            life_steal_bonus = attack_hero.skill_list["Life Steal"] * 5 + 20
            life_steal_rate += life_steal_bonus
            if show_all_the_details:
                print("{} triggered Life Steal, life steal rate bonus {}%.".format(attack_hero.name, life_steal_bonus))

    damage_list[0] = evadable_physical_damage
    damage_list[1] = evadable_magic_damage
    damage_list[2] = evadable_true_damage

    damage_list[6] = attacker_take_physical_damage
    damage_list[7] = attacker_take_magic_damage
    damage_list[8] = attacker_take_true_damage

    damage_list[9] = life_steal_amount
    damage_list[10] = normal_attack_damage
    attack_result = damage_calculation(attack_hero, defend_hero, damage_list, life_steal_rate,
                                       show_log_or_not, show_all_the_details)

    if "JinGu Mastery" in attack_hero.main_skill_list.keys():
        attack_hero.other_positive_effect["JinGu Mastery Attack Times"] += 1
        if attack_hero.other_positive_effect["JinGu Mastery Attack Times"] == -1:
            attack_hero.other_positive_effect["JinGu Mastery Attack Times"] = 1
            bonus_jingu_damage = attack_hero.main_skill_list["JinGu Mastery"] * 30 + 10
            attack_hero.status['Lowest Damage'] += bonus_jingu_damage
            attack_hero.status['Highest Damage'] += bonus_jingu_damage
            bonus_jingu_life_steal = 15 * attack_hero.main_skill_list["JinGu Mastery"] + 10
            attack_hero.life_steal_rate += bonus_jingu_life_steal
            if show_all_the_details:
                print("{} triggered Jingu Mastery, damage bonus {}, life steal rate bonus {}%.\n"
                      .format(attack_hero.name, bonus_jingu_damage, bonus_jingu_life_steal))
        if attack_hero.other_positive_effect["JinGu Mastery Attack Times"] == 5:
            attack_hero.other_positive_effect["JinGu Mastery Attack Times"] = -5
            bonus_jingu_damage = attack_hero.main_skill_list["JinGu Mastery"] * 30 + 10
            attack_hero.status['Lowest Damage'] -= bonus_jingu_damage
            attack_hero.status['Highest Damage'] -= bonus_jingu_damage
            bonus_jingu_life_steal = 15 * attack_hero.main_skill_list["JinGu Mastery"] + 10
            attack_hero.life_steal_rate -= bonus_jingu_life_steal
            if show_all_the_details:
                print("{}'s Jingu Mastery ends, lose damage bonus {}, lose life steal rate bonus {}%.\n"
                      .format(attack_hero.name, bonus_jingu_damage, bonus_jingu_life_steal))

    return attack_result


def damage_calculation(attack_hero: Hero, defend_hero: Hero, damage_list,
                       life_steal_rate=0, show_log_or_not=False, show_all_the_details=False) -> list:
    """
    Calculate various damage caused by an attack action.

    :param attack_hero: the hero who attacks
    :param defend_hero: the hero who defends
    :param damage_list: the damage caused an attack action, before
        # evadable physical damage, evadable magic damage, evadable true damage
        # un-evadable physical damage, un-evadable magic damage, un-evadable true damage
        # self-taken physical damage (comes from skills like Thorn Armor), self-taken magic damage
    :param life_steal_rate: this attack's attached life steal rate
    :param show_log_or_not: whether show details of attack result in log
    :param show_all_the_details: whether show details of attack result in log
    :return: a list of total damage taken by attack_hero and defend_hero
    """
    attacker_taken_damage = 0
    defender_taken_damage = 0
    life_steal_amount = damage_list[9]
    if "Fire!" in attack_hero.skill_list.keys():
        damage_amount, normal_attack_resistance = calculate_physical_damage_under_skill_fire(attack_hero, defend_hero,
                                                                                             damage_list[10])
        defender_taken_damage += damage_amount
        if show_all_the_details:
            # normal_attack_damage_without_fire = defend_hero.taken_physical_damage(damage_list[10])
            print("{} triggered Fire!, ignore armor, normal attack damage {}.".format(attack_hero.name, damage_amount))
            # print("Without Fire!, the normal attack damage will be {}".format(normal_attack_damage_without_fire))
        defender_taken_damage += defend_hero.taken_physical_damage(damage_list[0] + damage_list[3] - damage_list[10])
    else:
        defender_taken_damage += defend_hero.taken_physical_damage(damage_list[0] + damage_list[3])
        normal_attack_resistance = defend_hero.status["Physical Resistance"]

    actual_normal_attack_damage = damage_list[10] * normal_attack_resistance
    life_steal_amount += actual_normal_attack_damage * life_steal_rate / 100
    if show_all_the_details and life_steal_amount != 0:
        print("{}'s total life steal: {}.".format(attack_hero.name, life_steal_amount))

    if "Thorn Armor" in defend_hero.skill_list.keys():
        damage_reflection = actual_normal_attack_damage * (
            defend_hero.other_positive_effect["Physical Damage Reflection"]) / 100
        damage_list[6] += damage_reflection
        if show_all_the_details:
            print("{} triggered Thorn Armor, reflected damage {}.".format(defend_hero.name, damage_reflection))

    # curse will reduce life steal amount
    if "Curse of Death" in defend_hero.skill_list.keys() and life_steal_amount != 0:
        life_steal_amount = life_steal_amount * (
                100 - defend_hero.other_positive_effect["Curse Reg Reduction"]) / 100
        if show_all_the_details:
            print("{} triggered Curse of Death, reducing actual enemy life steal to {}.".
                  format(defend_hero.name, life_steal_amount))

    defender_taken_damage += defend_hero.taken_magical_damage(damage_list[1] + damage_list[4])
    defender_taken_damage += defend_hero.taken_true_damage(damage_list[2] + damage_list[5])
    attacker_taken_damage += attack_hero.taken_physical_damage(damage_list[6])
    attacker_taken_damage += attack_hero.taken_magical_damage(damage_list[7])
    attacker_taken_damage += attack_hero.taken_true_damage(damage_list[8])
    attack_hero.life_steal_regenerate(life_steal_amount)

    attack_result = [attacker_taken_damage, defender_taken_damage, life_steal_amount]
    if show_log_or_not:
        show_attack_log(attack_hero, defend_hero, attack_result)
    return attack_result


def show_attack_log(attack_hero, defend_hero, damage_list: list):
    print("{} attacks {}, caused {} damage, get {} counter damage, regenerates {} by life steal."
          .format(attack_hero.name, defend_hero.name,
                  round(damage_list[1]), round(damage_list[0]), round(damage_list[2])))
    print("{} HP left: {}\t\t\t{} HP left {}\n".format(attack_hero.name, round(attack_hero.status["Current HP"]),
                                                       defend_hero.name, round(defend_hero.status["Current HP"])))


def calculate_physical_damage_under_skill_fire(attack_hero: Hero, defend_hero: Hero,
                                               physical_damage_amount: float) -> tuple:
    if defend_hero.status["Armor"] > 0:
        actual_armor = defend_hero.status["Armor"] * (100 - attack_hero.other_positive_effect["Ignore Armor"]) / 100
    else:
        actual_armor = defend_hero.status["Armor"]
    actual_physical_resistance = 1 - (0.052 * actual_armor) / (0.9 + 0.048 * abs(actual_armor))

    actual_damage = physical_damage_amount * actual_physical_resistance

    defend_hero.status["Current HP"] -= actual_damage
    actual_damage = round(actual_damage)

    return actual_damage, actual_physical_resistance


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


def trigger_moment_of_courage(attack_hero: Hero, defend_hero: Hero, show_log_or_not=False, show_all_the_details=False):
    if "Moment of Courage" in defend_hero.main_skill_list.keys():
        if random.randint(1, 100) <= 25:
            if show_all_the_details:
                print("{} Triggerd Moment of Courage ".format(defend_hero.name))
            life_steal_rate = 10 * defend_hero.main_skill_list["Moment of Courage"] + 45
            defend_hero.life_steal_rate += life_steal_rate
            attack(defend_hero, attack_hero, show_log_or_not, show_all_the_details)
            defend_hero.life_steal_rate -= life_steal_rate


def duel(hero_1: Hero, hero_2: Hero, show_log_or_not=False, show_all_the_details=False, show_regenerate_rs=False):
    # before duel start, calculate various long-lasting effects
    # for example, Corruption (reduce armor)

    hero_1.calculate_status()
    hero_2.calculate_status()

    corruption_status(hero_1, hero_2, show_all_the_details)
    corruption_status(hero_2, hero_1, show_all_the_details)
    curse_status(hero_1, hero_2, show_all_the_details)
    curse_status(hero_2, hero_1, show_all_the_details)

    hero_1_attack_time_axis = hero_1.status["Attack Interval"]
    hero_2_attack_time_axis = hero_2.status["Attack Interval"]
    last_hit_time_axis = 0
    hero_1_attacked = False
    hero_2_attacked = False

    while True:
        if hero_1_attack_time_axis < hero_2_attack_time_axis:
            # before attack, calculate regeneration and curse damage
            time = hero_1_attack_time_axis - last_hit_time_axis
            hero_1.regenerate_and_curse(time, show_regenerate_rs)
            hero_2.regenerate_and_curse(time, show_regenerate_rs)
            last_hit_time_axis = hero_1_attack_time_axis

            # attack
            attack(hero_1, hero_2, show_log_or_not, show_all_the_details)
            trigger_moment_of_courage(hero_1, hero_2, show_log_or_not, show_all_the_details)

            hero_1_attacked = True

        elif hero_1_attack_time_axis > hero_2_attack_time_axis:
            time = hero_2_attack_time_axis - last_hit_time_axis
            hero_1.regenerate_and_curse(time, show_regenerate_rs)
            hero_2.regenerate_and_curse(time, show_regenerate_rs)
            last_hit_time_axis = hero_2_attack_time_axis
            attack(hero_2, hero_1, show_log_or_not, show_all_the_details)
            trigger_moment_of_courage(hero_2, hero_1, show_log_or_not, show_all_the_details)
            hero_2_attacked = True
        else:
            # attack at same time, randomly decide sequence of attack
            time = hero_1_attack_time_axis - last_hit_time_axis
            hero_1.regenerate_and_curse(time, show_regenerate_rs)
            hero_2.regenerate_and_curse(time, show_regenerate_rs)
            last_hit_time_axis = hero_2_attack_time_axis
            if random.randint(0, 1) == 0:
                attack(hero_1, hero_2, show_log_or_not, show_all_the_details)
                trigger_moment_of_courage(hero_1, hero_2, show_log_or_not, show_all_the_details)
                hero_1_attacked = True
            else:
                attack(hero_2, hero_1, show_log_or_not, show_all_the_details)
                trigger_moment_of_courage(hero_2, hero_1, show_log_or_not, show_all_the_details)
                hero_2_attacked = True

        if hero_1.status["Current HP"] <= 0 or hero_2.status["Current HP"] <= 0:
            break

        if hero_1_attacked:
            hero_1_attack_time_axis += hero_1.status["Attack Interval"]
            hero_1_attacked = False
        if hero_2_attacked:
            hero_2_attack_time_axis += hero_2.status["Attack Interval"]
            hero_2_attacked = False

    return hero_1, hero_2


def corruption_status(owner_hero: Hero, affected_hero: Hero, show_all_the_details=False) -> None:
    # only one Corruption will take effect
    # affected by two enemy heroes both learned Corruption, only the highest level corruption takes effect
    if "Corruption" in owner_hero.skill_list.keys():
        if "Corruption" not in affected_hero.other_negative_effect.keys() \
                or affected_hero.other_negative_effect["Corruption"] < owner_hero.skill_list["Corruption"]:
            affected_hero.other_negative_effect["Corruption"] = owner_hero.skill_list["Corruption"]
            affected_hero.other_negative_effect["Reduced Armor"] = owner_hero.other_positive_effect[
                "Reduce Enemy Armor"]
            affected_hero.status["Armor"] -= affected_hero.other_negative_effect["Reduced Armor"]
            affected_hero.status["Physical Resistance"] = 1 - (0.052 * affected_hero.status["Armor"]) / (
                    0.9 + 0.048 * abs(affected_hero.status["Armor"]))
            if show_all_the_details:
                print("{} triggered Armor Corruption.\n".format(owner_hero.name))


def curse_status(owner_hero: Hero, affected_hero: Hero, show_all_the_details=False) -> None:
    # only one Curse of Death will take effect
    # affected by two enemy heroes both learned Curse of Death, only the highest level corruption takes effect
    if "Curse of Death" in owner_hero.skill_list.keys():
        if "Curse of Death" not in affected_hero.other_negative_effect.keys() \
                or affected_hero.other_negative_effect["Curse of Death"] < owner_hero.skill_list["Curse of Death"]:
            affected_hero.other_negative_effect["Curse of Death"] = owner_hero.skill_list["Curse of Death"]
            affected_hero.other_negative_effect["Curse Reg Reduction"] = owner_hero.other_positive_effect[
                "Curse Reg Reduction"]
            affected_hero.other_negative_effect["Curse Damage"] = owner_hero.other_positive_effect[
                "Curse Damage"]
            if show_all_the_details:
                print("{}'s Curse of Death begin to take effects.\n".format(owner_hero.name))


@dataclass
class HeroMonkeyKing(Hero):
    def __init__(self, hero_level=1, name="Monkey King"):
        Hero.__init__(self)
        self.name = name
        self.base_attack_time = 1.7
        self.basic_attack_speed = 100
        self.basic_lowest_damage = 29
        self.basic_highest_damage = 33
        self.basic_armor = 2
        self.basic_hit_point = 164
        self.basic_regeneration = 1
        self.main_attribute = "Agility"  # Intelligence or Strength or Agility
        self.basic_strength = 15.2
        self.basic_agility = 18.3
        self.strength_level_growth = 2.8
        self.agility_level_growth = 3.7
        self.hero_level = hero_level


@dataclass
class LifeStealer(Hero):
    def __init__(self, hero_level=1, name="LifeStealer"):
        Hero.__init__(self)
        self.name = name
        self.base_attack_time = 1.7
        self.basic_attack_speed = 120
        self.basic_lowest_damage = 22
        self.basic_highest_damage = 28
        self.basic_armor = 1
        self.basic_hit_point = 262
        self.basic_regeneration = 0.25
        self.main_attribute = "Strength"  # Intelligence or Strength or Agility
        self.basic_strength = 22.6
        self.basic_agility = 16.4
        self.strength_level_growth = 2.4
        self.agility_level_growth = 2.6
        self.hero_level = hero_level


@dataclass
class TreantProtector(Hero):
    def __init__(self, hero_level=1, name="Treant Protector"):
        Hero.__init__(self)
        self.name = name
        self.base_attack_time = 1.9
        self.basic_attack_speed = 100
        self.basic_lowest_damage = 62
        self.basic_highest_damage = 70
        self.basic_armor = -1
        self.basic_hit_point = 262
        self.basic_regeneration = 0.25
        self.main_attribute = "Strength"  # Intelligence or Strength or Agility
        self.basic_strength = 21.6
        self.basic_agility = 13
        self.strength_level_growth = 3.4
        self.agility_level_growth = 2
        self.hero_level = hero_level


@dataclass
class BountyHunter(Hero):
    def __init__(self, hero_level=1, name="Bounty Hunter"):
        Hero.__init__(self)
        self.name = name
        self.base_attack_time = 1.7
        self.basic_attack_speed = 100
        self.basic_lowest_damage = 30
        self.basic_highest_damage = 38
        self.basic_armor = 4
        self.basic_hit_point = 160
        self.basic_regeneration = 1.25
        self.main_attribute = "Agility"  # Intelligence or Strength or Agility
        self.basic_strength = 17.5
        self.basic_agility = 18.4
        self.strength_level_growth = 2.5
        self.agility_level_growth = 2.6
        self.hero_level = hero_level


if __name__ == "__main__":
    hero_1 = HeroMonkeyKing(hero_level=1)
    hero_2 = LifeStealer(hero_level=1)

    hero_1.get_random_skill_book(20)
    hero_2.get_random_skill_book(20)

    duel(hero_1, hero_2, True, True, False)

    print("Skill List:")
    print("{}: {}".format(hero_1.name, hero_1.skill_list.keys()))
    print("{}: {}".format(hero_2.name, hero_2.skill_list.keys()))
    print(len(hero_1.skill_list.keys()))
