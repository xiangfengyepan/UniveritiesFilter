import pandas as pd

def combine_header_and_values(headers, values):
    """
    Combine headers with the corresponding values into a single list.
    
    :param headers: List of column headers.
    :param values: List of values (rows) corresponding to the headers.
    :return: A combined list where the first element is the headers and the rest are the values (rows).
    """
    # Combines the headers and values into one list, with headers as the first element
    return [headers] + values

def parse_value(value, decimal_separator=',', thousand_separator='.'):
    """
    Parse a string value into a numeric type (float or int), or return it as a string.
    This function handles custom decimal and thousand separators for parsing.

    :param value: The string value to be parsed (could represent a number).
    :param decimal_separator: The character used for decimal points (default is ',').
    :param thousand_separator: The character used for thousand separators (default is '.').
    :return: The parsed value as a float, int, or string, depending on the input format.
    """
    # Remove the thousand separator (if provided) before parsing as a number
    if thousand_separator:
        value = value.replace(thousand_separator, '')  # Remove thousand separators (e.g., dots)

    # Check if the value contains a decimal separator (e.g., a comma)
    if decimal_separator in value:
        try:
            # Try to convert the value to a float using the specified decimal separator
            return float(value.replace(decimal_separator, '.'))  # Convert ',' to '.' and parse as float
        except ValueError:
            # If it can't be converted, return the original string value
            return value
    else:
        try:
            # If the value doesn't contain a decimal point, try converting it to an integer
            return int(value)
        except ValueError:
            # If it can't be converted to an integer, return the original value (assumed to be a string)
            return value

def parse_value_all(data_list):
    """
    Apply the `parse_value` function to each element in the data_list, transforming strings to 
    their corresponding numeric types (if applicable), or returning them as strings.

    :param data_list: List of lists (rows) where each element can be a string representation of a number.
    :return: A new list where each value has been parsed into the appropriate numeric or string type.
    """
    # Apply parse_value to each element in each row using map, then convert it back to a list
    return [list(map(parse_value, row)) for row in data_list]

class DataFrameProcessor:
    """
    A class that provides methods for manipulating and converting a pandas DataFrame into other formats
    (such as CSV-like lists). It also includes utility functions for parsing and processing data.
    """

    def __init__(self, df):
        """
        Initializes the DataFrameProcessor with a pandas DataFrame.
        
        :param df: The pandas DataFrame that this processor will operate on.
        """
        self.df = df  # Store the DataFrame as an instance variable

    def get_headers(self):
        """
        Get the headers (column names) from the DataFrame.
        
        :return: A list of strings representing the column names.
        """
        # Convert DataFrame columns to a list and return
        return list(self.df.columns)
    
    def csv_to_list_with_lines(self):
        """
        Convert the DataFrame into a list of lists, where each inner list represents a row
        in CSV format. Each value in the DataFrame is converted to a string.

        :return: A list of lists where each sublist represents a row (values as strings).
        """
        # Convert the DataFrame values to strings and convert to a list of rows
        data_list = self.df.astype(str).values.tolist()
        return data_list

    @staticmethod
    def list_to_csv_with_lines(data_list):
        """
        Convert a list of lists (where each inner list represents a row) into a pandas DataFrame.
        The first row will be treated as column headers, and the remaining rows will be treated as data.

        :param data_list: A list of lists, where the first list contains column headers, 
                          and the subsequent lists contain the data rows.
        :return: A pandas DataFrame created from the list of lists.
        :raises ValueError: If the input data_list is empty.
        """
        # Raise an error if the input data_list is empty
        if not data_list:
            raise ValueError("The input data_list is empty.")
        
        # The first row will be used as the column names for the DataFrame
        columns = data_list[0]
        
        # The remaining rows represent the actual data in the DataFrame
        rows = data_list[1:]
        
        # Create and return a pandas DataFrame from the rows and columns
        return pd.DataFrame(rows, columns=columns)
