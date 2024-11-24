# my_custom_function.py

# Importing necessary modules and functions
from DataFrameProcessor import (
    DataFrameProcessor,  # Class to handle DataFrame processing
    combine_header_and_values,  # Function to combine header and values into a structured list
    parse_value,  # Function to parse individual values in the data
    filter_rows  # Function to filter rows based on a condition
)
from parent_src.Cli_utils import CliInput, CliOutput  # CLI utilities for input and output operations

# Function to filter rows based on a condition
def filter_values(row):
    # Check if the third column (index 2) contains the word "barcelona" (case-insensitive)
    if 'barcelona' in row[2].lower():
        return True  # Include this row in the filtered results
    return False  # Exclude this row from the filtered results

# Function to define a sorting key for rows
def sort_list(row):
    # Prioritize rows containing "barcelona" in the third column (index 2)
    # and "U. PÚBL." in the fifth column (index 4)
    # Rows with "U. PÚBL." are given much higher priority
    return ('barcelona' in row[2].lower()) * 10 + ('U. PÚBL.' in row[4].lower()) * 10000

# Main processing function
def process(df):
    # Initialize the DataFrameProcessor with the input DataFrame
    dfp = DataFrameProcessor(df)

    # Convert the DataFrame to a list of rows with lines preserved
    data_list = dfp.csv_to_list_with_lines()

    # Sort the data list using the custom sorting key defined in sort_list
    data_list.sort(key=sort_list, reverse=True)

    # Filter the rows based on the condition defined in filter_values
    # data_list = filter_rows(data_list, filter_values)

    # Extract the header from the DataFrame
    header = dfp.get_headers()

    # Combine the header with the filtered and sorted data list
    data_list = combine_header_and_values(header, data_list)

    # Convert the processed list back to a DataFrame
    # Only include the first 5 columns from the header
    df = DataFrameProcessor.list_to_csv_with_lines(data_list, header)
    
    # Return the processed DataFrame
    return df
