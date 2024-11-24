import pandas as pd  
from Cli_utils import CliInput, CliOutput
from Menu import Menu
import sys
import os
import platform

# Dictionary to store user-defined custom functions
CUSTOM_FUNCTIONS = {}

# Store the identifier of the last successfully used function
LAST_FUNCTION_IDENTIFIER = None


def clear_terminal():
    """Clears the terminal screen."""
    if platform.system().lower() == "windows":
        os.system("cls")  # Windows
    else:
        os.system("clear")  # macOS/Linux


def pretty_format_df(df, max_width=None):
    def format_value(x, column_name):
        """Format values for pretty printing, assuming all values are strings."""
        # If column is 'Preu orientatiu' and the value is not 'NaN' (string 'nan')
        if column_name.lower() == 'preu orientatiu' and x.lower() != 'nan':
            # Add the '€' symbol if it's not 'NaN'
            return f"{x}€"
        
        # For specific columns, replace dot with a comma (e.g., 'PAU / CFGS', 'Més grans de 25 anys', etc.)
        if column_name.lower() in ['pau / cfgs', 'més grans de 25 anys', 'titulats universitaris', 'més grans de 45 anys']:
            return x.replace('.', ',')  # Replace dot with comma
        
        return x  # Otherwise, return the string as is

    def truncate_value(value, width):
        """Truncate a value to fit within the specified maximum width."""
        value_str = str(value)
        if max_width and len(value_str) > width:
            return value_str[: width - 3] + "..."
        return value_str

    # Apply formatting to the DataFrame
    formatted_df = df.copy()
    for col in formatted_df.columns:
        formatted_df[col] = formatted_df[col].apply(lambda x: format_value(x, col))

    # Convert all column headers to uppercase
    headers = formatted_df.columns.str.upper()

    # Determine the maximum width for each column (header + data)
    col_widths = [
        min(max(len(str(cell)) for cell in [header] + formatted_df[col].astype(str).tolist()), max_width or float("inf"))
        for header, col in zip(headers, formatted_df.columns)
    ]

    # Ensure that columns numbered '1, 2, 3, ..., 27' have the same width
    for i, col in enumerate(formatted_df.columns):
        if col.strip().isdigit() and int(col.strip()) in range(1, 28):  # Check if column name is 1, 2, ..., 27
            col_widths[i] = 2  # Set the width of these columns to 2 (to keep them uniform)

    # Create the formatted header (right-aligned for numbers, left-aligned for text)
    header_line = " | ".join(
        truncate_value(header, width).ljust(width) for header, width in zip(headers, col_widths)
    )

    # Add a separator line
    separator_line = "-+-".join("-" * width for width in col_widths)

    # Format the rows (right-aligned for numbers, left-aligned for text)
    rows = []
    for i, (_, row) in enumerate(formatted_df.iterrows()):
        formatted_row = " | ".join(
            truncate_value(str(cell), width).rjust(width) if isinstance(df[col].iloc[0], (int, float)) else truncate_value(str(cell), width).ljust(width)
            for cell, width, col in zip(row, col_widths, df.columns)
        )
        # Alternate row separator for readability
        if i > 0:
            rows.append(separator_line)  # Add a separator between rows
        rows.append(formatted_row)

    # Combine everything into a single formatted string
    formatted_table = f"{header_line}\n{separator_line}\n" + "\n".join(rows)

    return formatted_table

def save_pretty_format_to_file(df, output_file):
    """Save a pretty-formatted DataFrame to a text file."""
    formatted_table = pretty_format_df(df, 20)
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


def update(output_file, input_file):
    """Update the output file with the latest sort/filter applied."""
    global LAST_FUNCTION_IDENTIFIER

    if LAST_FUNCTION_IDENTIFIER is None:
        CliOutput.warning("No previous custom function has been applied.")
        return

    custom_function = CUSTOM_FUNCTIONS.get(LAST_FUNCTION_IDENTIFIER)
    if not custom_function:
        CliOutput.error(f"No function found for identifier '{LAST_FUNCTION_IDENTIFIER}'.")
        return

    CliOutput.info(f"Reapplying the last used custom function: {LAST_FUNCTION_IDENTIFIER}")
    try:
        df = pd.read_csv(input_file)

        # Apply custom function (ensure numeric precision is maintained)
        df = custom_function(df)

        save_pretty_format_to_file(df, output_file)
        CliOutput.success(f"Output file updated with last applied filter: {output_file}")
    except Exception as e:
        CliOutput.error(f"Error updating the output file: {e}")


def filter_and_sort_csv(input_file, output_file, custom_function=None, func_identifier=None):
    """
    Filter and sort CSV data and save it with formatting.
    Ensures all values are read and processed as strings to preserve their original format.
    """
    global LAST_FUNCTION_IDENTIFIER

    # Read the CSV with dtype=str to treat all values as strings
    df = pd.read_csv(input_file, dtype=str)
    print(df.columns)
    CliOutput.info(f"Data read from {input_file} (all values as strings):")

    if custom_function:
        CliOutput.info(f"Applying custom function with the identifier {func_identifier} to the data.")
        df = custom_function(df)

    save_pretty_format_to_file(df, output_file)

    # Update LAST_FUNCTION_IDENTIFIER
    if func_identifier:
        LAST_FUNCTION_IDENTIFIER = func_identifier
        CliOutput.success(f"Last applied function updated to: {func_identifier}")

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
        filter_and_sort_csv(input_file, output_file, custom_function=CUSTOM_FUNCTIONS[func_identifier], func_identifier=func_identifier)
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
    main()
