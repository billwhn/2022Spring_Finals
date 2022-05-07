from dataclasses import dataclass
import random


@dataclass
class Hero:
    """A super-class for heroes"""
    name: str  # the nickname for the hero

    base_attack_time: float  # affecting attack interval
    basic_attack_speed: int  # affecting attack interval
    basic_lowest_damage: int  # hero's attack damage has a range, the lowest number when hero is level 0
    basic_highest_damage: int  # hero's attack damage has a range, the highest number when hero is level 0
    basic_armor: float  # hero's armor at level 0, armor affects physical damage taken by the hero
    basic_hit_point: int  # hero's HP at level 0
    basic_regeneration: float  # hero's basic regeneration at level 0
    main_attribute: str  # hero's main attribute, Intelligence or Strength or Agility

    basic_strength: float  # hero's strength at level 0
    basic_agility: float  # hero's agility at level 0
    strength_level_growth: float  # the amount of strength the hero will get when grow one level
    agility_level_growth: float  # the amount of agility the hero will get when grow one level

    bonus_strength: int  # hero's bonus strength comes from items and skills
    bonus_agility: int  # hero's bonus agility comes from items and skills
    bonus_damage_without_main_attribute: int  # hero's bonus damage comes from items and skills

    # there are more than 1 skill can grant evasion ability
    evasion_list: dict  # key: skill name, value: int, evasion possibility

    bonus_attack_speed_without_agility: int  # hero's bonus attack speed comes from items and skills
    bonus_armor_without_agility: int  # hero's bonus armor comes from items and skills
    bonus_regeneration_without_strength: int  # hero's bonus regeneration comes from items and skills
    bonus_hit_point_without_strength: int  # hero's bonus HP comes from items and skills

    skill_list: dict  # the sub skills that the hero has learned
    attack_attachment: dict  # the attachment effects of the hero's normal attack may have
    other_positive_effect: dict  # the positive buff that the hero has
    other_negative_effect: dict  # the de-buff that the hero is taking
    # there are more than 1 skill can grant critical attack ability
    critical_list: dict  # key: skill name, value: list, [possibility, critical rate]
    main_skill_list: dict  # the main skills that the hero has learned

    hero_level: int  # hero's level, between 1 ~ 30
    life_steal_rate: int  # the life steal rate the hero has for each attack
    pierce: dict  # the possibility of ignoring evasion
    ultimate_skill: bool  # if the hero has learned ultimate skill or not

    status: dict  # records hero's various real-time attributes like current HP

    def __init__(self, hero_level=1):
        """
        Initiate function for all the heroes.
        """
        self.bonus_strength = 0
        self.bonus_agility = 0
        self.bonus_damage_without_main_attribute = 0
        self.evasion_list = {}

        self.bonus_attack_speed_without_agility = 0
        self.bonus_armor_without_agility = 0
        self.bonus_regeneration_without_strength = 0
        self.bonus_hit_point_without_strength = 0

        self.skill_list = {}
        self.attack_attachment = {}
        self.other_positive_effect = {}
        self.other_negative_effect = {}
        self.critical_list = {}
        self.status = {}
        self.main_skill_list = {}
        self.hero_level = hero_level
        self.life_steal_rate = 0
        self.pierce = {}
        self.ultimate_skill = False

    def set_name(self, name: str) -> None:
        """
        Setting Hero Object's nickname.

        :param name: hero's nickname
        :return: None
        """
        self.name = name

    def set_hero_level(self, hero_level: int) -> None:
        """
        Setting the level of the Hero object.

        :param hero_level: hero's level
        :return: None
        """
        self.hero_level = hero_level

    def learn_skill_book(self, skill_name: str, qty_of_books: int) -> [int, int]:
        """
        This function is a common function when a skill book is consumed.
        This function determines how many levels the skill will improve.

        :param skill_name: the skill that this Skill Book is bounded to.
        :param qty_of_books: how many skill books -Attribute Bonus- are consumed
        :return: [original_level, new_level]
                 original_level: the level of this skill before consuming the skill book(s);
                 new_level: the level of this skill after consuming the skill book(s)
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

    def check_able_to_learn_skill_book(self, skill_name: str) -> bool:
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

    def learn_skill_attribute_bonus(self, qty_of_books: int) -> None:
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

    def learn_skill_evasion(self, qty_of_books: int) -> None:
        """
        When a hero consumes Skill Book -Evasion-.

        :param qty_of_books: how many skill books -Evasion- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Evasion"):
            return None
        _, new_level = self.learn_skill_book("Evasion", qty_of_books)
        self.evasion_list["Evasion"] = 30 + 5 * new_level

    def learn_skill_corruption(self, qty_of_books: int) -> None:
        """
        When a hero consumes Skill Book -Corruption-.

        :param qty_of_books: how many skill books -Corruption- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Corruption"):
            return None
        _, new_level = self.learn_skill_book("Corruption", qty_of_books)
        self.other_positive_effect["Reduce Enemy Armor"] = 2 * new_level

    def learn_skill_armor_bonus(self, qty_of_books: int) -> None:
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

    def learn_skill_thorn_armor(self, qty_of_books: int) -> None:
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

    def learn_skill_curse_of_death(self, qty_of_books: int) -> None:
        """
        When a hero consumes Skill Book -Curse of Death-.
        If consumed successfully, the skill will be recorded in Hero's attribute other_positive_effect

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

    def learn_skill_fire(self, qty_of_books: int) -> None:
        """
        When a hero consumes Skill Book -Fire!-.

        :param qty_of_books: how many skill books -Fire!- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Fire!"):
            return None
        _, new_level = self.learn_skill_book("Fire!", qty_of_books)
        self.other_positive_effect["Ignore Armor"] = 10 + 5 * new_level

    def learn_skill_crushing(self, qty_of_books: int) -> None:
        """
        When a hero consumes Skill Book -Crushing-.

        :param qty_of_books: how many skill books -Crushing- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Crushing"):
            return None
        _, new_level = self.learn_skill_book("Crushing", qty_of_books)
        self.attack_attachment["Crushing"] = new_level

    def learn_skill_damage_bonus(self, qty_of_books: int) -> None:
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

    def learn_skill_life_steal(self, qty_of_books: int) -> None:
        """
        When a hero consumes Skill Book -Life Steal-.

        :param qty_of_books: how many skill books -Life Steal- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Life Steal"):
            return None
        _, new_level = self.learn_skill_book("Life Steal", qty_of_books)
        self.attack_attachment["Life Steal"] = new_level

    def learn_skill_smash(self, qty_of_books: int) -> None:
        """
        When a hero consumes Skill Book -Smash-.

        :param qty_of_books: how many skill books -Smash- are consumed
        :return: None
        """
        if not self.check_able_to_learn_skill_book("Smash"):
            return None
        _, new_level = self.learn_skill_book("Smash", qty_of_books)
        self.attack_attachment["Smash"] = new_level

    def get_random_skill_book(self, amount_of_skill_book: int) -> None:
        """
        Roll random amount of skill books. The hero will learn the 4 skills with the highest amount of skill book.
        E.g., rolled 20 skill books for [2, 5, 2, 3, 0 ,1, 2, 2, 2, 1, 2]
        The hero will learn level 5 skill, level 3 skill and randomly pick two level 2 skills.

        :param amount_of_skill_book: how many skill books the hero will get
        :return: None
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

    def calculate_status(self) -> None:
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

        if "MKB" in self.attack_attachment.keys():
            self.pierce["MKB"] = pierce_possibility_mkb(self.attack_attachment["MKB"]) * 100

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
        """
        When the hero gets some life steals, this will heal same amount HP for the hero.

        :param life_steal_amount: life steal amount
        :return: Actual damage caused
        """
        self.status["Current HP"] += life_steal_amount
        actual_amount = round(life_steal_amount)
        return actual_amount

    def regenerate_and_curse(self, time_second: float, show_all_the_details=False) -> int:
        """
        Calculate hit point regenerate during time period.
        This function also consider damages the hero taken by second.
        E.g., Damage comes from Curse of Death

        :param time_second: how mang seconds have passed
        :param show_all_the_details: show details of regenerate and damage or not
        :return: how many hit points the hero regenerated or lost
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

    def learn_main_skill_feast(self) -> None:
        """
        When hero learns main skill -Feast-.

        :return: None
        """
        self.main_skill_list["Feast"] = min(4, (self.hero_level + 1) // 2)

    def learn_main_skill_blade_dance(self) -> None:
        """
        When hero learns main skill -Blade Dance-.

        :return: None
        """
        skill_level = min(4, (self.hero_level + 1) // 2)
        self.main_skill_list["Blade Dance"] = skill_level
        # critical_list: dict  # key: skill name, value: list, [possibility, critical rate]
        self.critical_list["Blade Dance"] = [15 + 5 * skill_level, 180]

    def learn_main_skill_jingu_mastery(self) -> None:
        """
        When hero learns main skill -Jingu Mastery-.

        :return: None
        """
        skill_level = min(4, (self.hero_level + 1) // 2)
        self.main_skill_list["JinGu Mastery"] = skill_level
        self.other_positive_effect["JinGu Mastery Attack Times"] = -5

    def learn_main_skill_moment_of_courage(self):
        """
        When hero learns main skill -Moment of Courage-.

        :return: None
        """
        skill_level = min(4, (self.hero_level + 1) // 2)
        self.main_skill_list["Moment of Courage"] = skill_level

    def learn_main_skill_coup_de_grace(self) -> None:
        """
        When hero learns main skill -Cope De Grace-.
        This is an ultimate skill, only can be learned at level 6 and only one ultimate skill is allowed.

        :return: None
        """
        if self.hero_level < 6:
            return None
        if self.ultimate_skill:
            return None
        skill_level = min(3, self.hero_level // 6)
        self.main_skill_list["Coup de Grace"] = skill_level
        # critical_list: dict  # key: skill name, value: list, [possibility, critical rate]
        self.critical_list["Coup de Grace"] = [15, 75 + 125 * skill_level]
        self.ultimate_skill = True

    def learn_main_skill_grow(self):
        """
        When hero learns main skill -Grow-.
        This is an ultimate skill, only can be learned at level 6 and only one ultimate skill is allowed.

        :return: None
        """
        if self.hero_level < 6:
            return None
        if self.ultimate_skill:
            return None
        skill_level = min(3, self.hero_level // 6)
        self.main_skill_list["Grow"] = skill_level
        self.bonus_armor_without_agility += 6 + 6 * skill_level
        self.bonus_damage_without_main_attribute += 40 * skill_level - 10
        self.bonus_attack_speed_without_agility -= 10 + 10 * skill_level
        self.ultimate_skill = True

    def roll_main_skill(self, amount_of_main_skill: int, learn_ultimate_or_not=False) -> None:
        """
        The hero will randomly learn certain amount of main skills.

        :param amount_of_main_skill: how many main skills the hero will get
        :param learn_ultimate_or_not: whether learn an ultimate skill or not (do not count in as amount_of_main_skill)
        :return: None
        """
        count = 0
        while True:
            if count == amount_of_main_skill:
                break
            randon_int = random.randint(1, 4)
            if randon_int == 1:
                if "JinGu Mastery" not in self.main_skill_list.keys():
                    self.learn_main_skill_jingu_mastery()
                    count += 1
            elif randon_int == 2:
                if "Feast" not in self.main_skill_list.keys():
                    self.learn_main_skill_feast()
                    count += 1
            elif randon_int == 3:
                if "Blade Dance" not in self.main_skill_list.keys():
                    self.learn_main_skill_blade_dance()
                    count += 1
            elif randon_int == 4:
                if "Moment of Courage" not in self.main_skill_list.keys():
                    self.learn_main_skill_moment_of_courage()
                    count += 1
        if learn_ultimate_or_not:
            randon_int = randon_int(1, 2)
            if randon_int == 1:
                if "Coup de Grace" not in self.main_skill_list.keys():
                    self.learn_main_skill_coup_de_grace()
            elif randon_int == 2:
                if "Grow" not in self.main_skill_list.keys():
                    self.learn_main_skill_grow()


def attack(attack_hero: Hero, defend_hero: Hero, show_log_or_not=False, show_all_the_details=False) -> list:
    """
    One hero attacks another hero once.

    :param show_log_or_not: whether show the details of attack result in log or not
    :param show_all_the_details: whether show the details of attack damage composition in log or not
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
    for key in attack_hero.pierce.keys():
        if random.randint(1, 100) <= attack_hero.pierce[key]:
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
    :param damage_list: the damage caused by an attack action, before calculate physical and magic resistance
                    [ evadable physical damage, evadable magic damage, evadable true damage,
                      un-evadable physical damage, un-evadable magic damage, un-evadable true damage,
                      reflected physical damage, reflected magic damage, reflected true damage,
                      life steal amount, normal attack damage
                    ]
    :param life_steal_rate: this attack's attached life steal rate
    :param show_log_or_not: whether show the details of attack result in log or not
    :param show_all_the_details: whether show the details of attack damage composition in log or not
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


