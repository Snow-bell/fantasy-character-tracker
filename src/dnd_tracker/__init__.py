"""
Fantasy Character Tracker

A polymorphic character management system using Binary Search Trees
for efficient level-based sorting and retrieval.

Classes:
    Character: Base character class with core stats and leveling
    Drunkard: Character archetype focused on alcohol and tavern brawling
    Avatar: Roleplay-focused character with relationships and profession
    Battler: Combat-focused character with weapons, armor, and spells
    BST: Binary Search Tree for character storage and retrieval
    Node: Node class for BST
    UI: User interface for the character tracker
"""

from .character import Character, Drunkard, Avatar, Battler, RelationshipStatus, XP_LEVEL_UP_THRESHOLD, DrunkardConstants
from .bst import BST, Node

__version__ = "1.0.0"
__author__ = "Michael Bell"
__all__ = [
    "Character",
    "Drunkard",
    "Avatar",
    "Battler",
    "RelationshipStatus",
    "XP_LEVEL_UP_THRESHOLD",
    "DrunkardConstants",
    "BST",
    "Node",
]