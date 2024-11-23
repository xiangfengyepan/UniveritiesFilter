import pandas as pd  # type:ignore
from Cli_utils import CliInput, CliOutput
from Menu import Menu

# Dictionary to store user-defined custom functions
CUSTOM_FUNCTIONS = {}


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
    func_number = CliInput.prompt("Enter a number to associate with your custom function")
    func_name = CliInput.prompt("Enter the name of the Python file (without .py extension) containing the custom function")
    try:
        # Dynamically import the custom function module
        custom_module = __import__("./child_src/" + func_name)
        if hasattr(custom_module, "process"):
            CUSTOM_FUNCTIONS[func_number] = custom_module.process
            CliOutput.success(f"Custom function '{func_name}' added and associated with number {func_number}.")
        else:
            CliOutput.error(f"The file '{func_name}.py' does not contain a 'process' function.")
    except ImportError as e:
        CliOutput.error(f"Failed to import the file '{func_name}.py': {e}")


def execute_custom_function(input_file, output_file):
    """Allows the user to execute a previously added custom function."""
    if not CUSTOM_FUNCTIONS:
        CliOutput.warning("No custom functions available.")
        return

    CliOutput.info("Available custom functions:")
    for number, func in CUSTOM_FUNCTIONS.items():
        CliOutput.print(f"{number}. {func.__name__}", color="blue")

    func_number = CliInput.prompt("Enter the number of the custom function you want to execute")
    if func_number in CUSTOM_FUNCTIONS:
        CliOutput.info(f"Executing custom function associated with number {func_number}.")
        filter_and_sort_csv(input_file, output_file, custom_function=CUSTOM_FUNCTIONS[func_number])
    else:
        CliOutput.error("Invalid function number.")


def main():
    CliOutput.info("Welcome to the CSV Custom Function Tool!")
    input_file = CliInput.prompt("Enter the path to the input CSV file")
    output_file = CliInput.prompt("Enter the path to save the output CSV file")

    menu = Menu()
    menu.add_option(1, "Add custom function", add_custom_function)
    menu.add_option(2, "Execute custom function", lambda: execute_custom_function(input_file, output_file))
    menu.add_option(3, "Exit", lambda: CliOutput.success("Goodbye!") or exit())

    while True:
        menu.display()
        menu.select_option()


if __name__ == "__main__":
    main()