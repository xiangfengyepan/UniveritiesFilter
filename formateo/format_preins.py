import argparse
import os

def process_text(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        context = f.read()
    print(f"Llegint de: {input_filename}")
    
    result_lines = []  

    for line in context.split('\n'):
        line = line.strip()
        
        result_lines.append(line)

    with open(output_filename, "w") as f:
        f.write("Codi,Nom del centre d'estudi,Universitat,Població,Tipus de centre,Places orientatives,Preu orientatiu,Observacions\n")
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

    print(f"Solving issues preinscription: {input_filename} to {output_filename}")
    process_text(input_filename, output_filename)