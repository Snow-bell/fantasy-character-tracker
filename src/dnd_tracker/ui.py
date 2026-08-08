"""
D&D Character Tracker User Interface
"""

from DnD_character import Character, Drunkard, Avatar, Battler
from DnD_bst import BST


class UI:
    """User interface for the D&D character tracker."""
    
    def __init__(self) -> None:
        self.__user_command: int = 10
    
    
    def get_command(self) -> int:
        return self.__user_command
    
    
    def set_command(self, command: int) -> None:
        self.__user_command = command
    
    
    def enter_command(self) -> None:
        """Get and validate command input from user."""
        try:
            command = int(input("\nPlease enter what you want to do: "))
            self.__user_command = command
        except ValueError:
            print("\nError: Invalid input. Please enter a number.\n")
            self.__user_command = 10
    
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n    Menu:")
        print("\t (1) Add new character")
        print("\t (2) Remove a character")
        print("\t (3) Retrieve a character's information")
        print("\t (4) Modify a character")
        print("\t (5) Display all characters")
        print("\t (9) Remove all characters")
        print("\t (0) Quit")
    
    
    def _get_character_type(self) -> str | None:
        """Prompt user for character type. Returns 'd', 'a', 'b', or None if invalid."""
        char_type = input("Is the character a Drunkard (d), Avatar (a), or Battler (b)? ").lower()
        if char_type not in ['d', 'a', 'b']:
            print("Error: Invalid character type.\n")
            return None
        return char_type
    
    
    def _get_base_character_stats(self) -> dict | None:
        """Prompt for base character stats common to all types."""
        try:
            return {
                'name': input("Character name: "),
                'char_class': input("Character class: "),
                'race': input("Character race: "),
                'hp': int(input("Hit points: ")),
            }
        except ValueError:
            print("Error: Invalid input for base stats.\n")
            return None
    
    
    def _create_new_character(self, char_type: str) -> Character | None:
        """Create a brand new level 1 character."""
        stats = self._get_base_character_stats()
        if not stats:
            return None
        
        try:
            if char_type == 'd':
                return Drunkard(stats['name'], 1, stats['hp'], 0, stats['char_class'], stats['race'])
            
            elif char_type == 'a':
                profession = input("Profession: ")
                alignment = input("Alignment: ")
                history = input("Backstory: ")
                return Avatar(stats['name'], 1, stats['hp'], 0, stats['char_class'], stats['race'], 
                            profession, alignment, history)
            
            elif char_type == 'b':
                weapon = input("Weapon: ")
                armor_class = int(input("Armor class: "))
                spell = input("Spell: ")
                return Battler(stats['name'], 1, stats['hp'], 0, stats['char_class'], stats['race'], 
                             weapon, armor_class, spell)
        except ValueError:
            print("Error: Invalid input.\n")
        
        return None
    
    
    def _add_existing_character(self, char_type: str) -> Character | None:
        """Add an existing character with custom level/XP."""
        stats = self._get_base_character_stats()
        if not stats:
            return None
        
        try:
            level = int(input("Level: "))
            xp = int(input("Experience points: "))
            
            if char_type == 'd':
                return Drunkard(stats['name'], level, stats['hp'], xp, stats['char_class'], stats['race'])
            
            elif char_type == 'a':
                profession = input("Profession: ")
                alignment = input("Alignment: ")
                history = input("Backstory: ")
                return Avatar(stats['name'], level, stats['hp'], xp, stats['char_class'], stats['race'], 
                            profession, alignment, history)
            
            elif char_type == 'b':
                weapon = input("Weapon: ")
                armor_class = int(input("Armor class: "))
                spell = input("Spell: ")
                return Battler(stats['name'], level, stats['hp'], xp, stats['char_class'], stats['race'], 
                             weapon, armor_class, spell)
        except ValueError:
            print("Error: Invalid input.\n")
        
        return None
    
    
    def _get_character_safe(self, bst: BST, name: str) -> Character | None:
        """Retrieve a character from BST and validate it exists."""
        node = bst.retrieve(name)
        if node is None:
            print(f"\nNo character named '{name}' found in the system.\n")
            return None
        return node.get_data()[0]
    
    
    def _modify_drunkard(self, character: Drunkard) -> None:
        """Handle Drunkard-specific modifications."""
        print("\t (1) Level up")
        print("\t (2) Add XP")
        print("\t (3) Take a drink")
        print("\t (4) Sleep (reset BAC)")
        print("\t (5) Start a tavern brawl")
        
        try:
            choice = int(input("\nWhat would you like to do: "))
            
            if choice == 1:
                character + 100
                print(f"{character._name} leveled up!\n")
            elif choice == 2:
                xp = int(input("How much XP to add: "))
                character + xp
                print(f"Added {xp} XP.\n")
            elif choice == 3:
                drinks = int(input("How many drinks: "))
                character.drink(drinks)
                print(f"{character._name} drank {drinks} mugs of ale!\n")
            elif choice == 4:
                character.sleep()
                print("You feel rested and sober!\n")
            elif choice == 5:
                character.drunk_fight()
            else:
                print("Invalid choice.\n")
        except ValueError:
            print("Error: Invalid input.\n")
    
    
    def _modify_avatar(self, character: Avatar) -> None:
        """Handle Avatar-specific modifications."""
        print("\t (1) Level up")
        print("\t (2) Add XP")
        print("\t (3) Change profession")
        print("\t (4) Get married")
        print("\t (5) Get divorced")
        print("\t (6) Get revenge")
        
        try:
            choice = int(input("\nWhat would you like to do: "))
            
            if choice == 1:
                character + 100
                print(f"{character._name} leveled up!\n")
            elif choice == 2:
                xp = int(input("How much XP to add: "))
                character + xp
                print(f"Added {xp} XP.\n")
            elif choice == 3:
                profession = input("New profession: ")
                character.set_profession(profession)
                print(f"Changed profession to {profession}.\n")
            elif choice == 4:
                spouse = input("Spouse name: ")
                character.get_married(spouse)
                print(f"Congratulations on your marriage to {spouse}!\n")
            elif choice == 5:
                character.divorce()
                print("You're now divorced.\n")
            elif choice == 6:
                kill = input("Kill your ex? (y/n): ").lower() == 'y'
                character.revenge(kill)
            else:
                print("Invalid choice.\n")
        except ValueError:
            print("Error: Invalid input.\n")
    
    
    def _modify_battler(self, character: Battler) -> None:
        """Handle Battler-specific modifications."""
        print("\t (1) Level up")
        print("\t (2) Add XP")
        print("\t (3) Change weapon")
        print("\t (4) Take damage")
        print("\t (5) Use spell")
        print("\t (6) Change spell")
        print("\t (7) Change armor class")
        print("\t (8) Rest (recharge spell)")
        
        try:
            choice = int(input("\nWhat would you like to do: "))
            
            if choice == 1:
                character + 100
                print(f"{character._name} leveled up!\n")
            elif choice == 2:
                xp = int(input("How much XP to add: "))
                character + xp
                print(f"Added {xp} XP.\n")
            elif choice == 3:
                weapon = input("New weapon: ")
                character.set_weapon(weapon)
                print(f"Equipped {weapon}.\n")
            elif choice == 4:
                damage = int(input("Damage taken: "))
                character.take_dmg(damage)
                print(f"{character._name} took {damage} damage. HP: {character._hp}\n")
            elif choice == 5:
                character.use_spell()
            elif choice == 6:
                spell = input("New spell: ")
                character.set_spell(spell)
                print(f"Learned {spell}!\n")
            elif choice == 7:
                ac = int(input("New armor class: "))
                character.set_armor_class(ac)
                print(f"Armor class set to {ac}.\n")
            elif choice == 8:
                character.rest()
                print("You rested. Spell recharged.\n")
            else:
                print("Invalid choice.\n")
        except ValueError:
            print("Error: Invalid input.\n")
    
    
    def command_chain(self, bst: BST) -> None:
        """Execute the command selected by the user."""
        
        if self.__user_command == 1:
            # Add new character
            char_type = self._get_character_type()
            if not char_type:
                return
            
            mode = input("Create new character (0) or add existing (1): ")
            if mode == '0':
                character = self._create_new_character(char_type)
            else:
                character = self._add_existing_character(char_type)
            
            if character:
                bst.insert(character)
                print(f"\n{character._name} has been added to the system.\n")
        
        
        elif self.__user_command == 2:
            # Remove character
            name = input("Enter character name to remove: ")
            bst.remove_character(name)
        
        
        elif self.__user_command == 3:
            # Retrieve character info
            name = input("Enter character name to retrieve: ")
            character = self._get_character_safe(bst, name)
            if character:
                print(character)
        
        
        elif self.__user_command == 4:
            # Modify character
            name = input("Enter character name to modify: ")
            character = self._get_character_safe(bst, name)
            if not character:
                return
            
            if isinstance(character, Drunkard):
                self._modify_drunkard(character)
            elif isinstance(character, Avatar):
                self._modify_avatar(character)
            elif isinstance(character, Battler):
                self._modify_battler(character)
        
        
        elif self.__user_command == 5:
            # Display all characters
            bst.display()
        
        
        elif self.__user_command == 9:
            # Remove all characters
            bst.remove_all()