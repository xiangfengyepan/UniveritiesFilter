import pandas as pd # type: ignore
import argparse
import os
import pdfplumber # type: ignore
from tabula import read_pdf # type: ignore
import camelot # type: ignore
import fitz  # PyMuPDF # type: ignore
import pdfminer # type: ignore
from pdfminer.high_level import extract_text # type: ignore
import subprocess
import sys

# Llista dels paquets que necessitem instal·lar
packages = [
    'jpype1',
    'tabula-py',
    'pdfplumber',
    'pandas',
    'camelot-py[cv]',
    'PyMuPDF',
    'pdfminer.six'
]

def install_package(package):
    """Funció per comprovar si un paquet està instal·lat i instal·lar-lo si no ho està."""
    try:
        __import__(package)
        print(f"El paquet {package} ja està instal·lat.")
    except ImportError:
        print(f"El paquet {package} no està instal·lat. Instal·lant...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def plumber(input_path, output_filename):
    """Funció per extraure taules usant pdfplumber"""
    install_package('pdfplumber')
    try:
        with pdfplumber.open(input_path) as pdf:
            data_frames = []
            # Iterem per cada pàgina del PDF
            for page in pdf.pages:
                # Extreiem taules de la pàgina
                tables = page.extract_tables()
                for table in tables:
                    # Convertim la taula a DataFrame de pandas
                    df = pd.DataFrame(table[1:], columns=table[0])
                    data_frames.append(df)
            
            # Combina totes les taules extretes
            if data_frames:
                result = pd.concat(data_frames, ignore_index=True)
                # Guardem el DataFrame al fitxer CSV
                result.to_csv(output_filename, index=False)
                print(f"Conversió completada (pdfplumber). Fitxer guardat a: {output_filename}")
            else:
                print("No s'han trobat taules al PDF (pdfplumber).")
    except Exception as e:
        print(f"Error al processar amb pdfplumber: {e}")

def tabula(input_path, output_filename, delimiter=","):
    """
    Procesa un PDF con tablas y exporta a un CSV, manejando celdas vacías, comas y encabezados incorrectos.

    :param input_path: Ruta del archivo PDF.
    :param output_filename: Ruta del archivo CSV de salida.
    :param delimiter: Delimitador para el archivo CSV.
    """
    try:
        # Verifica si el archivo PDF existe
        if not os.path.exists(input_path):
            print(f"El archivo {input_path} no existe.")
            return
        
        # Extrae tablas del PDF
        tables = read_pdf(input_path, pages="all", multiple_tables=True, lattice=True)
        
        if tables:
            # Combina todas las tablas extraídas en un único DataFrame
            combined_df = pd.concat(tables, ignore_index=True)

            # Rellenar celdas vacías con un marcador o una cadena vacía
            combined_df.fillna("N/A", inplace=True)
            combined_df = combined_df.replace({',': ' '}, regex=True)
            
            # Solución para columnas desalineadas (si aplica)
            if len(combined_df.columns) > 0:
                combined_df.columns = [str(col).strip() for col in combined_df.columns]

            # Guarda las tablas en un archivo CSV, manejando comas con comillas dobles
            combined_df.to_csv(output_filename, index=False, sep=delimiter, quotechar='#')
            print(f"Conversión completada. Archivo CSV guardado en: {output_filename}")
        else:
            print("No se encontraron tablas en el PDF.")
    except Exception as e:
        print(f"Error procesando el PDF: {e}")


def camelot_converter(input_path, output_filename):
    """Funció per extreure taules usant Camelot"""
    install_package('camelot-py[cv]')

    try:
        # Llegeix el PDF i extreu les taules
        tables = camelot.read_pdf(input_path, pages='all', flavor='stream')  # 'lattice' també és una opció per taules amb línies

        # Exporta les taules a CSV
        if tables:
            tables.export(output_filename, f='csv', compress=False)
            print(f"Conversió completada (Camelot). Fitxer guardat a: {output_filename}")
        else:
            print("No s'han trobat taules al PDF (Camelot).")
    except Exception as e:
        print(f"Error al processar amb Camelot: {e}")

def pymupdf_converter(input_path, output_filename):
    """Funció per extreure taules usant PyMuPDF (fitz)"""
    install_package('PyMuPDF')

    try:
        # Obre el PDF
        doc = fitz.open(input_path)
        text = ""
        
        # Itera per cada pàgina del PDF
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")  # Extracció de text

        # Processa el text (potser parsejats les taules manualment)
        with open(output_filename, 'w') as output_file:
            output_file.write(text)

        print(f"Conversió completada (PyMuPDF). Fitxer guardat a: {output_filename}")
    except Exception as e:
        print(f"Error al processar amb PyMuPDF: {e}")

def pdfminer_converter(input_path, output_filename):
    """Funció per extreure text usant PDFMiner"""
    install_package('pdfminer.six')

    try:
        # Extracte text complet del PDF
        text = extract_text(input_path)

        # Guardar el text extraït a un fitxer CSV (com a text pur)
        with open(output_filename, 'w') as output_file:
            output_file.write(text)

        print(f"Conversió completada (PDFMiner). Fitxer guardat a: {output_filename}")
    except Exception as e:
        print(f"Error al processar amb PDFMiner: {e}")

def convert_pdf_to_csv(input_path, output_filename, method='both'):
    """Funció per seleccionar i executar la conversió de PDF a CSV amb el mètode desitjat"""
    # comas
    if method == 'tabula':
        tabula(input_path, output_filename)
        
    # tabuladors
    if method == 'pymupdf':
        pymupdf_converter(input_path, output_filename)

    # elimina notes
    if method == 'pdfminer':
        pdfminer_converter(input_path, output_filename)

    # no funciona
    if method == 'plumber':
        plumber(input_path, output_filename)
    # no funciona
    if method == 'camelot':
        camelot_converter(input_path, output_filename)

def main():
    parser = argparse.ArgumentParser(description='Convertir taules d\'un PDF a CSV.')
    parser.add_argument('file_path', type=str, help='El camí del fitxer d\'entrada.')
    parser.add_argument('directory_output', type=str, help='Nom de la carpeta per desar els arxius de sortida.')
    parser.add_argument('--method', type=str, choices=['plumber', 'tabula', 'camelot', 'pymupdf', 'pdfminer'], default='tabula',
                        help='Mètode per extreure les taules: "plumber", "tabula", "camelot", "pymupdf", "pdfminer" (per defecte tabula).')

    args = parser.parse_args()

    input_path = args.file_path
    base_filename = os.path.splitext(os.path.basename(input_path))[0]  # Corrected here to use input_path
    output_filename = os.path.join(args.directory_output, base_filename + ".csv")

    print(f"Convertint {input_path} a {output_filename} utilitzant el mètode: {args.method}")
    convert_pdf_to_csv(input_path, output_filename, method=args.method)

if __name__ == "__main__":
    install_package('pandas')
    install_package('jpype1')
    main()
