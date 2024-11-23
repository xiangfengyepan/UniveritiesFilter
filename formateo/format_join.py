import os
import glob
import pandas as pd  # type:ignore
import argparse

def merge_csv_by_columns(input_dir, output_file, merge_columns=None, columns_to_merge=None):
    # Find all CSV files in the directory
    input_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    if not input_files:
        print("No file found")
        return  # Exit if no files are found

    merged_df = pd.DataFrame()

    for file in input_files:
        print(f"Processing {file}")
        
        try:
            # Read the current CSV file into a DataFrame
            df = pd.read_csv(file, on_bad_lines='skip', quotechar='"')  # Handle quoted commas
            
        except pd.errors.ParserError as e:
            print(f"Error reading {file}: {e}")
            continue

        # Check if all required columns exist in the file
        if merge_columns:
            missing_columns = [col for col in merge_columns if col not in df.columns]
            if missing_columns:
                print(f"Warning: Missing columns {missing_columns} in {file}. Skipping.")
                continue

        # If it's the first file, initialize merged_df
        if merged_df.empty:
            merged_df = df
        else:
            # Merge subsequent files on the specified columns
            merged_df = pd.merge(merged_df, df, on=merge_columns, how='outer')

    # If columns are specified, filter them; otherwise, keep all columns
    if columns_to_merge:
        merged_df = merged_df[columns_to_merge]
    
    # Save the merged DataFrame to the output CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Merge CSV files in a directory by multiple columns.')
    parser.add_argument('input_dir', type=str, help='Directory containing the CSV files.')
    parser.add_argument('output_file', type=str, help='Output file path for the merged CSV.')
    parser.add_argument('--merge_columns', type=str, help='Comma-separated list of columns to merge on (required).')
    parser.add_argument('--columns', type=str, help='Comma-separated list of columns to include in the merged file (optional).')

    args = parser.parse_args()

    # Print the input arguments for debugging
    print(f"Input Directory: {args.input_dir}")
    print(f"Output File: {args.output_file}")

    # Parse columns for merging and optional columns to include
    if args.merge_columns:
        merge_columns = [col.strip() for col in args.merge_columns.split(',')]
        print(f"Columns to Merge On: {merge_columns}")
    else:
        print("Error: --merge_columns is required.")
        return

    columns_to_merge = None
    if args.columns:
        # Strip spaces and split by commas
        columns_to_merge = [col.strip() for col in args.columns.split(',')]
        print(f"Columns to Include: {columns_to_merge}")
    else:
        print("No specific columns to merge (all columns will be included).")

    merge_csv_by_columns(args.input_dir, args.output_file, merge_columns=merge_columns, columns_to_merge=columns_to_merge)


if __name__ == "__main__":
    main()
