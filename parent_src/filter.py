import pandas as pd  
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

def pretty_format_df(df):
    """Pretty format DataFrame as a string for writing to a file with right-aligned numbers and left-aligned text."""
    
    # Format the columns (except for 'Codi' and numeric columns like 1, 2, 3, ...)
    def format_value(x, column_name):
        if isinstance(x, (int, float)):
            # Skip 'Codi' and numeric column names (e.g., '1', '2', '3')
            if column_name == 'Codi' or column_name.isdigit():
                return str(x)  # Keep raw data for 'Codi' and numeric columns
            # Format with commas for thousands and 3 decimals
            return f"{x:,.3f}"
        return str(x)

    # Apply formatting to the DataFrame
    for col in df.columns:
        df[col] = df[col].apply(lambda x: format_value(x, col))

    # Convert all column headers to uppercase
    headers = df.columns.str.upper()

    # Determine the maximum width for each column (header + data)
    col_widths = [max(len(str(cell)) for cell in [header] + df[col].astype(str).tolist()) for header, col in zip(headers, df.columns)]

    # Create the formatted header (left-aligned for text, right-aligned for numbers)
    header_line = " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))

    # Add a separator line
    separator_line = "-+-".join("-" * width for width in col_widths)

    # Format the rows (right-aligned for numbers, left-aligned for text)
    rows = []
    for _, row in df.iterrows():
        formatted_row = " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
        rows.append(formatted_row)

    # Combine everything into a single formatted string
    formatted_table = f"{header_line}\n{separator_line}\n" + "\n".join(rows)

    return formatted_table


def save_pretty_format_to_file(df, output_file):
    """Save a pretty-formatted DataFrame to a text file."""
    formatted_table = pretty_format_df(df)
    with open(output_file, "w") as f:
        f.write(formatted_table)
    CliOutput.success(f"Formatted table saved to {output_file}")


def export(input_file, export_file):
    """Export the CSV file without any formatting (raw data)."""
    try:
        df = pd.read_csv(input_file)
        df.to_csv(export_file, index=False)
        CliOutput.success(f"Data exported to {export_file} without formatting.")
    except Exception as e:
        CliOutput.error(f"Error exporting the file: {e}")

def update(output_file, input_file, custom_function=None):
    """Update the output file with the latest sort/filter applied."""
    try:
        df = pd.read_csv(input_file)

        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='ignore')

        if custom_function:
            CliOutput.info("Applying custom function to the data.")
            df = custom_function(df)

        df.to_csv(output_file, index=False)
        CliOutput.success(f"Output file updated: {output_file}")
    except Exception as e:
        CliOutput.error(f"Error updating the output file: {e}")

def filter_and_sort_csv(input_file, output_file, custom_function=None):
    """Filter and sort CSV data and save it with formatting."""
    df = pd.read_csv(input_file)

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='ignore')

    if custom_function:
        CliOutput.info("Applying custom function to the data.")
        df = custom_function(df)

    save_pretty_format_to_file(df, output_file)

    CliOutput.success(f"Filtered and sorted data saved to {output_file} with formatting.")

def add_custom_function():
    """Allows the user to add a custom function."""
    func_identifier = CliInput.prompt("Enter a string identifier to associate with your custom function")
    file_name = CliInput.prompt("Enter the name of the Python file (without .py extension) containing the custom function")
    func_name = CliInput.prompt("Enter the name of the function to use from the module", default="process")

    try:
        # Add the directory containing the custom functions to sys.path
        module_dir = "./child_src"
        if module_dir not in sys.path:
            sys.path.append(module_dir)  # Append the directory to sys.path
        
        # Dynamically import the custom function module
        custom_module = __import__(file_name)  # Import based on the filename (without .py extension)
        
        # Check if the module has the user-defined function
        if hasattr(custom_module, func_name):
            CUSTOM_FUNCTIONS[func_identifier] = getattr(custom_module, func_name)
            CliOutput.success(f"Custom function '{func_name}' from '{file_name}.py' added and associated with identifier '{func_identifier}'.")
        else:
            CliOutput.error(f"The file '{file_name}.py' does not contain the function '{func_name}'.")
    
    except ImportError as e:
        CliOutput.error(f"Failed to import the file '{file_name}.py': {e}")
    except Exception as e:
        CliOutput.error(f"An error occurred: {e}")

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
    menu.add_option("Export data without formatting", lambda: export(input_file, "exported_data.csv"))
    menu.add_option("Update output file with last applied filter", lambda: update(output_file, input_file))
    menu.add_option("Exit", lambda: CliOutput.success("Goodbye!") or exit())

    while True:
        menu.display()
        menu.select_option()

if __name__ == "__main__":
    print(sys.path)

    main()
