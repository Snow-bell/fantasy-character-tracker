"""
Comprehensive pytest suite for D&D Character Tracker
Tests Character, Drunkard, Avatar, Battler, and BST classes
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from dnd_tracker import Character, Drunkard, Avatar, Battler, RelationshipStatus, XP_LEVEL_UP_THRESHOLD, DrunkardConstants, BST, Node


# ==================== FIXTURES ====================

@pytest.fixture
def base_character():
    """Create a base character for testing."""
    return Character("Aragorn", 5, 50, 45, "Ranger", "Human")


@pytest.fixture
def drunkard():
    """Create a drunkard for testing."""
    return Drunkard("Stumbles McGee", 3, 40, 25, "Bard", "Dwarf")


@pytest.fixture
def avatar():
    """Create an avatar for testing."""
    return Avatar("Elara", 4, 45, 30, "Cleric", "Elf", "Healer", "Neutral Good", "Temple priestess")


@pytest.fixture
def battler():
    """Create a battler for testing."""
    return Battler("Kael", 6, 60, 50, "Fighter", "Human", "Greatsword", 16, "Fireball")


@pytest.fixture
def bst():
    """Create an empty BST for testing."""
    return BST()


# ==================== CHARACTER TESTS ====================

class TestCharacterInit:
    """Test Character initialization."""
    
    def test_init_valid(self, base_character):
        assert base_character._name == "Aragorn"
        assert base_character._level == 5
        assert base_character._hp == 50
        assert base_character._xp == 45
        assert base_character._character_class == "Ranger"
        assert base_character._race == "Human"
    
    def test_init_defaults(self):
        char = Character("TestChar", 1, 30, 0, "Warrior", "Elf")
        assert char._xp == 0
        assert char._level == 1


class TestCharacterSetters:
    """Test Character setter methods with validation."""
    
    def test_set_name_valid(self, base_character):
        base_character.set_name("Legolas")
        assert base_character._name == "Legolas"
    
    def test_set_name_empty_raises(self, base_character):
        with pytest.raises(ValueError):
            base_character.set_name("")
    
    def test_set_character_class_valid(self, base_character):
        base_character.set_character_class("Mage")
        assert base_character._character_class == "Mage"
    
    def test_set_character_class_empty_raises(self, base_character):
        with pytest.raises(ValueError):
            base_character.set_character_class("")
    
    def test_set_race_valid(self, base_character):
        base_character.set_race("Dwarf")
        assert base_character._race == "Dwarf"
    
    def test_set_race_empty_raises(self, base_character):
        with pytest.raises(ValueError):
            base_character.set_race("")
    
    def test_set_level_valid(self, base_character):
        base_character.set_level(10)
        assert base_character._level == 10
    
    def test_set_level_negative_raises(self, base_character):
        with pytest.raises(ValueError):
            base_character.set_level(0)
    
    def test_set_hp_valid(self, base_character):
        base_character.set_hp(100)
        assert base_character._hp == 100
    
    def test_set_hp_negative_clamps_to_zero(self, base_character):
        base_character.set_hp(-10)
        assert base_character._hp == 0


class TestCharacterLevelUp:
    """Test character leveling mechanics."""
    
    def test_level_up_at_threshold(self, base_character):
        base_character._xp = XP_LEVEL_UP_THRESHOLD
        base_character.level_up()
        assert base_character._level == 6
        assert base_character._xp == 0
    
    def test_level_up_above_threshold(self, base_character):
        base_character._xp = 150
        base_character.level_up()
        assert base_character._level == 6
        assert base_character._xp == 50
    
    def test_level_up_below_threshold_no_change(self, base_character):
        base_character._xp = 50
        base_character.level_up()
        assert base_character._level == 5
        assert base_character._xp == 50
    
    def test_multiple_level_ups(self, base_character):
        base_character._xp = 250
        base_character.level_up()
        assert base_character._level == 7
        assert base_character._xp == 50


class TestCharacterComparison:
    """Test character name comparison methods."""
    
    def test_compare_name_equal(self, base_character):
        assert base_character.compare_name("Aragorn") == 0
    
    def test_compare_name_less(self, base_character):
        assert base_character.compare_name("Zebra") == -1
    
    def test_compare_name_greater(self, base_character):
        assert base_character.compare_name("Aardvark") == 1
    
    def test_compare_data_name_equal(self, base_character):
        other = Character("Aragorn", 3, 30, 20, "Mage", "Elf")
        assert base_character.compare_data_name(other) == 0
    
    def test_compare_data_name_less(self, base_character):
        other = Character("Zebra", 3, 30, 20, "Mage", "Elf")
        assert base_character.compare_data_name(other) == -1
    
    def test_compare_data_name_greater(self, base_character):
        other = Character("Aardvark", 3, 30, 20, "Mage", "Elf")
        assert base_character.compare_data_name(other) == 1
    
    def test_compare_data_name_wrong_type_raises(self, base_character):
        with pytest.raises(TypeError):
            base_character.compare_data_name("NotACharacter")


class TestCharacterOperatorOverloads:
    """Test XP and level comparison operators."""
    
    def test_add_xp_no_level_up(self, base_character):
        result = base_character + 10
        assert base_character._xp == 55
        assert base_character._level == 5
        assert result == 55
    
    def test_add_xp_with_level_up(self, base_character):
        result = base_character + 55
        assert base_character._xp == 0
        assert base_character._level == 6
        assert result == 0
    
    def test_sub_xp_normal(self, base_character):
        result = base_character - 10
        assert base_character._xp == 35
        assert result == 35
    
    def test_sub_xp_clamps_to_zero(self, base_character):
        result = base_character - 100
        assert base_character._xp == 0
        assert result == 0
    
    def test_lt_by_level(self):
        char1 = Character("A", 3, 50, 50, "Warrior", "Human")
        char2 = Character("B", 5, 50, 50, "Warrior", "Human")
        assert char1 < char2
    
    def test_lt_by_xp_same_level(self):
        char1 = Character("A", 5, 50, 30, "Warrior", "Human")
        char2 = Character("B", 5, 50, 50, "Warrior", "Human")
        assert char1 < char2
    
    def test_gt_by_level(self):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 3, 50, 50, "Warrior", "Human")
        assert char1 > char2
    
    def test_eq_same_level_and_xp(self):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 5, 50, 50, "Mage", "Elf")
        assert char1 == char2
    
    def test_not_eq_different_level(self):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 6, 50, 50, "Warrior", "Human")
        assert not (char1 == char2)
    
    def test_not_eq_different_xp(self):
        char1 = Character("A", 5, 50, 30, "Warrior", "Human")
        char2 = Character("B", 5, 50, 50, "Warrior", "Human")
        assert not (char1 == char2)


# ==================== DRUNKARD TESTS ====================

class TestDrunkardDrink:
    """Test Drunkard drinking mechanics."""
    
    def test_drink_increases_bac(self, drunkard):
        initial_bac = drunkard._bac
        drunkard.drink(1)
        assert drunkard._bac > initial_bac
    
    def test_drink_multiple(self, drunkard):
        drunkard.drink(3)
        assert drunkard._bac > 0.03  # At least 0.01 * 3
    
    def test_drink_dead_character_no_effect(self, drunkard):
        drunkard._hp = 0
        drunkard.drink(5)
        assert drunkard._bac == 0.0
    
    def test_drink_stops_at_danger_threshold(self, drunkard):
        drunkard._bac = DrunkardConstants.BAC_DANGER_THRESHOLD
        drunkard.drink(10)
        # Should stop at first drink since already at danger threshold
        assert drunkard._bac == DrunkardConstants.BAC_DANGER_THRESHOLD


class TestDrunkardSleep:
    """Test Drunkard sleep mechanics."""
    
    def test_sleep_resets_bac(self, drunkard):
        drunkard.drink(5)
        assert drunkard._bac > 0
        drunkard.sleep()
        assert drunkard._bac == 0.0


class TestDrunkardAlcoholPoisoning:
    """Test alcohol poisoning mechanics."""
    
    def test_alcohol_poisoning_returns_bool(self, drunkard):
        result = drunkard.alcohol_poisoning()
        assert isinstance(result, bool)
    
    def test_alcohol_poisoning_can_kill(self, drunkard):
        # Run multiple times to have decent chance of hitting the 30%
        killed = False
        for _ in range(100):
            test_drunk = Drunkard("Test", 1, 50, 0, "Bard", "Dwarf")
            if test_drunk.alcohol_poisoning():
                killed = True
                break
        # Statistically should kill at least once in 100 tries
        assert killed


class TestDrunkardDrunkFight:
    """Test drunk fight mechanics."""
    
    def test_drunk_fight_dead_character_no_effect(self, drunkard):
        drunkard._hp = 0
        drunkard.drunk_fight()
        # Should return early, no exception
    
    def test_drunk_fight_affects_xp(self, drunkard):
        initial_xp = drunkard._xp
        drunkard._bac = 0.5  # High BAC = guaranteed success
        drunkard.drunk_fight()
        # XP should change (either gain or lose)
        assert drunkard._xp != initial_xp


# ==================== AVATAR TESTS ====================

class TestAvatarMarriage:
    """Test Avatar marriage mechanics."""
    
    def test_get_married(self, avatar):
        avatar.get_married("Theron")
        assert avatar._spouse_name == "Theron"
        assert avatar._relationship_status == RelationshipStatus.MARRIED
    
    def test_divorce(self, avatar):
        avatar.get_married("Theron")
        avatar.divorce()
        assert avatar._relationship_status == RelationshipStatus.SINGLE
        assert avatar._spouse_name == ""
    
    def test_divorce_not_married_no_effect(self, avatar):
        avatar.divorce()
        assert avatar._relationship_status == RelationshipStatus.SINGLE


class TestAvatarRevenge:
    """Test Avatar revenge mechanics."""
    
    def test_revenge_kill_becomes_outlaw(self, avatar):
        avatar.get_married("Enemy")
        avatar.revenge(True)
        assert avatar._profession == "Outlaw"
    
    def test_revenge_spare_stays_same_profession(self, avatar):
        original_profession = avatar._profession
        avatar.get_married("Enemy")
        avatar.revenge(False)
        assert avatar._profession == original_profession
    
    def test_outlaw_cannot_change_profession(self, avatar):
        avatar._profession = "Outlaw"
        avatar.set_profession("Merchant")
        assert avatar._profession == "Outlaw"


class TestAvatarRelationshipStatus:
    """Test Avatar relationship status enum."""
    
    def test_relationship_status_enum_values(self):
        assert RelationshipStatus.SINGLE.value == 0
        assert RelationshipStatus.DATING.value == 1
        assert RelationshipStatus.MARRIED.value == 2
    
    def test_set_relationship_status_when_single(self, avatar):
        avatar.set_relationship_status(RelationshipStatus.DATING)
        assert avatar._relationship_status == RelationshipStatus.DATING
    
    def test_cannot_change_status_when_married(self, avatar):
        avatar.get_married("Spouse")
        avatar.set_relationship_status(RelationshipStatus.SINGLE)
        assert avatar._relationship_status == RelationshipStatus.MARRIED


# ==================== BATTLER TESTS ====================

class TestBattlerSpellMechanics:
    """Test Battler spell usage."""
    
    def test_can_use_spell_initially(self, battler):
        assert battler.can_use_spell() is True
    
    def test_use_spell_sets_flag_false(self, battler):
        battler.use_spell()
        assert battler._spell_use is False
    
    def test_rest_recharges_spell(self, battler):
        battler.use_spell()
        battler.rest()
        assert battler._spell_use is True


class TestBattlerDamage:
    """Test Battler damage mechanics."""
    
    def test_take_dmg_normal(self, battler):
        initial_hp = battler._hp
        battler.take_dmg(15)
        assert battler._hp == initial_hp - 15
    
    def test_take_dmg_clamps_to_zero(self, battler):
        battler.take_dmg(100)
        assert battler._hp == 0
    
    def test_take_dmg_zero_damage(self, battler):
        initial_hp = battler._hp
        battler.take_dmg(0)
        assert battler._hp == initial_hp


class TestBattlerSetters:
    """Test Battler setter validation."""
    
    def test_set_weapon_valid(self, battler):
        battler.set_weapon("Longsword")
        assert battler._weapon == "Longsword"
    
    def test_set_weapon_empty_raises(self, battler):
        with pytest.raises(ValueError):
            battler.set_weapon("")
    
    def test_set_armor_class_valid(self, battler):
        battler.set_armor_class(18)
        assert battler._armor_class == 18
    
    def test_set_armor_class_negative_raises(self, battler):
        with pytest.raises(ValueError):
            battler.set_armor_class(-1)
    
    def test_set_spell_valid(self, battler):
        battler.set_spell("Lightning Bolt")
        assert battler._spell == "Lightning Bolt"
    
    def test_set_spell_empty_raises(self, battler):
        with pytest.raises(ValueError):
            battler.set_spell("")


# ==================== BST TESTS ====================

class TestNodeBasics:
    """Test Node class."""
    
    def test_node_init_with_data(self, base_character):
        node = Node(base_character)
        assert len(node.get_data()) == 1
        assert node.get_data()[0] == base_character
    
    def test_node_init_empty(self):
        node = Node()
        assert node.get_data() == []
    
    def test_node_get_data_type(self, drunkard):
        node = Node(drunkard)
        assert node.get_data_type() == Drunkard
    
    def test_node_get_data_type_empty(self):
        node = Node()
        assert node.get_data_type() is None


class TestBSTInsertion:
    """Test BST insertion."""
    
    def test_insert_single_character(self, bst, base_character):
        bst.insert(base_character)
        assert bst._BST__root is not None
    
    def test_insert_multiple_characters_sorts_by_level(self, bst):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 3, 40, 30, "Mage", "Elf")
        char3 = Character("C", 7, 60, 60, "Ranger", "Human")
        
        bst.insert(char1)
        bst.insert(char2)
        bst.insert(char3)
        
        # Root should be char1 (level 5)
        assert bst._BST__root.get_data()[0] == char1
    
    def test_insert_duplicate_level_xp_adds_to_list(self, bst):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 5, 50, 50, "Mage", "Elf")
        
        bst.insert(char1)
        bst.insert(char2)
        
        # Both should be in root's data list
        assert len(bst._BST__root.get_data()) == 2


class TestBSTRetrieval:
    """Test BST character retrieval."""
    
    def test_retrieve_existing_character(self, bst, base_character):
        bst.insert(base_character)
        node = bst.retrieve("Aragorn")
        assert node is not None
        assert node.get_data()[0] == base_character
    
    def test_retrieve_non_existing_character(self, bst):
        node = bst.retrieve("NonExistent")
        assert node is None
    
    def test_retrieve_finds_character_regardless_of_tree_position(self, bst):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 3, 40, 30, "Mage", "Elf")
        char3 = Character("C", 7, 60, 60, "Ranger", "Human")
        
        bst.insert(char1)
        bst.insert(char2)
        bst.insert(char3)
        
        # Find character in different positions
        assert bst.retrieve("A") is not None
        assert bst.retrieve("B") is not None
        assert bst.retrieve("C") is not None


class TestBSTRemoval:
    """Test BST character removal."""
    
    def test_remove_character_by_name(self, bst):
        char = Character("Aragorn", 5, 50, 50, "Ranger", "Human")
        bst.insert(char)
        bst.remove_character("Aragorn")
        assert bst.retrieve("Aragorn") is None
    
    def test_remove_non_existing_character(self, bst):
        bst.remove_character("NonExistent")
        # Should not raise error
    
    def test_remove_all(self, bst):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 3, 40, 30, "Mage", "Elf")
        
        bst.insert(char1)
        bst.insert(char2)
        bst.remove_all()
        
        assert bst._BST__root is None


class TestBSTFindMin:
    """Test BST find_min helper."""
    
    def test_find_min_returns_leftmost(self, bst):
        char1 = Character("A", 5, 50, 50, "Warrior", "Human")
        char2 = Character("B", 3, 40, 30, "Mage", "Elf")
        char3 = Character("C", 7, 60, 60, "Ranger", "Human")
        
        bst.insert(char1)
        bst.insert(char2)
        bst.insert(char3)
        
        min_node = bst.find_min(bst._BST__root)
        assert min_node.get_data()[0]._level == 3


# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests combining multiple components."""
    
    def test_create_and_level_up_drunkard(self, bst):
        drunk = Drunkard("Barley", 2, 35, 80, "Bard", "Dwarf")
        bst.insert(drunk)
        
        retrieved = bst.retrieve("Barley").get_data()[0]
        retrieved + 30  # Should level up
        
        assert retrieved._level == 3
        assert retrieved._xp == 10
    
    def test_marriage_and_revenge_flow(self, bst):
        avatar = Avatar("Elara", 5, 50, 50, "Cleric", "Elf", "Healer", "Good", "Once a priestess")
        bst.insert(avatar)
        
        retrieved = bst.retrieve("Elara").get_data()[0]
        retrieved.get_married("Theron")
        retrieved.divorce()
        retrieved.revenge(True)
        
        assert retrieved._profession == "Outlaw"
    
    def test_battler_combat_flow(self, bst):
        battler = Battler("Kael", 5, 50, 50, "Fighter", "Human", "Sword", 15, "Fireball")
        bst.insert(battler)
        
        retrieved = bst.retrieve("Kael").get_data()[0]
        retrieved.take_dmg(20)
        retrieved.use_spell()
        retrieved.rest()
        
        assert retrieved._hp == 30
        assert retrieved._spell_use is True