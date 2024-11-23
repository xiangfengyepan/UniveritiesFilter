import re
import argparse
import os

def aline_text(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        context = f.read()
    print(f"Llegint de: {input_filename}")
    
    result_lines = []  
    current_code_line = None 
    find_code = False

    for line in context.split('\n'):
        line = line.strip()
        line = line.replace('  ', ' ')
        
        while line.startswith('N/A,'):
            line = line.replace('N/A,', '', 1)
        if line.endswith(',N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A'):
            line = line.replace(',N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A', '', 1)
        if line.endswith(',N/A,N/A,N/A,N/A,N/A,N/A,N/A'):
            line = line.replace(',N/A,N/A,N/A,N/A,N/A,N/A,N/A', '', 1)

        line = line.replace('.0', '')


        if line.startswith("Grau") or line.startswith("Total"):
            find_code = False

        match = re.match(r"^\d{5}$", line.split(',')[0])
        if match:
            find_code = True
            if current_code_line:
                result_lines.append(current_code_line)

            current_code_line = line
            continue

        # elimina el principit
        if not find_code:
            continue

        if find_code and current_code_line is not None:
            current_code_line += " " + line

    if current_code_line:
        result_lines.append(current_code_line)

    with open(output_filename, "w") as f:
        f.write("\n".join(result_lines))

    print(f"Resultat escrit a: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and format lines in a file.')
    parser.add_argument('file_path', type=str, help='Name of the input file.')
    parser.add_argument('output_dir', type=str, help='Directory to save the formatted output file.')

    args = parser.parse_args()

    base_filename = os.path.splitext(os.path.basename(args.file_path))[0]
    input_directory = os.path.dirname(args.file_path)
    input_filename = os.path.join(input_directory, base_filename + ".csv")
    output_filename = os.path.join(args.output_dir, base_filename + "_formated.csv")

    print(f"Aligning text: {input_filename} to {output_filename}")
    aline_text(input_filename, output_filename)