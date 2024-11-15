import argparse


def move_dades(input_filename, output_filename):
    print("moving " + input_filename + " to " + output_filename)
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        content = infile.read()
        outfile.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Proces de formateo')
    parser.add_argument('filename', type=str, help='Path to the file.')
    
    args = parser.parse_args()
    
    input_filename = "./formateo/dades_input/" + args.filename + ".txt"
    output_filename = "./dades/2024/" + args.filename + ".txt"

    if args.filename == "nota":
        move_dades(input_filename, output_filename)
    if args.filename == "coefficients":
        move_dades(input_filename, output_filename)
    if args.filename == "capacity":
        move_dades(input_filename, output_filename)

