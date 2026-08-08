#DnD_character.py

#NOTE STILL NEED TO IMPLEMENT NUMPY LIST: Maybe use an array to store the drinking history of a drunkard
#Or use it to store a list of three weapons or spells that battler can have on them

"""
# Author: Michael Bell
# Core Hierarchy File

This file contains the base class and derived class for the D&D characters.
The base class will have the data for each characters name, level, xp (experience points), hp (hit points), class, and race.

The different types of characters:
-- Drunkard: Tracks a character that loves alcohol and how many drinks they've had and their BAC (Blood Alcohol Content)
-- Avatar: Tracks roleplaying stats for a purely roleplaying character (alignment, relationship status, etc.)
-- Battler: Tracks a battle focused character (weapon, armor class, a spell)

There is detailed information about each class above their declaration
"""

from random import uniform, randint # both used in Drunkard(Character) class
from enum import Enum

XP_LEVEL_UP_THRESHOLD = 100

class DrunkardConstants:
    """Game balance constants for Drunkard class mechanics."""
    BAC_DANGER_THRESHOLD = 0.4
    ALCOHOL_POISONING_DEATH_CHANCE = 0.30  # 30% chance when BAC >= 0.4
    MIN_DRINK_BAC = 0.01
    MAX_DRINK_BAC = 0.07
    
    # Maps BAC range to drunk_fight success chance threshold (out of 10)
    DRUNK_FIGHT_CHANCES = {
        (0.0, 0.1): 2,        # 20% chance
        (0.1, 0.15): 3,       # 30% chance
        (0.15, 0.2): 4,       # 40% chance
        (0.2, 0.25): 5,       # 50% chance
        (0.25, 0.3): 6,       # 60% chance
        (0.3, 0.35): 7,       # 70% chance
        (0.35, 0.4): 8,       # 80% chance
        (0.4, float('inf')): 10,  # 100% chance
    }
    
    XP_FIGHT_GAIN_RANGE = (1, 50)
    XP_FIGHT_LOSS_RANGE = (1, 50)


class Character:
    """
    Base class representing a D&D character with core stats and leveling mechanics.
    
    All character types inherit from this class. Characters automatically level up
    when XP reaches 100 or more. Characters are compared by level first, then by
    XP as a tiebreaker for BST sorting.
    
    Attributes:
        _name (str): Character's name
        _level (int): Character's experience level (starts at 1)
        _hp (int): Hit points (health). Capped at 0 minimum.
        _xp (int): Experience points (0-99 per level, resets on level up)
        _character_class (str): Character class (e.g., "Warrior", "Mage")
        _race (str): Character race (e.g., "Human", "Elf")
    
    Example:
        >>> character = Character("Aragorn", 5, 50, 45, "Ranger", "Human")
        >>> character.set_hp(60)
        >>> character + 60  # Gains 60 XP, levels up
    """
    
    def __init__(
        self, 
        name: str, 
        level: int, 
        hp: int, 
        xp: int, 
        character_class: str, 
        race: str
    ) -> None:
        
        self._name = name
        self._level = level
        self._hp = hp
        self._xp = xp
        self._character_class = character_class
        self._race = race
        
    
     # Setter functions for each data member
    
    def set_name(self, name: str) -> None:
        if not name:
            raise ValueError("Character name cannot be empty")
        self._name = name
    
    def set_character_class(self, character_class: str) -> None:
        if not character_class:
            raise ValueError("Character class cannot be empty")
        self._character_class = character_class
    
    def set_race(self, race: str) -> None:
        if not race:
            raise ValueError("Character race cannot be empty")
        self._race = race
    
    def set_level(self, level: int) -> None:
        if level < 1:
            raise ValueError("Character level must be at least 1")
        self._level = level
    
    def set_hp(self, hp: int) -> None:
        self._hp = max(0, hp)


    def level_up(self) -> None:
        """Increase level if XP >= 100, then reset XP counter."""
        if self._xp >= XP_LEVEL_UP_THRESHOLD:
            self._level += 1
            self._xp -= XP_LEVEL_UP_THRESHOLD
            
            
    def compare_name(self, name: str):
        """Returns 0 if equal, -1 if less, 1 if greater (lexicographic)."""
        if self._name == name:          
            return 0                    
        elif self._name < name:
            return -1
        else:
            return 1
        
    def compare_data_name(self, data: "Character") -> int:
        """Returns 0 if equal, -1 if less, 1 if greater (lexicographic)."""
        if not isinstance(data, Character):
            raise TypeError(f"Expected Character, got {type(data).__name__}")
            
        if self._name == data._name:          
            return 0                    
        elif self._name < data._name:
            return -1
        else:
            return 1
                 
    
    def __add__(self, xp: int):
        """Gain XP and auto-level up if threshold reached. Returns new XP total."""
        self._xp += xp
        if self._xp >= XP_LEVEL_UP_THRESHOLD:
            self.level_up()
        return self._xp
    
    def __sub__(self, xp: int):
        """Lose XP (minimum 0). Does not cause level decrease. Returns new XP total."""
        self._xp = max(0, self._xp - xp)
        return self._xp
                  
            
    def __lt__(self, character):
        """Compare by level first, XP second (for BST sorting)."""
        if self._level != character._level:
            return self._level < character._level
        return self._xp < character._xp
    
    def __gt__(self, character):
        """Compare by level first, XP second (for BST sorting)."""
        if self._level != character._level:
            return self._level > character._level
        return self._xp > character._xp
    
    def __le__(self, character):
        return self < character or self == character
    
    def __ge__(self, character):
        return self > character or self == character
    
    def __eq__(self, character: "Character") -> bool:
        return self._level == character._level and self._xp == character._xp
    
    
    def __str__(self) -> str:
        return f"\nCharacter Type: Base character \nName: {self._name} \nRace: {self._race} \nClass: {self._character_class} \nHealth: {self._hp} \nLevel: {self._level} \nExperience: {self._xp}/100\n"
    
    
    