def show_attack_log(attack_hero: Hero, defend_hero: Hero, damage_list: list):
    """
    Function used to show the damage result of an attack action.

    :param attack_hero: the attacker hero
    :param defend_hero: the defender hero
    :param damage_list: the result of this attack [ Damage reflected to the attacker hero,
                                                    Damage caused to the defender hero,
                                                    Life Steal amount of the attacker hero]
    :return: a list of total damage taken by attack_hero and defend_hero
    """
    print("{} attacks {}, caused {} damage, get {} counter damage, regenerates {} by life steal."
          .format(attack_hero.name, defend_hero.name,
                  round(damage_list[1]), round(damage_list[0]), round(damage_list[2])))
    print("{} HP left: {}\t\t\t{} HP left {}\n".format(attack_hero.name, round(attack_hero.status["Current HP"]),
                                                       defend_hero.name, round(defend_hero.status["Current HP"])))


def calculate_physical_damage_under_skill_fire(attack_hero: Hero, defend_hero: Hero,
                                               physical_damage_amount: float) -> tuple(int, float):
    """
    This function calculates actual physical damage when affected by skill -Fire!- (Ignore armor).
    -Fire!- only affects normal attack damage.

    :param attack_hero: the attacker hero
    :param defend_hero: the defender hero
    :param physical_damage_amount: the amount of physical damage before calculating armor
    :return: (actual physical amount, actual physical resistance regarding normal attack)
    """
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


