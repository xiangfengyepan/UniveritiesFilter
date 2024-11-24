# my_custom_function.py
from child_src.DataFrameProcessor import DataFrameProcessor as DataFilter 
import sys
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)
print(sys.path)


def process(df):
    # Collect indices of rows where 'Població' is not 'Barcelona'
    indices_to_drop = df[df['Població'] != 'Barcelona'].index
    
    # Drop the rows with the collected indices
    df.drop(indices_to_drop, inplace=True)

    return df