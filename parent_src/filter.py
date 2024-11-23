import pandas as pd  # type:ignore
from Cli_utils import CliInput, CliOutput
from Menu import Menu
import sys
import os
import platform

# Dictionary to store user-defined custom functions
CUSTOM_FUNCTIONS = {}

def clear_terminal():
    """Clears the terminal screen."""
    if platform.system().lower() == "windows":
        os.system("cls")  # Windows
    else:
        os.system("clear")  # macOS/Linux

def filter_and_sort_csv(input_file, output_file, custom_function=None):
    df = pd.read_csv(input_file)

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='ignore')

    if custom_function:
        CliOutput.info("Applying custom function to the data.")
        df = custom_function(df)

    df.to_csv(output_file, index=False)
    CliOutput.success(f"Filtered and sorted data saved to {output_file}")

def add_custom_function():
    """Allows the user to add a custom function."""
    func_identifier = CliInput.prompt("Enter a string identifier to associate with your custom function")
    func_name = CliInput.prompt("Enter the name of the Python file (without .py extension) containing the custom function")
    function_to_add = CliInput.prompt("Enter the name of the function to use from the module (default: 'process')", default="process")

    try:
        # Add the directory containing the custom functions to sys.path
        module_dir = "./child_src"
        if module_dir not in sys.path:
            sys.path.append(module_dir)  # Append the directory to sys.path
        
        # Dynamically import the custom function module
        custom_module = __import__(func_name)  # Import based on the filename (without .py extension)
        
        # Use default 'process' if the user didn't specify a function
        if not hasattr(custom_module, function_to_add):
            CliOutput.warning(f"Custom function '{function_to_add}' not found, using default process function.")
            function_to_add = 'default_process'

        # Add default_process to the module if it doesn't exist
        if function_to_add == 'default_process':
            CUSTOM_FUNCTIONS[func_identifier] = default_process
            CliOutput.success(f"Default function 'process' added and associated with identifier '{func_identifier}'.")
        else:
            if hasattr(custom_module, function_to_add):
                CUSTOM_FUNCTIONS[func_identifier] = getattr(custom_module, function_to_add)
                CliOutput.success(f"Custom function '{function_to_add}' from '{func_name}.py' added and associated with identifier '{func_identifier}'.")
            else:
                CliOutput.error(f"The file '{func_name}.py' does not contain the function '{function_to_add}'.")
    
    except ImportError as e:
        CliOutput.error(f"Failed to import the file '{func_name}.py': {e}")
    except Exception as e:
        CliOutput.error(f"An error occurred: {e}")

def default_process(df):
    """Default process function to handle the DataFrame."""
    return df.dropna()  # Example of a default function

def execute_custom_function(input_file, output_file):
    """Allows the user to execute a previously added custom function."""
    if not CUSTOM_FUNCTIONS:
        CliOutput.warning("No custom functions available.")
        return

    CliOutput.info("Available custom functions:")
    for identifier, func in CUSTOM_FUNCTIONS.items():
        CliOutput.print(f"{identifier}. {func.__name__}", color="blue")

    func_identifier = CliInput.prompt("Enter the identifier of the custom function you want to execute")
    if func_identifier in CUSTOM_FUNCTIONS:
        clear_terminal()  # Clear the terminal screen before executing
        CliOutput.info(f"Executing custom function associated with identifier '{func_identifier}'.")
        filter_and_sort_csv(input_file, output_file, custom_function=CUSTOM_FUNCTIONS[func_identifier])
    else:
        CliOutput.error("Invalid function identifier.")

def main():
    CliOutput.info("Welcome to the CSV Custom Function Tool!")

    # Default values for input and output files
    input_file = CliInput.prompt("Enter the path to the input CSV file (default: result.csv)", default="result.csv")
    output_file = CliInput.prompt("Enter the path to save the output CSV file (default: filter.csv)", default="filter.csv")

    menu = Menu()
    menu.add_option("Add custom function", add_custom_function)
    menu.add_option("Execute custom function", lambda: execute_custom_function(input_file, output_file))
    menu.add_option("Clear terminal", clear_terminal)
    menu.add_option("Exit", lambda: CliOutput.success("Goodbye!") or exit())

    while True:
        menu.display()
        menu.select_option()

if __name__ == "__main__":
    main()
