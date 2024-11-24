import argparse
import os
import sys
from parent_src.Cli_utils import CliOutput  # Assuming CliOutput is pre-implemented

def process_text(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as f:
            context = f.read()
        CliOutput.info(f"Llegint de: {input_filename}")
        
        result_lines = []  

        for line in context.split('\n'):
            line = line.strip()
            line = line.replace('€', '')
            result_lines.append(line)

        with open(output_filename, "w") as f:
            f.write("Codi,Nom del centre de estudi,Universitat,Població,Tipus de centre,Places orientatives,Preu orientatiu,Observacions\n")
            f.write("\n".join(result_lines))

        CliOutput.success(f"Resultat escrit a: {output_filename}")
    except FileNotFoundError:
        CliOutput.error(f"No s'ha trobat el fitxer: {input_filename}")
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

    CliOutput.info(f"Solving issues preinscription: {input_filename} to {output_filename}")
    process_text(input_filename, output_filename)

if __name__ == "__main__":
    main()