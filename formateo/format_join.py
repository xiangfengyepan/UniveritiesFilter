import os
import glob
import pandas as pd  
import argparse
import sys
from parent_src.Cli_utils import CliOutput  # Assuming CliOutput is implemented

def transform_cell_values(df):
    """
    Function to transform the values of the cells in the DataFrame.
    Ensures that all values are treated as strings, and numeric precision is preserved.
    """
    for column in df.columns:
        # Convert all values to strings to ensure consistency
        df[column] = df[column].astype(str)

        if df[column].dtype == 'object':  # If the column contains string data
            # Convert all string values to uppercase and replace NaN with 'N/A'
            df[column] = df[column].str.upper().fillna('N/A')
        # No need for numeric check as everything is now treated as a string.

def merge_csv_by_columns(input_dir, output_file, merge_columns=None, columns_to_merge=None):
    input_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    if not input_files:
        CliOutput.error("No file found")
        return

    merged_df = pd.DataFrame()

    for file in input_files:
        CliOutput.info(f"Processing {file}")
        
        try:
            # Read the CSV with dtype=str to treat all values as strings
            df = pd.read_csv(file, on_bad_lines='skip', quotechar='"', dtype=str)
            CliOutput.info(f"Available columns in {file}: {df.columns.tolist()}")

            # Normalize columns
            df.columns = df.columns.str.strip()

            # Apply transformations on cell values before merging
            transform_cell_values(df)

        except pd.errors.ParserError as e:
            CliOutput.error(f"Error reading {file}: {e}")
            continue

        if merge_columns:
            merge_columns = [col.strip() for col in merge_columns]  # Normalize merge columns
            missing_columns = [col for col in merge_columns if col not in df.columns]
            if missing_columns:
                CliOutput.warning(f"Missing columns {missing_columns} in {file}. Skipping.")
                continue

        if merged_df.empty:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on=merge_columns, how='outer')

    if columns_to_merge:
        columns_to_merge = [col.strip() for col in columns_to_merge]  # Normalize columns to merge
        try:
            merged_df = merged_df[columns_to_merge]
        except KeyError as e:
            CliOutput.error(f"KeyError: {e}. Check columns in the input files.")

    merged_df.to_csv(output_file, index=False)
    CliOutput.success(f"Merged CSV saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Merge CSV files in a directory by multiple columns.')
    parser.add_argument('input_dir', type=str, help='Directory containing the CSV files.')
    parser.add_argument('output_file', type=str, help='Output file path for the merged CSV.')
    parser.add_argument('--merge_columns', type=str, help='Comma-separated list of columns to merge on (required).')
    parser.add_argument('--columns', type=str, help='Comma-separated list of columns to include in the merged file (optional).')

    args = parser.parse_args()

    CliOutput.info(f"Input Directory: {args.input_dir}")
    CliOutput.info(f"Output File: {args.output_file}")

    if args.merge_columns:
        merge_columns = [col.strip() for col in args.merge_columns.split(',')]
        CliOutput.info(f"Columns to Merge On: {merge_columns}")
    else:
        CliOutput.error("Error: --merge_columns is required.")
        return

    columns_to_merge = None
    if args.columns:
        columns_to_merge = [col.strip() for col in args.columns.split(',')]
        CliOutput.info(f"Columns to Include: {columns_to_merge}")
    else:
        CliOutput.info("No specific columns to merge (all columns will be included).")

    merge_csv_by_columns(args.input_dir, args.output_file, merge_columns=merge_columns, columns_to_merge=columns_to_merge)

if __name__ == "__main__":
    main()