def trigger_moment_of_courage(attack_hero: Hero, defend_hero: Hero,
                              show_log_or_not=False, show_all_the_details=False) -> None:
    """
    To judge if main skill -Monment of Courage- is triggered.

    :param attack_hero: the attacker hero
    :param defend_hero: the defender hero
    :param show_log_or_not: whether show the details of attack result in log or not
    :param show_all_the_details: whether show the details of attack damage composition in log or not
    :return: None
    """
    if "Moment of Courage" in defend_hero.main_skill_list.keys():
        if random.randint(1, 100) <= 25:
            if show_all_the_details:
                print("{} Triggerd Moment of Courage ".format(defend_hero.name))
            life_steal_rate = 10 * defend_hero.main_skill_list["Moment of Courage"] + 45
            defend_hero.life_steal_rate += life_steal_rate
            attack(defend_hero, attack_hero, show_log_or_not, show_all_the_details)
            defend_hero.life_steal_rate -= life_steal_rate


def duel(hero_1: Hero, hero_2: Hero,
         show_log_or_not=False, show_all_the_details=False, show_regenerate_rs=False) -> tuple(Hero, Hero):
    """
    Let two heroes have a duel

    :param hero_1: the first hero
    :param hero_2: the second hero
    :param show_log_or_not: whether show the details of attack result in log or not
    :param show_all_the_details: whether show the details of attack damage composition in log or not
    :param show_regenerate_rs: whether show the details of regeneration in log or not
    :return: the two hero's status after the duel is over
    """
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

        if last_hit_time_axis >= 500:
            break

        if hero_1_attacked:
            hero_1_attack_time_axis += hero_1.status["Attack Interval"]
            hero_1_attacked = False
        if hero_2_attacked:
            hero_2_attack_time_axis += hero_2.status["Attack Interval"]
            hero_2_attacked = False

    return hero_1, hero_2


