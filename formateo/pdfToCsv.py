import pandas as pd  
import argparse
import os
from tabula import read_pdf  
import subprocess
import sys
from parent_src.Cli_utils import CliOutput  # Import the pre-implemented CliOutput


# Install required packages
def install_package(package):
    try:
        __import__(package)
        CliOutput.success(f"El paquet {package} ja està instal·lat.")
    except ImportError:
        CliOutput.warning(f"El paquet {package} no està instal·lat. Instal·lant...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def tabula(input_path, output_filename, delimiter=","):
    try:
        if not os.path.exists(input_path):
            CliOutput.error(f"El fitxer {input_path} no existeix.")
            return

        tables = read_pdf(input_path, pages="all", multiple_tables=True, lattice=True)

        if tables:
            combined_df = pd.concat(tables, ignore_index=True)
            combined_df.fillna("N/A", inplace=True)
            combined_df = combined_df.replace({',': ' '}, regex=True)
            combined_df.columns = [str(col).strip() for col in combined_df.columns]
            combined_df.to_csv(output_filename, index=False, sep=delimiter, quotechar='"')
            CliOutput.success(f"Conversió completada (tabula). Fitxer guardat a: {output_filename}")
        else:
            CliOutput.warning("No s'han trobat taules al PDF (tabula).")
    except Exception as e:
        CliOutput.error(f"Error al processar amb tabula: {e}")

def convert_pdf_to_csv(input_path, output_filename):
    # Check if the output file already exists
    if os.path.exists(output_filename):
        CliOutput.info(f"El fitxer {output_filename} ja existeix. Saltant la conversió.")
        return
    
    tabula(input_path, output_filename)

def main():
    parser = argparse.ArgumentParser(description='Convertir taules d\'un PDF a CSV.')
    parser.add_argument('file_path', type=str, help='El camí del fitxer d\'entrada.')
    parser.add_argument('directory_output', type=str, help='Nom de la carpeta per desar els arxius de sortida.')

    args = parser.parse_args()

    input_path = args.file_path
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_filename = os.path.join(args.directory_output, base_filename + ".csv")

    # Check if the output file already exists
    if os.path.exists(output_filename):
        CliOutput.info(f"El fitxer {output_filename} ja existeix. Saltant la conversió.")
        return

    CliOutput.info(f"Convertint {input_path} a {output_filename} utilitzant el mètode: tabula")
    convert_pdf_to_csv(input_path, output_filename)


if __name__ == "__main__":
    install_package('pandas')
    install_package('jpype1')
    main()