class Drunkard(Character):
    """
    A character archetype focused on alcohol and tavern brawling.
    
    Drunkards track Blood Alcohol Content (BAC) which affects their abilities.
    Higher BAC increases tavern brawl success chance but risks alcohol poisoning.
    At BAC >= 0.4, there's a 30% chance of death per drink consumed.
    
    Attributes:
        _bac (float): Blood Alcohol Content (0.0 to ~0.5+)
        _name, _level, _hp, _xp, _character_class, _race (inherited from Character)
    
    Example:
        >>> drunkard = Drunkard("Stumbles McGee", 3, 40, 25, "Bard", "Dwarf")
        >>> drunkard.drink(2)  # BAC increases by ~0.02-0.14
        >>> drunkard.drunk_fight()  # Higher BAC = better chance to win
        >>> drunkard.sleep()  # BAC resets to 0
    """
    def __init__(
        self, 
        name: str, 
        level: int, 
        hp: int, 
        xp: int, 
        character_class: str, 
        race: str
    ) -> None:
        super().__init__(name, level, hp, xp, character_class, race)
        self._bac = 0.0
    
    
    def drink(self, num_drinks: int) -> None:
        """Increase BAC by 0.01-0.07 per drink. Triggers alcohol poisoning check if BAC >= 0.4."""
        if self._hp > 0:
            for i in range(num_drinks):
                if self._bac >= DrunkardConstants.BAC_DANGER_THRESHOLD:
                    self.alcohol_poisoning()    
                    return
                self._bac += round(uniform(
                    DrunkardConstants.MIN_DRINK_BAC, 
                    DrunkardConstants.MAX_DRINK_BAC
                ), 2)
    
    def sleep(self) -> None:
        """Reset BAC to 0."""
        self._bac = 0
    
    def alcohol_poisoning(self) -> bool:
        """30% chance of death from alcohol poisoning. Returns True if character died."""
        roll = randint(1, 10)
        if roll <= 3:  # 30% chance
            self._hp = 0
            print("Your character died of alcohol poisoning! You'll need someone to revive you!\n")
            return True
        return False
        
        
    def drunk_fight(self) -> None:
        """Attempt to start a tavern brawl. Higher BAC = better success chance. Gain/lose 1-50 XP."""
        if self._hp <= 0:
            return
        
        chance = randint(1, 10)
        threshold = None
        
        # Find the BAC range and get success threshold
        for (low, high), thresh in DrunkardConstants.DRUNK_FIGHT_CHANCES.items():
            if low <= self._bac < high:
                threshold = thresh
                break
        
        if threshold is None:
            threshold = 10  # Fallback for edge cases
        
        if chance <= threshold:
            xp = randint(*DrunkardConstants.XP_FIGHT_GAIN_RANGE)
            self + xp  # Use parent's __add__ for XP gain
            print(f"You started a tavern brawl and gained {xp} xp!\n")
        else:
            xp = randint(*DrunkardConstants.XP_FIGHT_LOSS_RANGE)
            self - xp  # Use parent's __sub__ for XP loss
            print(f"You tried and failed to start a tavern brawl and lost {xp} xp!\n")
    
    
    def __str__(self) -> str:
        return f"\nCharacter Type: Drunkard \nName: {self._name} \nRace: {self._race} \nClass: {self._character_class} \nHealth: {self._hp} \nLevel: {self._level} \nExperience: {self._xp}/100\n"

    
    
