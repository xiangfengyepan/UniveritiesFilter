import argparse
import os

NUMBER_COLUMN_START = 4
NUMBER_COLUMN_END = 31

def extract_numbers(input_string):
    valid_numbers = {str(i) for i in range(10)}
    found_numbers = [char for char in input_string if char in valid_numbers]
    if found_numbers:
        number = int("".join(found_numbers))
        formatted_number = f"{number:,}".replace(",", ".")
    return formatted_number if found_numbers else "N/A"

def transform_list(input_list):
    if NUMBER_COLUMN_END < len(input_list) or len(input_list) < NUMBER_COLUMN_START :
        return input_list

    transformed_list = input_list[:NUMBER_COLUMN_START] + [extract_numbers(s) for s in input_list[NUMBER_COLUMN_START:NUMBER_COLUMN_END]]
    return transformed_list

def process_text(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        context = f.read()
    print(f"Llegint de: {input_filename}")
    
    result_lines = []  

    for line in context.split('\n'):
        line = line.strip()
    
        # solve casilles incorrectes
        list_line = transform_list(line.split(','))
        line = ",".join(list_line)

        # espaic en blanc per 0
        line = line.replace('N/A', '0')

        result_lines.append(line)

    with open(output_filename, "w") as f:
        f.write("Codi,Nom del centre d'estudi,Universitat,Branca,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27\n")
        f.write("\n".join(result_lines))

    print(f"Resultat escrit a: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and format lines in a file.')
    parser.add_argument('file_path', type=str, help='Path of the input file.')
    parser.add_argument('output_dir', type=str, help='Directory to save the formatted output file.')

    args = parser.parse_args()

    base_filename = os.path.splitext(os.path.basename(args.file_path))[0]
    input_directory = os.path.dirname(args.file_path)
    input_filename = os.path.join(input_directory, base_filename + ".csv")
    output_filename = os.path.join(args.output_dir, base_filename + ".csv")

    print(f"Solving issues pond: {input_filename} to {output_filename}")
    process_text(input_filename, output_filename)
