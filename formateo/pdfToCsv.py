import pandas as pd  
import argparse
import os
import pdfplumber  
from tabula import read_pdf  
import camelot  
import fitz  # PyMuPDF 
from pdfminer.high_level import extract_text  
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


# PDF conversion functions
def plumber(input_path, output_filename):
    install_package('pdfplumber')
    try:
        with pdfplumber.open(input_path) as pdf:
            data_frames = []
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    data_frames.append(df)

            if data_frames:
                result = pd.concat(data_frames, ignore_index=True)
                result.to_csv(output_filename, index=False)
                CliOutput.success(f"Conversió completada (pdfplumber). Fitxer guardat a: {output_filename}")
            else:
                CliOutput.warning("No s'han trobat taules al PDF (pdfplumber).")
    except Exception as e:
        CliOutput.error(f"Error al processar amb pdfplumber: {e}")


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


def camelot_converter(input_path, output_filename):
    install_package('camelot-py[cv]')
    try:
        tables = camelot.read_pdf(input_path, pages='all', flavor='stream')

        if tables:
            tables.export(output_filename, f='csv', compress=False)
            CliOutput.success(f"Conversió completada (Camelot). Fitxer guardat a: {output_filename}")
        else:
            CliOutput.warning("No s'han trobat taules al PDF (Camelot).")
    except Exception as e:
        CliOutput.error(f"Error al processar amb Camelot: {e}")


def pymupdf_converter(input_path, output_filename):
    install_package('PyMuPDF')
    try:
        doc = fitz.open(input_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")

        with open(output_filename, 'w') as output_file:
            output_file.write(text)

        CliOutput.success(f"Conversió completada (PyMuPDF). Fitxer guardat a: {output_filename}")
    except Exception as e:
        CliOutput.error(f"Error al processar amb PyMuPDF: {e}")


def pdfminer_converter(input_path, output_filename):
    install_package('pdfminer.six')
    try:
        text = extract_text(input_path)
        with open(output_filename, 'w') as output_file:
            output_file.write(text)

        CliOutput.success(f"Conversió completada (PDFMiner). Fitxer guardat a: {output_filename}")
    except Exception as e:
        CliOutput.error(f"Error al processar amb PDFMiner: {e}")


def convert_pdf_to_csv(input_path, output_filename, method='both'):
    # Check if the output file already exists
    if os.path.exists(output_filename):
        CliOutput.info(f"El fitxer {output_filename} ja existeix. Saltant la conversió.")
        return

    if method == 'tabula':
        tabula(input_path, output_filename)
    elif method == 'pymupdf':
        pymupdf_converter(input_path, output_filename)
    elif method == 'pdfminer':
        pdfminer_converter(input_path, output_filename)
    elif method == 'plumber':
        plumber(input_path, output_filename)
    elif method == 'camelot':
        camelot_converter(input_path, output_filename)
    else:
        CliOutput.error(f"Mètode desconegut: {method}")

def main():
    parser = argparse.ArgumentParser(description='Convertir taules d\'un PDF a CSV.')
    parser.add_argument('file_path', type=str, help='El camí del fitxer d\'entrada.')
    parser.add_argument('directory_output', type=str, help='Nom de la carpeta per desar els arxius de sortida.')
    parser.add_argument('--method', type=str, choices=['plumber', 'tabula', 'camelot', 'pymupdf', 'pdfminer'], default='tabula',
                        help='Mètode per extreure les taules: "plumber", "tabula", "camelot", "pymupdf", "pdfminer" (per defecte tabula).')

    args = parser.parse_args()

    input_path = args.file_path
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_filename = os.path.join(args.directory_output, base_filename + ".csv")

    # Check if the output file already exists
    if os.path.exists(output_filename):
        CliOutput.info(f"El fitxer {output_filename} ja existeix. Saltant la conversió.")
        return

    CliOutput.info(f"Convertint {input_path} a {output_filename} utilitzant el mètode: {args.method}")
    convert_pdf_to_csv(input_path, output_filename, method=args.method)


if __name__ == "__main__":
    install_package('pandas')
    install_package('jpype1')
    main()

