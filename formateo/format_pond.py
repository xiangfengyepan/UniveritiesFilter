
import argparse
import os
import sys
from parent_src.Cli_utils import CliOutput  # Importing CliOutput for better message handling

NUMBER_COLUMN_START = 4
NUMBER_COLUMN_END = 31

def extract_numbers(input_string):
    valid_numbers = {str(i) for i in range(10)}
    found_numbers = [char for char in input_string if char in valid_numbers]
    if found_numbers:
        number = int("".join(found_numbers))
        formatted_number = f"{number:,}".replace(",", ".")
        return formatted_number
    return "N/A"

def transform_list(input_list):
    if NUMBER_COLUMN_END < len(input_list) or len(input_list) < NUMBER_COLUMN_START:
        return input_list

    transformed_list = input_list[:NUMBER_COLUMN_START] + [extract_numbers(s) for s in input_list[NUMBER_COLUMN_START:NUMBER_COLUMN_END]]
    return transformed_list

def process_text(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as f:
            context = f.read()
        CliOutput.info(f"Llegint de: {input_filename}")
    except FileNotFoundError:
        CliOutput.error(f"No s'ha trobat el fitxer: {input_filename}")
        return
    except Exception as e:
        CliOutput.error(f"Error al llegir el fitxer {input_filename}: {e}")
        return

    result_lines = []

    try:
        for line in context.split('\n'):
            line = line.strip()

            # Solve incorrect cells
            list_line = transform_list(line.split(','))
            line = ",".join(list_line)

            # Replace "N/A" with 0
            line = line.replace('N/A', '0')

            result_lines.append(line)

        with open(output_filename, "w") as f:
            f.write("Codi,Nom del centre d'estudi,Universitat,Branca,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27\n")
            f.write("\n".join(result_lines))

        CliOutput.success(f"Resultat escrit a: {output_filename}")
    except Exception as e:
        CliOutput.error(f"Error al processar el fitxer {input_filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Process and format lines in a file.')
    parser.add_argument('file_path', type=str, help='Path of the input file.')
    parser.add_argument('output_dir', type=str, help='Directory to save the formatted output file.')

    args = parser.parse_args()

    base_filename = os.path.splitext(os.path.basename(args.file_path))[0]
    input_directory = os.path.dirname(args.file_path)
    input_filename = os.path.join(input_directory, base_filename + ".csv")
    output_filename = os.path.join(args.output_dir, base_filename + ".csv")

    if not os.path.exists(args.file_path):
        CliOutput.error(f"El fitxer d'entrada no existeix: {args.file_path}")
        exit(1)

    if not os.path.exists(args.output_dir):
        CliOutput.warning(f"El directori de sortida no existeix. Creant: {args.output_dir}")
        os.makedirs(args.output_dir)

    CliOutput.info(f"Solving issues pond: {input_filename} to {output_filename}")
    process_text(input_filename, output_filename)

if __name__ == "__main__":
    module_dir = "./parent_src"
    if module_dir not in sys.path:
        sys.path.append(module_dir)

    main()
