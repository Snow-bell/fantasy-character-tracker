# Fantasy Character Tracker

A character management system using Binary Search Trees and object-oriented design principles in Python.

## Project Overview

This project demonstrates:
- BST implementation for character storage and retrieval
- Polymorphic class hierarchy (Character, Drunkard, Avatar, Battler)
- Comprehensive unit testing with pytest
- Type hints and input validation

## Installation

**Requirements:** Python 3.12+

**Setup:**
```bash
git clone https://github.com/YOUR_USERNAME/fantasy-character-tracker.git
cd fantasy-character-tracker
pip install -e .
pip install -e ".[dev]"  # for testing
```

## Usage

Run the application:
```bash
fantasy-tracker
```

### Example Code

```python
from src.dnd_tracker import Drunkard, BST

# Create and store a character
drunkard = Drunkard("Stumbles", 3, 40, 25, "Bard", "Dwarf")
bst = BST()
bst.insert(drunkard)

# Retrieve
node = bst.retrieve("Stumbles")
character = node.get_data()[0]
```

## Character Types

**Drunkard** - BAC system, tavern brawls, alcohol poisoning  
**Avatar** - Relationships, professions, revenge mechanic  
**Battler** - Weapons, armor class, spell system

See `docs/CLASS_HIERARCHY.md` for details.

## Testing

```bash
pytest                                    # Run all tests
pytest --cov=src/dnd_tracker              # With coverage
pytest -v                                 # Verbose
```

150+ test cases covering all classes and edge cases.

## Project Structure

```
src/dnd_tracker/
├── character.py # Character classes
├── bst.py # Binary Search Tree
├── ui.py # User interface
└── main.py # Entry point

tests/
└── test_character.py # Test suite

docs/
├── ARCHITECTURE.md
└── CLASS_HIERARCHY.md
```

## Key Features

- Binary Search Tree sorted by level + XP
- Polymorphic character classes with inheritance
- Type hints on all methods
- Input validation and error handling
- Comprehensive test coverage

## License

Apache License 2.0