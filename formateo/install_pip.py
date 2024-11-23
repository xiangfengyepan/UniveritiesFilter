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


def main():
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
    
    # Comprovem si els paquets estan instal·lats
    for package in packages:
        install_package(package)

if __name__ == "__main__":
    main()

# pip install jpype1
# pip install tabula-py
# pip install pdfplumber
# pip install pandas
# pip install camelot-py[cv]
# pip install PyMuPDF
# pip install pdfminer.six
