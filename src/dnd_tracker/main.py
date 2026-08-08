"""
D&D Character Tracker - Main
"""

from DnD_character import Character, Drunkard, Avatar, Battler
from DnD_bst import BST
from DnD_ui import UI


def main() -> None:
    """Run the D&D character tracker application."""
    dnd_bst = BST()
    ui = UI()
    
    try:
        while ui.get_command() != 0:
            ui.display_menu()
            ui.enter_command()
            ui.command_chain(dnd_bst)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.\n")
    
    print("Thank you for using our D&D character tracker!\n")


if __name__ == "__main__":
    main()