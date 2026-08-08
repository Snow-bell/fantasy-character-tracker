# Architecture Overview

## System Design

The Fantasy Character Tracker is built on a polymorphic character management system using a Binary Search Tree (BST) for efficient storage and retrieval.

### High-Level Architecture

```
┌──────────────────────────────────┐
│ User Interface (UI) │
│ - Menu system │
│ - Input validation │
│ - Character operations │
└──────────────┬───────────────────┘
│
┌──────────────▼───────────────────┐
│ Binary Search Tree (BST) │
│ - Sorted by Level → XP │
│ - O(log n) retrieval │
│ - Stores Character nodes │
└──────────────┬───────────────────┘
│
┌──────────────▼───────────────────┐
│ Character Class Hierarchy │
│ ┌──────────────────────────┐ │
│ │ Character (Base) │ │
│ │ - Level, XP, HP, Name │ │
│ │ - Level-up mechanics │ │
│ └──┬──────────┬──────────┬─┘ │
│ │ │ │ │
│ ┌──▼──┐ ┌───▼──┐ ┌──▼───┐ │
│ │Drunk│ │Avatar│ │Battle│ │
│ │-BAC │ │-Prof │ │-Weap.│ │
│ │-Brawl │-Marr.│ │-Spell│ │
│ └──────┘ └──────┘ └──────┘ │
└──────────────────────────────────┘
```

## Data Flow

1. **User Input** → UI validates and parses commands
2. **Character Operations** → Create, modify, or retrieve characters
3. **BST Storage** → Characters sorted by (level, XP)
4. **Name-Based Retrieval** → Full tree search (independent of BST ordering)
5. **Output** → Display character stats or confirmation

## Why Binary Search Tree?

- ✅ **O(log n) insertion/deletion** - Fast character management
- ✅ **Sorted by level** - Natural grouping for display
- ✅ **Handles duplicates** - Multiple characters at same level/XP stored in node lists
- ✅ **Scalable** - Efficient even with thousands of characters

## Package Structure

```
src/dnd_tracker/
├── init.py # Package exports
├── character.py # Character class hierarchy
├── bst.py # Binary Search Tree implementation
├── ui.py # User interface
└── main.py # Entry point
```