def corruption_status(owner_hero: Hero, affected_hero: Hero, show_all_the_details=False) -> None:
    """
    Update the status if a hero is being affect by skill -Corruption-.

    :param owner_hero: the hero who learned skill -Corruption- (Reduce nearby enemy's armor)
    :param affected_hero: the hero who is affected by the skill
    :param show_all_the_details: whether show the details of being affected in log or not
    :return: None
    """
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
    """
    Update the status if a hero is being affect by skill -Curse of Death-.

    :param owner_hero: the hero who learned skill -Curse of Death- (Reduce nearby enemy's armor)
    :param affected_hero: the hero who is affected by the skill
    :param show_all_the_details: whether show the details of being affected in log or not
    :return: None
    """
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
    """
    The hero model for Hero Monkey King
    """
    def __init__(self, hero_level=1, name="Monkey King"):
        Hero.__init__(self, hero_level)
        self.name = name
        self.base_attack_time = 1.7
        self.basic_attack_speed = 100
        self.basic_lowest_damage = 29
        self.basic_highest_damage = 33
        self.basic_armor = 2
        self.basic_hit_point = 164
        self.basic_regeneration = 1
        self.main_attribute = "Agility"
        self.basic_strength = 15.2
        self.basic_agility = 18.3
        self.strength_level_growth = 2.8
        self.agility_level_growth = 3.7

        self.learn_main_skill_jingu_mastery()


