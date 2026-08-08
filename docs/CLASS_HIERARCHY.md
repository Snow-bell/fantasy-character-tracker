# Class Hierarchy

## Character (Base Class)

The foundation for all character types. Handles core RPG mechanics.

### Attributes
- `_name` (str): Character's name
- `_level` (int): Experience level
- `_hp` (int): Hit points (health)
- `_xp` (int): Experience points (0-99 per level)
- `_character_class` (str): Class type (Warrior, Mage, etc.)
- `_race` (str): Race (Human, Elf, Dwarf, etc.)

### Key Methods
- `level_up()` - Auto-level when XP ≥ 100
- `__add__(xp)` - Gain XP with auto-leveling
- `__sub__(xp)` - Lose XP (floor at 0)
- `__lt__, __gt__, __le__, __ge__, __eq__` - Comparison by (level, xp)
- `compare_name(name)` - String comparison for retrieval

---

## Drunkard(Character)

A character archetype focused on alcohol consumption and tavern brawling.

### Unique Attributes
- `_bac` (float): Blood Alcohol Content (0.0 to 0.5+)

### Key Methods
- `drink(num_drinks)` - Increase BAC, risk alcohol poisoning at BAC ≥ 0.4
- `sleep()` - Reset BAC to 0
- `alcohol_poisoning()` - 30% chance of death when BAC ≥ 0.4
- `drunk_fight()` - Gain/lose XP based on BAC success chance

### Mechanics
- **BAC Range 0.0-0.1**: 20% chance to start fight
- **BAC Range 0.1-0.4**: Increases by 10% per range
- **BAC ≥ 0.4**: 100% chance + death risk per drink

---

## Avatar(Character)

A roleplay-focused character with relationships and personal narrative.

### Unique Attributes
- `_profession` (str): Character's job/role
- `_alignment` (str): Moral alignment
- `_history` (str): Backstory
- `_relationship_status` (RelationshipStatus): SINGLE, DATING, or MARRIED
- `_spouse_name` (str): Name of spouse if married

### Key Methods
- `get_married(spouse_name)` - Enter marriage
- `divorce()` - Exit marriage
- `revenge(kill_ex)` - Permanently become "Outlaw" if kill_ex=True
- `set_profession(profession)` - Change profession (locked if Outlaw)

### Mechanics
- **Profession Lock**: Once "Outlaw", cannot be changed
- **Relationship States**: Controlled via marriage/divorce only
- **Revenge Flow**: Must divorce before revenge

---

## Battler(Character)

A combat-focused character with weapons, armor, and spells.

### Unique Attributes
- `_weapon` (str): Currently equipped weapon
- `_armor_class` (int): Defense rating (higher is better)
- `_spell` (str): Known spell name
- `_spell_use` (bool): True if spell available, False if used

### Key Methods
- `take_dmg(damage)` - Subtract damage from HP (floor at 0)
- `use_spell()` - Cast spell (marks as used)
- `rest()` - Recharge spell for next use
- `can_use_spell()` - Check if spell is available

### Mechanics
- **One Spell Per Rest**: Spell charge-based system
- **Damage Capping**: HP cannot go below 0
- **Stat Validation**: Armor class must be non-negative

---

## Inheritance Benefits

All character types inherit:
- ✅ Base stats (level, HP, XP, name, class, race)
- ✅ Leveling system
- ✅ XP operators (+/-)
- ✅ Comparison logic (for BST sorting)
- ✅ Name-based retrieval

This **DRY principle** means:
- Centralized stat management
- Consistent leveling across all types
- Polymorphic behavior through method overriding
- Easy to extend with new character types