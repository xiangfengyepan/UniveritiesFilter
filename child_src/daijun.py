# my_custom_function.py
from DataFrameProcessor import DataFrameProcessor, combine_header_and_values, parse_value, filter_rows
from parent_src.Cli_utils import CliInput, CliOutput

def filter_values(row):
    if 'barcelona' in row[2].lower():  # Ejemplo de condición: valor mayor que 10
        return True
    return False

def sort_list(row):
    return ('barcelona' in row[2].lower()) * 10 + ('U. PÚBL.' in row[4].lower()) * 10000 

def process(df):
    dfp = DataFrameProcessor(df)
    data_list = dfp.csv_to_list_with_lines()

    data_list.sort(key=sort_list, reverse=True)
    data_list = filter_rows(data_list, filter_values)

    header = dfp.get_headers()
    data_list = combine_header_and_values(header, data_list)
    df = DataFrameProcessor.list_to_csv_with_lines(data_list, header[0:5])
    return df