SOURCES := $(wildcard codi/*/*.cpp codi/*.cpp codi/*/*.cc codi/*.cc)
OBJECTS := $(SOURCES:codi/%.cpp=build/%.o)

CPP_FLAGS := -Wno-unused-result -std=c++17 -O3

POND_FILE_PATH = Ponderacions-2024_v7
NOTES_FILE_PATH = Notes-tall-1a-assignacio_juny_2024
PREINS_FILE_PATH = Preins-2024-Juny
ALL_FILE = $(NOTES_FILE_PATH) $(POND_FILE_PATH) $(PREINS_FILE_PATH)

DIR_PDF = ./formateo/dades_pdf
DIR_CSV = ./formateo/dades_csv
DIR_FORMATED = ./formateo/dades_formated
DIR_INPUT = ./dades/2024

build:
	pip install -e .
	python3 setup.py sdist bdist_wheel

init: install_wsl install_all_packages build

mkdir:
	@echo "Creating necessary directories..."
	mkdir -p ./formateo/dades_csv 
	mkdir -p ./formateo/dades_result/
	mkdir -p ./formateo/dades_result/2024 
	mkdir -p ./formateo/dades_formated

install_wsl:
	@echo "Checking and installing WSL..."
	# Check if WSL is installed
	if ! command -v wsl > /dev/null 2>&1; then \
		echo "WSL is not installed. Installing WSL..."; \
		sudo apt update && sudo apt install -y wsl; \
	fi

	# Install WSL (if not installed) and Ubuntu 22.04 LTS
	if ! wsl -l | grep -q "Ubuntu-22.04"; then \
		echo "Ubuntu 22.04 LTS not found. Installing Ubuntu..."; \
		wsl --install -d Ubuntu-22.04; \
	fi

	# Ensure Ubuntu 22.04 is the default WSL distro
	wsl --set-default Ubuntu-22.04

	# Ensure using WSL 2
	wsl --set-version Ubuntu-22.04 2

install_all_packages:
	@echo "Installing required packages..."
	sudo apt update
	sudo apt upgrade -y
	sudo apt install -y python3
	sudo apt install -y python3-pip
	sudo apt install -y openjdk-11-jdk
	sudo apt install -y curl
	sudo apt install -y gnupg
	sudo apt install -y lsb-release
	sudo apt install -y software-properties-common
	sudo apt install -y wget
	sudo apt install -y default-jre

	# Install Python libraries
	sudo pip install pandas
	sudo pip install tabula-py

run: build
	@echo "Running the main Python script..."
	clear
	python3 parent_src/filter.py

format_pdf_to_csv:
	@echo "Converting PDF files in $(DIR_PDF) to CSV format in $(DIR_CSV)..."
	for file in $(DIR_PDF)/*; do \
		echo "Processing $$file..."; \
		python3 ./formateo/pdfToCsv.py "$$file" $(DIR_CSV); \
	done

format_aline:
	@echo "Formatting CSV files in $(DIR_CSV) and saving to $(DIR_FORMATED)..."
	for file in $(DIR_CSV)/*; do \
		echo "Processing $$file..."; \
		python3 ./formateo/format_aline.py "$$file" $(DIR_FORMATED); \
	done

format_pond:
	@echo "Formatting Ponderacions files..."
	python3 ./formateo/format_pond.py $(DIR_FORMATED)/$(POND_FILE_PATH)*.csv $(DIR_FORMATED);

format_notes:
	@echo "Formatting Notes files..."
	python3 ./formateo/format_notes.py $(DIR_FORMATED)/$(NOTES_FILE_PATH)*.csv $(DIR_FORMATED);

format_preins:
	@echo "Formatting Preinscripcions files..."
	python3 ./formateo/format_preins.py $(DIR_FORMATED)/$(PREINS_FILE_PATH)*.csv $(DIR_FORMATED);

format_join:
	@echo "Joining formatted files into a single CSV..."
	python3 ./formateo/format_join.py ./formateo/dades_formated ./formateo/dades_result/2024/result.csv \
	--merge_columns Codi \
	--columns Codi,"Nom del centre de estudi",Població,Universitat,"Tipus de centre","Places orientatives","Preu orientatiu",Observacions,\
	"PAU / CFGS","Més grans de 25 anys","Titulats universitaris","Més grans de 45 anys",\
	Branca,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27

format: mkdir format_pdf_to_csv format_aline format_notes format_pond format_preins format_join
	@echo "All formatting steps completed."

clean:
	@echo "Cleaning build directory..."
	rm -rf ./build/ ./dist/ ./UniversitiesFilter.egg-info/

clean_format:
	@echo "Cleaning formatted data directories..."
	rm -rf ./formateo/dades_csv/ ./formateo/dades_formated/ ./formateo/dades_result/

clean_cache:
	@echo "Clearing Python cache files and directories..."
	find $(DIR) -type f -name "*.pyc" -delete -print
	find $(DIR) -type f -name "*.pyo" -delete -print
	find $(DIR) -type d -name "__pycache__" -exec rm -rf {} + -print
	@echo "Python cache cleared."

ultraclean: clean clean_cache clean_format

help:
	@echo "Available commands:"
	@echo "  run                - Run the main Python script."
	@echo "  format_pdf_to_csv  - Convert PDF files to CSV format."
	@echo "  format_aline       - Format CSV files (alignment)."
	@echo "  format_pond        - Format Ponderacions files."
	@echo "  format_notes       - Format Notes files."
	@echo "  format_preins      - Format Preinscripcions files."
	@echo "  format_join        - Join formatted files into a single CSV."
	@echo "  format_all         - Perform all formatting steps."
	@echo "  clean              - Clean the build directory."
	@echo "  clean_format       - Clean formatted data directories."
	@echo "  clean-cache        - Remove Python cache files and directories."
	@echo "  help               - Show this help message."

-include $(OBJECTS:.o=.d)
