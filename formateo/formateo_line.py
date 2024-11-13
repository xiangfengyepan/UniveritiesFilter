import re
import argparse

def process_lines(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        i = 0
        combined_line = ""
        skip_until_lit = False
        

            
        while i < len(lines):
            line = lines[i].strip()
            
            if "2024" in line:
                skip_until_lit = True
            
            if skip_until_lit:
                if "Lit" in line:
                    skip_until_lit = False
                i += 1
                continue
            
            if re.match(r'^\d{5}', line):
                if combined_line:
                    outfile.write(combined_line + "\n")
                combined_line = line
            else:
                combined_line += " " + line.strip()
            i += 1

        if combined_line:
            outfile.write(combined_line + "\n")
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and align career data.')
    parser.add_argument('filename', type=str, help='Path to the file.')
    
    args = parser.parse_args()
    
    input_filename = "./formateo/dades_original/" + args.filename + ".txt"
    output_filename = "./formateo/dades_alineades/" + args.filename + ".txt"

    process_lines(input_filename, output_filename)
