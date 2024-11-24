# my_custom_function.py
from DataFrameProcessor import DataFrameProcessor, combine_header_and_values
from parent_src.Cli_utils import CliInput, CliOutput

def sort_list(row):
    return row[2].strip().lower() == 'barcelona'

def process(df):
    dfp = DataFrameProcessor(df)
    data_list = dfp.csv_to_list_with_lines()


    # data_list = [
    #       [..., ..., ...]
    #       [..., ..., ...]
    #       ....
    # ]

    data_list.sort(key=sort_list, reverse=True)



    header = dfp.get_headers()
    data_list = combine_header_and_values(header, data_list)
    df = DataFrameProcessor.list_to_csv_with_lines(data_list)
    return df