# Monte Carlo Simulation of a Duel in Game Background
#### Game: Battle or Mirkwood (Based on Dota2 Engine)
![read_me_pics/dota2.png](read_me_pics/dota2.png)
#### 2022 Spring Final Project
![read_me_pics/battle_of_mirkwood.png](read_me_pics/battle_of_mirkwood.png)

*Note: The data is up to 05/05/2022, some changes may occur since Dota2 is always updating.
## Team Members
![read_me_pics/group_members.png](read_me_pics/group_members.png)
## Game Introduction
This is a simulation of a duel in a game background.
Battle Of Mirkwood is a Role Play Game based on Dota2. Hundreds of neutral creatures wander throughout the whole map. The neutral creatures will grant hero Skill Books which can be consumed to learn a new skill or improve the skill level by one level for each Skill Book consumed.
Players will encounter each other; this is where the duel happens. The duel might happen throughout the game, and the player who achieves 80 Player Kills first wins the game.
## Basic Conceptions
### Heroes
Each hero has different attributes: Damage, Attack Speed, Hit Point (HP), Armor and so on. Details see Appendix. 
Since there are too many models in the game which will unnecessarily complicate the simulation, we will set the model to Monkey King.
### Skills
Since spells are too complicated to simulate, we only consider passive skills. Each hero can learn 2 main passive skills and 4 sub passive skills.
#### Main Skills
The max level for a main skill is 4, the skill level cannot exceed (1+hero’s level) / 2.
The level of main skills grow as the level of the hero grows.
In the simulation, it is totally randomly selected.
#### Sub Skills
The max level for a sub skill is 10, the skill level cannot exceed the hero’s level.
Killing the neutral creatures will grant hero Skill Books. Each Skill Book is bounded to a specific Sub Skill. Consuming a Skill Book can grant hero that Sub Skill. If the hero has already learned that Sub Skill, each Skill Book consumed will improve one skill level of that Sub Skill.
For example, if a hero consumed 7 Skill Book-Armor Improving, he will have a Level 7 Sub Skill Armor Improving.
### Items
There are various items in the game, which makes it impossible to simulate. Thus, we will simulate the duel only selected items, includes: Monkey King Bar, Heart of Tarrasque and so on.


## Basic Assumptions
![read_me_pics/assumptions.png](read_me_pics/assumptions.png)
![read_me_pics/game_phases.png](read_me_pics/game_phases.png)
## Variables
### Fixed Variables
Hero models & items ---
The attributes for each hero model and each item are set by Dota2.

Skill Effects ---
The effect of each skill is set according to the RPG game as shown on last slide.
### Controlled Variables
Items ---
The hero will equip what set of items.

Hero Model and Hero Level --- 
Which hero model the simulation will actually use and the hero level are manually set.

Amount of Skill Books ---
How many amount of skill books the Hero will get is manually set.
### Variables with Randomness
![read_me_pics/random_var.png](read_me_pics/random_var.png)
## Hypothesis
# Appendix
## Illustration for More Detailed Game Mechanism
### Armor
Reduce physical damage the hero takes.

![read_me_pics/physical_resis_formula.png](read_me_pics/physical_resis_formula.png)

(Source: https://liquipedia.net/dota2/Armor)
### Magic Resistance
Reduces Magical damage the hero takes.

All the heroes have a 25% basic Magic Resistance. Since the item system is limited, there is no way to improve magic resistance in this model.

(Source: https://liquipedia.net/dota2/Magic_Resistance)
### Strength & Agility
Strength increases maximum health and health regeneration while Agility increases armor and attack speed. If Strength or Agility is the main attribute (primary attribute), it will also increase damage.

![read_me_pics/strength_icon.png](read_me_pics/strength_icon.png)
Each Strength gives: +20 Health (Hit Points), +0.1 Health Regeneration

![read_me_pics/agility_icon.png](read_me_pics/agility_icon.png)
Each Agility gives: +0.16 Armor, +1 Attack Speed
### Attack Speed
Attack Interval = Base Attack Time ÷ (1 + (Increased Attack Speed ÷ 100))

(Source: https://liquipedia.net/dota2/Attack_Speed)
### Damage Type
Physical Damage: Will be compromised by Physical Resistance, related to Armor.

Magic Damage: WIll be compromised by Magic Resistance

True Damage: Will not be compromised by anything.
## Illustration for sub-Skills
Sub-skills are the skills gained by consuming Skill Books. These skills are defined by the RPG game, not Dota2 itself.

![read_me_pics/sub_skills.png](read_me_pics/sub_skills.png)

## Main SKills
Main Skills are set by Dota2. The main skills implemented includes:
### Jingu Mastery 
![read_me_pics/jingu_mastery.png](read_me_pics/jingu_mastery.png)This is a skill of Monkey King in Dota2 (https://liquipedia.net/dota2/Monkey_King).

- Upon the fourth hit on the same enemy hero, Monkey King earns four charged attacks that have bonus damage and life steal.
![read_me_pics/jingu_mastery_math.png](read_me_pics/jingu_mastery_math.png)
### Other Main Skills Implemented
Feast (Skill of Life Stealer in Dota2 https://liquipedia.net/dota2/Lifestealer)

Moment of Courage (Skill of Legion Commander in Dota2 https://liquipedia.net/dota2/Legion_Commander)

Coup De Grace (Skill of Phantom Assassin in Dota2 https://liquipedia.net/dota2/Phantom_Assassin)

Grow (Skill of Tiny in Dota2 https://liquipedia.net/dota2/Tiny)
## Hero Models
### Monkey King
![read_me_pics/monkey_king.png](read_me_pics/monkey_king.png)
![read_me_pics/monkey_king_attr.png](read_me_pics/monkey_king_attr.png)

(Source: https://liquipedia.net/dota2/Monkey_King)
### Other Hero Models Implemented
Life Stealer (https://liquipedia.net/dota2/Lifestealer)

Bounty Hunter (https://liquipedia.net/dota2/Bounty_Hunter)

Treant Protector (https://liquipedia.net/dota2/Treant_Protector)
## Items
### Monkey King Bar:
Damage + 40, Attack Speed + 45. Grants each attack an 80% chance to pierce through evasion and deal 70 bonus magical damage.

![read_me_pics/MKB.png](read_me_pics/MKB.png)

(Source: https://liquipedia.net/dota2/Monkey_King_Bar)
### Heart of Tarrasque:
Strength + 45, Health+ 250, Health Regen+ 1.6% Max Health Regen

![read_me_pics/heart.png](read_me_pics/heart.png)

(Source: https://liquipedia.net/dota2/Heart_of_Tarrasque)
### Satanic:
Strength + 25, Damage + 45, Life Steal + 25%

![read_me_pics/satanic.png](read_me_pics/satanic.png)

(Source: https://liquipedia.net/dota2/Satanic)