@dataclass
class HeroLifeStealer(Hero):
    """
    The hero model for Hero LifeStealer
    """
    def __init__(self, hero_level=1, name="LifeStealer"):
        Hero.__init__(self, hero_level)
        self.name = name
        self.base_attack_time = 1.7
        self.basic_attack_speed = 120
        self.basic_lowest_damage = 22
        self.basic_highest_damage = 28
        self.basic_armor = 1
        self.basic_hit_point = 262
        self.basic_regeneration = 0.25
        self.main_attribute = "Strength"
        self.basic_strength = 22.6
        self.basic_agility = 16.4
        self.strength_level_growth = 2.4
        self.agility_level_growth = 2.6

        self.learn_main_skill_feast()


@dataclass
class HeroTreantProtector(Hero):
    """
    The hero model for Hero Treant Protector
    """
    def __init__(self, hero_level=1, name="Treant Protector"):
        Hero.__init__(self, hero_level)
        self.name = name
        self.base_attack_time = 1.9
        self.basic_attack_speed = 100
        self.basic_lowest_damage = 62
        self.basic_highest_damage = 70
        self.basic_armor = -1
        self.basic_hit_point = 262
        self.basic_regeneration = 0.25
        self.main_attribute = "Strength"
        self.basic_strength = 21.6
        self.basic_agility = 13
        self.strength_level_growth = 3.4
        self.agility_level_growth = 2


@dataclass
class HeroBountyHunter(Hero):
    """
    The hero model for Hero Bounty Hunter
    """
    def __init__(self, hero_level=1, name="Bounty Hunter"):
        Hero.__init__(self, hero_level)
        self.name = name
        self.base_attack_time = 1.7
        self.basic_attack_speed = 100
        self.basic_lowest_damage = 30
        self.basic_highest_damage = 38
        self.basic_armor = 4
        self.basic_hit_point = 160
        self.basic_regeneration = 1.25
        self.main_attribute = "Agility"
        self.basic_strength = 17.5
        self.basic_agility = 18.4
        self.strength_level_growth = 2.5
        self.agility_level_growth = 2.6


def hero_initialize(hero_model: str, hero_level=1, hero_name=''):
    """
    Creating a hero object according to the parameters.

    :param hero_model: the name of the hero model
    :param hero_level: the hero level, from 1 to 30
    :param hero_name: the nickname for the hero object
    :return: the hero model object
    """
    if hero_model == 'MonkeyKing':
        if hero_name == '':
            return HeroMonkeyKing(hero_level=hero_level)
        else:
            return HeroMonkeyKing(hero_level=hero_level, name=hero_name)
    elif hero_model == 'LifeStealer':
        if hero_name == '':
            return HeroLifeStealer(hero_level=hero_level)
        else:
            return HeroLifeStealer(hero_level=hero_level, name=hero_name)
    elif hero_model == 'TreantProtector':
        if hero_name == '':
            return HeroTreantProtector(hero_level=hero_level)
        else:
            return HeroTreantProtector(hero_level=hero_level, name=hero_name)
    elif hero_model == 'BountyHunter':
        if hero_name == '':
            return HeroBountyHunter(hero_level=hero_level)
        else:
            return HeroBountyHunter(hero_level=hero_level, name=hero_name)
    else:
        raise ValueError('No such Hero {} in our Model!'.format(hero_model))