class RelationshipStatus(Enum):
    """Relationship status values for Avatar characters."""
    SINGLE = 0
    DATING = 1
    MARRIED = 2
    
class Avatar(Character):
    """
    A purely roleplaying character focused on personal narrative and relationships.
    
    Avatars track roleplay stats like profession, alignment, and relationship status.
    Notable mechanic: Profession becomes permanently "Outlaw" if character murders their ex.
    Relationship status can only be changed through get_married() and divorce() methods.
    
    Attributes:
        _profession (str): Character's profession (e.g., "Merchant", "Outlaw")
        _alignment (str): Moral/ethical alignment (e.g., "Lawful Good", "Chaotic Evil")
        _history (str): Character backstory
        _relationship_status (RelationshipStatus): SINGLE, DATING, or MARRIED
        _spouse_name (str): Name of spouse if married, otherwise empty
        _name, _level, _hp, _xp, _character_class, _race (inherited from Character)
    
    Example:
        >>> avatar = Avatar("Elara", 4, 45, 30, "Cleric", "Elf", "Healer", "Neutral Good", "Once a temple priestess")
        >>> avatar.get_married("Theron")
        >>> avatar.set_profession("Outlaw")  # Fails - would need to call revenge() first
    """
    def __init__(
        self, 
        name: str, 
        level: int, 
        hp: int, 
        xp: int, 
        character_class: str, 
        race: str, 
        profession: str, 
        alignment: str, 
        history: str
    ) -> None:
        super().__init__(name, level, hp, xp, character_class, race)
        self._profession = profession
        self._alignment = alignment
        self._history = history
        self._relationship_status = RelationshipStatus.SINGLE
        self._spouse_name = ""
        
        
    def set_profession(self, profession: str) -> None:
        """Set profession. Cannot change if character is an Outlaw."""
        if self._profession != "Outlaw":
            self._profession = profession
        else:
            print("You've become an outlaw and can't change your profession!\n")
    
    
    def set_alignment(self, alignment: str) -> None:
        self._alignment = alignment
    
    
    def set_history(self, history: str) -> None:
        self._history = history
    
    
    def set_relationship_status(self, relationship_status: RelationshipStatus) -> None:
        """Set relationship status. Only works if not currently married."""
        if self._relationship_status != RelationshipStatus.MARRIED:
            self._relationship_status = relationship_status
        else:
            print("You're currently married and can't change your relationship status unless you get a divorce.\n")
            
            
    def get_married(self, spouse_name: str) -> None:
        """Marry a character. Sets spouse name and relationship status to MARRIED."""
        self._spouse_name = spouse_name
        self._relationship_status = RelationshipStatus.MARRIED
    
    
    def divorce(self) -> None:
        """Divorce current spouse. Only works if married."""
        if self._relationship_status == RelationshipStatus.MARRIED:
            self._relationship_status = RelationshipStatus.SINGLE
            self._spouse_name = ""
        else:
            print("You're not currently married and can't get divorced.\n")
    
    
    def revenge(self, kill_ex: bool) -> None:
        """
        Execute revenge on ex-spouse. Permanently sets profession to Outlaw if kill_ex=True.
        
        Args:
            kill_ex: True to kill ex and become Outlaw, False to spare them
        """
        if kill_ex:
            self._profession = "Outlaw"
            print(f"You successfully killed your ex {self._spouse_name} and've now become an outlaw!\n")
        else:
            print("You decided to spare your ex's life.\n")
    
    
    def __str__(self) -> str:
        status_map = {
            RelationshipStatus.SINGLE: "single",
            RelationshipStatus.DATING: "dating",
            RelationshipStatus.MARRIED: "married"
        }
        status = status_map[self._relationship_status]
        
        base_str = f"\nCharacter Type: Avatar \nName: {self._name} \nRace: {self._race} \nClass: {self._character_class} \nHealth: {self._hp} \nLevel: {self._level} \nExperience: {self._xp}/100 \nProfession: {self._profession} \nAlignment: {self._alignment} \nHistory: {self._history} \nRelationship Status: {status}"
        
        if self._relationship_status == RelationshipStatus.MARRIED:
            base_str += f" \nSpouse: {self._spouse_name}"
        
        return base_str + "\n"

    
    
    
