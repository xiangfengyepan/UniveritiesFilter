import os
import platform
from Cli_utils import CliOutput, CliInput

def clear_terminal():
    """Clears the terminal screen."""
    if platform.system().lower() == "windows":
        os.system("cls")  # Windows
    else:
        os.system("clear")  # macOS/Linux



class Menu:
    def __init__(self):
        self.options = []
        self.menu_prompt = "Please select an action:"

    def add_option(self, description, action):
        """Adds an option to the menu and assigns it an automatic index starting from 1."""
        # Create a new index based on the current length of the options list + 1
        option_number = len(self.options) + 1
        self.options.append({'number': option_number, 'description': description, 'action': action})

    def display(self):
        """Displays the menu."""
        CliOutput.print("\n" + self.menu_prompt, color="bold")
        for option in self.options:
            CliOutput.print(f"{option['number']}. {option['description']}", color="blue")

    def select_option(self):
        """Handles the selection of an option."""
        choice = CliInput.prompt("Enter your choice")
        
        # Execute the selected option's action if valid
        for option in self.options:
            if choice == str(option['number']):
                option['action']()  # Call the associated action
                return True
        CliOutput.error("Invalid choice, please try again.")

        return False