def aggregate_analyze(loop_times: int, hero_level: int,
                      hero_1_model: str, hero_2_model: str, hero_1_name: str, hero_2_name: str,
                      number_of_skill_books: int, number_of_main_skills: int, items_dict: dict,
                      show_loop_aggregate_result=True, show_skill_list_each_time=False, show_log_or_not=False,
                      show_all_the_details=False, show_regenerate_rs=False):
    winning_count = {}
    winning_count_main_skill = {}
    winning_count_only = {}
    winning_count_main_skill_only = {}
    total_occurance = {}
    total_occurance_main_skill = {}
    total_occurance_only = {}
    total_occurance_main_skill_only = {}

    for i in range(0, loop_times):
        hero_1 = hero_initialize(hero_1_model, hero_level, hero_1_name)
        hero_2 = hero_initialize(hero_2_model, hero_level, hero_2_name)

        for item in items_dict.keys():
            if item == "MKB":
                hero_1.equip_monkey_king_bar(items_dict[item])
                hero_2.equip_monkey_king_bar(items_dict[item])
            elif item == "Satanic":
                hero_1.equip_satanic(items_dict[item])
                hero_2.equip_satanic(items_dict[item])
            elif item == "Heart":
                hero_1.equip_heart_of_tarrasque(items_dict[item])
                hero_2.equip_heart_of_tarrasque(items_dict[item])

        hero_1.get_random_skill_book(number_of_skill_books)
        hero_2.get_random_skill_book(number_of_skill_books)

        if number_of_main_skills != 0:
            hero_1.roll_main_skill(number_of_main_skills)
            hero_2.roll_main_skill(number_of_main_skills)

        duel(hero_1, hero_2, show_log_or_not, show_all_the_details, show_regenerate_rs)

        if show_skill_list_each_time:
            print("\nSkill List:")
            print(
                "{}: {}, main skills: {}".format(hero_1.name, hero_1.skill_list.keys(), hero_1.main_skill_list.keys()))
            print(
                "{}: {}, main skills: {}".format(hero_2.name, hero_2.skill_list.keys(), hero_2.main_skill_list.keys()))

        if hero_2.status["Current HP"] <= 0:
            skill_list = hero_1.skill_list.keys()
            main_skill_list = hero_1.main_skill_list.keys()
            skill_list2 = hero_2.skill_list.keys()
            main_skill_list2 = hero_2.main_skill_list.keys()
        else:
            skill_list = hero_2.skill_list.keys()
            main_skill_list = hero_2.main_skill_list.keys()
            skill_list2 = hero_1.skill_list.keys()
            main_skill_list2 = hero_1.main_skill_list.keys()

        def update_dict(dict_to_update, source_dict):
            for skill_name in source_dict.keys():
                if skill_name in dict_to_update.keys():
                    dict_to_update[skill_name] += 1
                else:
                    dict_to_update[skill_name] = 1
            return dict_to_update

        total_occurance = update_dict(total_occurance, hero_1.skill_list)

        total_occurance = update_dict(total_occurance, hero_2.skill_list)

        def update_only_dict(dict_to_update, source_dict, rival_dict):
            for skill_name in source_dict.keys():
                if skill_name not in rival_dict.keys():
                    if skill_name in dict_to_update.keys():
                        total_occurance_only[skill_name] += 1
                    else:
                        total_occurance_only[skill_name] = 1
            return dict_to_update

        total_occurance_only = update_only_dict(total_occurance_only, hero_1.skill_list, hero_2.skill_list)

        total_occurance_only = update_only_dict(total_occurance_only, hero_2.skill_list, hero_1.skill_list)

        total_occurance_main_skill = update_dict(total_occurance_main_skill, hero_1.main_skill_list)

        total_occurance_main_skill = update_dict(total_occurance_main_skill, hero_2.main_skill_list)

        total_occurance_main_skill_only = update_only_dict(total_occurance_main_skill_only,
                                                           hero_1.main_skill_list, hero_2.main_skill_list)

        total_occurance_main_skill_only = update_only_dict(total_occurance_main_skill_only,
                                                           hero_2.main_skill_list, hero_1.main_skill_list)

        def update_dict_by_list(dict_to_update, source_list):
            for skill_name in source_list:
                if skill_name in dict_to_update.keys():
                    dict_to_update[skill_name] += 1
                else:
                    dict_to_update[skill_name] = 1
            return dict_to_update

        winning_count = update_dict_by_list(winning_count, skill_list)

        def update_dict_by_list_only(dict_to_update, source_list, rival_list):
            for skill_name in source_list:
                if skill_name not in rival_list:
                    if skill_name in dict_to_update.keys():
                        dict_to_update[skill_name] += 1
                    else:
                        dict_to_update[skill_name] = 1
            return dict_to_update

        winning_count_only = update_dict_by_list_only(winning_count_only, skill_list, skill_list2)

        winning_count_main_skill = update_dict_by_list(winning_count_main_skill, main_skill_list)

        winning_count_main_skill_only = update_dict_by_list_only(winning_count_main_skill_only,
                                                                 main_skill_list, main_skill_list2)

    if show_loop_aggregate_result:
        winning_count = dict(sorted(winning_count.items(), key=lambda w: (w[1], w[0])))
        winning_count_only = dict(sorted(winning_count_only.items(), key=lambda w: (w[1], w[0])))
        winning_count_main_skill = dict(sorted(winning_count_main_skill.items(), key=lambda w: (w[1], w[0])))
        winning_count_main_skill_only = dict(sorted(winning_count_main_skill_only.items(), key=lambda w: (w[1], w[0])))

        attention_str = "{} Summary {}\n".format('#' * 60, '#' * 60)
        print("\n{}".format(attention_str * 3))

        print("Loop Times {}, Hero Level {}, Amount of Skill Books {}"
              .format(loop_times, hero_level, number_of_skill_books))

        show_dict_report("Sub Skills", winning_count, total_occurance, loop_times)

        show_dict_report("Sub Skills Rid of Cases Both Sides Learned One Skill", winning_count_only,
                         total_occurance_only, loop_times)

        show_dict_report("Main Skills", winning_count_main_skill, total_occurance_main_skill, loop_times)

        show_dict_report("Main Skills Rid of Cases Both Sides Learned One Skill", winning_count_main_skill_only,
                         total_occurance_main_skill_only, loop_times)


