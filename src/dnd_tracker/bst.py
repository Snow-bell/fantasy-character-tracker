"""
Binary Search Tree implementation for D&D characters.

The BST is sorted by character level (primary) and XP (tiebreaker).
Characters with the same level/XP are stored together in node lists.
Name-based retrieval searches the entire tree (not just BST ordering).
"""

from __future__ import annotations
from DnD_character import Character, Drunkard, Avatar, Battler


class Node:
    """
    A node in the BST containing a list of characters with the same level/XP.
    
    Attributes:
        __data (list[Character]): Characters at this node (same level/XP)
        __left (Node): Left subtree (lower level/XP characters)
        __right (Node): Right subtree (higher level/XP characters)
    """
    
    def __init__(self, data: Character | None = None) -> None:
        """Initialize a node with a character (or empty list if None)."""
        self.__data = [data] if data else []
        self.__left: Node | None = None
        self.__right: Node | None = None
    
    
    def get_data(self) -> list[Character]:
        return self.__data
    
    def get_left(self) -> Node | None:
        return self.__left
    
    def get_right(self) -> Node | None:
        return self.__right
    
    def get_data_type(self) -> type | None:
        """Return the type of the first character in this node's data list."""
        if not self.__data:
            return None
        first_char = self.__data[0]
        if isinstance(first_char, Drunkard):
            return Drunkard
        if isinstance(first_char, Avatar):
            return Avatar
        if isinstance(first_char, Battler):
            return Battler
        return Character
    
    def set_data(self, new_data: list[Character]) -> None:
        self.__data = new_data
    
    def set_left(self, new_left: Node | None) -> None:
        self.__left = new_left
    
    def set_right(self, new_right: Node | None) -> None:
        self.__right = new_right
    
    
    def insert(self, new_data: Character) -> None:
        """Insert a character into this node's data list (for duplicate level/XP)."""
        if new_data is None:
            return
        
        if not self.__data:
            self.__data.append(new_data)
        elif new_data < self.__data[0]:
            if self.__left is None:
                self.__left = Node(new_data)
            else:
                self.__left.insert(new_data)
        elif new_data > self.__data[0]:
            if self.__right is None:
                self.__right = Node(new_data)
            else:
                self.__right.insert(new_data)
        else:
            # Same level/XP - add to existing node's list
            self.__data.append(new_data)
    
    
    def display(self) -> None:
        """Print all characters at this node."""
        for character in self.__data:
            print(character)


class BST:
    """
    Binary Search Tree for D&D characters, sorted by level then XP.
    
    Supports insertion, deletion, display (in-order traversal), and name-based retrieval.
    Characters with identical level/XP are stored together in node lists.
    """
    
    def __init__(self) -> None:
        self.__root: Node | None = None
    
    
    def insert(self, new_data: Character) -> None:
        """Insert a character into the BST. Wrapper for insert_rec()."""
        if self.__root is None:
            self.__root = Node(new_data)
        else:
            self.insert_rec(self.__root, new_data)
    
    
    def insert_rec(self, curr: Node, new_data: Character) -> None:
        """Recursively insert a character into the BST by level/XP comparison."""
        if curr is None:
            return
        
        if new_data < curr.get_data()[0]:
            if curr.get_left() is None:
                curr.set_left(Node(new_data))
            else:
                self.insert_rec(curr.get_left(), new_data)
        elif new_data > curr.get_data()[0]:
            if curr.get_right() is None:
                curr.set_right(Node(new_data))
            else:
                self.insert_rec(curr.get_right(), new_data)
        else:
            # Same level/XP - add to this node's list
            curr.insert(new_data)
    
    
    def display(self) -> None:
        """Display all characters in the BST (in-order traversal by level/XP)."""
        if self.__root is None:
            print("There are no characters in our system.\n")
            return
        print("Here are all your characters (sorted by level, then XP):\n")
        self.display_rec(self.__root)
    
    
    def display_rec(self, curr: Node | None) -> None:
        """In-order traversal to display all characters."""
        if curr is None:
            return
        self.display_rec(curr.get_left())
        curr.display()
        self.display_rec(curr.get_right())
    
    
    def remove_all(self) -> None:
        """Remove all characters from the BST."""
        if self.__root is None:
            print("There are no characters in our system.\n")
            return
        self.__root = None
        print("All characters have been removed.\n")
    
    
    def retrieve(self, name: str) -> Node | None:
        """
        Retrieve a character by name (searches entire tree, not just BST ordering).
        
        Returns the Node containing the character, or None if not found.
        """
        if self.__root is None:
            return None
        result: list[Node] = []
        self._retrieve_by_name_rec(self.__root, name, result)
        return result[0] if result else None
    
    
    def _retrieve_by_name_rec(
        self, 
        curr: Node | None, 
        name: str, 
        results: list[Node]
    ) -> None:
        """Recursively search entire tree for character by name."""
        if curr is None:
            return
        
        # Check if any character in this node matches the name
        for character in curr.get_data():
            if character.compare_name(name) == 0:
                results.append(curr)
                return
        
        # Search both subtrees
        self._retrieve_by_name_rec(curr.get_left(), name, results)
        self._retrieve_by_name_rec(curr.get_right(), name, results)
    
    
    def remove_character(self, name: str) -> None:
        """Remove all instances of a character with the given name."""
        if self.__root is None:
            print("There are no characters in our system.\n")
            return
        self.__root = self.remove_character_rec(self.__root, name)
    
    
    def remove_character_rec(self, curr: Node | None, name: str) -> Node | None:
        """Recursively remove a character by name from the BST."""
        if curr is None:
            return None
        
        # Check if this node contains the character to remove
        for i, character in enumerate(curr.get_data()):
            if character.compare_name(name) == 0:
                # Found it - remove from this node's list
                curr.get_data().pop(i)
                
                # If node list is now empty, remove the node itself
                if not curr.get_data():
                    if curr.get_left() is None:
                        return curr.get_right()
                    elif curr.get_right() is None:
                        return curr.get_left()
                    else:
                        # Node has two children - use in-order successor
                        successor = self.find_min(curr.get_right())
                        curr.set_data(successor.get_data())
                        curr.set_right(self.remove_character_rec(curr.get_right(), successor.get_data()[0]._name))
                
                return curr
        
        # Character not in this node - search subtrees
        curr.set_left(self.remove_character_rec(curr.get_left(), name))
        curr.set_right(self.remove_character_rec(curr.get_right(), name))
        
        return curr
    
    
    def find_min(self, curr: Node) -> Node:
        """Find the node with minimum value (leftmost node in subtree)."""
        while curr.get_left() is not None:
            curr = curr.get_left()
        return curr