import pandas as pd

def combine_header_and_values(headers, values):
    return [headers] + values

def parse_value(value, decimal_separator=',', thousand_separator='.'):
    """
    Parse a string value and return it as a float, int, or string.
    Handles custom decimal and thousand separators.
    
    :param value: The string value to be parsed.
    :param decimal_separator: The character used for decimal points (default is ',').
    :param thousand_separator: The character used for thousand separators (default is '.').
    :return: The parsed value as a float, int, or string.
    """
    # Remove the thousand separator before parsing as a number
    if thousand_separator:
        value = value.replace(thousand_separator, '')

    # Check if the value contains a decimal separator
    if decimal_separator in value:
        try:
            # Try to convert the value to a float
            return float(value.replace(decimal_separator, '.'))
        except ValueError:
            # Return the original value if it can't be converted to a float
            return value
    else:
        try:
            # Try to convert the value to an integer
            return int(value)
        except ValueError:
            # Return the original value if it can't be converted to an integer
            return value

def parse_value_all(data_list):
    """Apply parse_value function to each element in the data_list."""
    # Use map to apply parse_value to each element in each row
    return [list(map(parse_value, row)) for row in data_list]

class DataFrameProcessor:
    def __init__(self, df):
        self.df = df

    def get_headers(self):
        """
        Returns the headers (columns) of the DataFrame as a list of strings.
        """
        return list(self.df.columns)
    
                

    def csv_to_list_with_lines(self):
        """
        Converts the DataFrame into a list of strings where each element is a row in CSV format.
        Each value in the DataFrame is converted to a string.
        """
        data_list = self.df.astype(str).values.tolist()
        return data_list

    @staticmethod
    def list_to_csv_with_lines(data_list):
        """
        Convert a list of lists (where each inner list represents a row) into a DataFrame.
        The first inner list is used as the column names.
        """
        if not data_list:
            raise ValueError("The input data_list is empty.")
        
        # The first row will be used as the column names
        columns = data_list[0]
        
        # The remaining rows are the data
        rows = data_list[1:]
        
        # Return the DataFrame
        return pd.DataFrame(rows, columns=columns)