class Battler(Character):
    """
    A combat-focused character with weapons, armor, and magic abilities.
    
    Battlers track battle stats and can use one spell per rest cycle.
    Armor Class affects defense, and spells recharge after resting.
    
    Attributes:
        _weapon (str): Currently equipped weapon (e.g., "Longsword", "Bow")
        _armor_class (int): Defense rating (higher is better)
        _spell (str): Name of known spell (e.g., "Fireball", "Heal")
        _spell_use (bool): True if spell is available, False if already used this rest cycle
        _name, _level, _hp, _xp, _character_class, _race (inherited from Character)
    
    Example:
        >>> battler = Battler("Kael", 6, 60, 50, "Fighter", "Human", "Greatsword", 16, "Fireball")
        >>> battler.take_dmg(15)  # Take damage
        >>> battler.use_spell()  # Cast spell
        >>> battler.rest()  # Recharge spell after battle
    """
    
    def __init__(
        self, 
        name: str, 
        level: int, 
        hp: int, 
        xp: int, 
        character_class: str, 
        race: str, 
        weapon: str, 
        armor_class: int, 
        spell: str
    ) -> None:
        super().__init__(name, level, hp, xp, character_class, race)
        self._weapon = weapon
        self._armor_class = armor_class
        self._spell = spell
        self._spell_use = True
        
    
    def set_weapon(self, weapon: str) -> None:
        if not weapon:
            raise ValueError("Weapon cannot be empty")
        self._weapon = weapon
    
    
    def set_armor_class(self, armor_class: int) -> None:
        if armor_class < 0:
            raise ValueError("Armor class cannot be negative")
        self._armor_class = armor_class
    
    
    def set_spell(self, spell: str) -> None:
        if not spell:
            raise ValueError("Spell cannot be empty")
        self._spell = spell
    
    
    def can_use_spell(self) -> bool:
        """Check if spell is currently available to cast."""
        return self._spell_use
    
    
    def use_spell(self) -> None:
        """Cast the spell. Can only be used once per rest cycle."""
        if self._spell_use:
            self._spell_use = False
        else:
            print(f"Spell already used. Rest to recharge.\n")
    
    
    def rest(self) -> None:
        """Rest and recharge spell for next use."""
        self._spell_use = True
    
    
    def take_dmg(self, damage: int) -> None:
        """Subtract damage from HP. Cannot go below 0."""
        self._hp = max(0, self._hp - damage)
    
    
    def __str__(self) -> str:
        return f"\nCharacter Type: Battler \nName: {self._name} \nRace: {self._race} \nClass: {self._character_class} \nHealth: {self._hp} \nLevel: {self._level} \nExperience: {self._xp}/100 \nWeapon: {self._weapon} \nArmor Class: {self._armor_class} \nSpell: {self._spell}\n"