def show_dict_report(report_name: str, winner_dict: dict, total_count_dict: dict, loop_times: int) -> None:
    """
    This function is used to print the result of the monte carlo simulation.
    """
    print('\n{}{}{}'.format(' ' * ((90 - len(report_name)) // 2), report_name, ' ' * ((90 - len(report_name)) // 2)))
    print("Skill Name{}Win Fights{}Occurrence(winner-side){}Total Occurance{}Winner-Side/Total"
          .format(' ' * (25 - len('Skill Name')), ' ' * (15 - len('Win Fights')),
                  ' ' * (27 - len('Occurrence(winner-side)')), ' ' * (20 - len('Total Occurance'))))
    for skill in winner_dict.keys():
        rate_winner_side = round(int(winner_dict[skill]) / loop_times * 100, 2)
        rate_occ_total = round(int(winner_dict[skill]) / total_count_dict[skill] * 100, 2)
        print("{}{}{}{}{}%{}{}{}{}%"
              .format(skill, ' ' * (25 - len(skill)),
                      winner_dict[skill], ' ' * (15 - len(str(winner_dict[skill]))),
                      rate_winner_side, ' ' * (26 - len(str(rate_winner_side))),
                      total_count_dict[skill], ' ' * (20 - len(str(total_count_dict[skill]))),
                      rate_occ_total
                      ))


if __name__ == "__main__":
    item_dict = {}

    aggregate_analyze(1000, 6, "MonkeyKing", "MonkeyKing", "Monkey King 1st", "King Monkey 2nd", 20, 0, item_dict,
                      True, False, False, False, False)

    aggregate_analyze(1000, 15, "MonkeyKing", "MonkeyKing", "Monkey King 1st", "King Monkey 2nd", 60, 0, item_dict,
                      True, False, False, False, False)

    item_dict["MKB"] = 1
    aggregate_analyze(1000, 15, "MonkeyKing", "MonkeyKing", "Monkey King 1st", "King Monkey 2nd", 60, 0, item_dict,
                      True, False, False, False, False)

    item_dict["Heart"] = 1
    aggregate_analyze(1000, 15, "MonkeyKing", "MonkeyKing", "Monkey King 1st", "King Monkey 2nd", 60, 0, item_dict,
                      True, False, False, False, False)

    item_dict["Heart"] = 3
    aggregate_analyze(1000, 25, "MonkeyKing", "MonkeyKing", "Monkey King 1st", "King Monkey 2nd", 120, 0, item_dict,
                      True, False, False, False, False)
