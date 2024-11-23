SOURCES := $(wildcard codi/*/*.cpp codi/*.cpp codi/*/*.cc codi/*.cc)
OBJECTS := $(SOURCES:codi/%.cpp=build/%.o)

CPP_FLAGS := -Wno-unused-result -std=c++17 -O3

POND_FILE_PATH = Ponderacions-2024_v7
NOTES_FILE_PATH = Notes-tall-1a-assignacio_juny_2024
PREINS_FILE_PATH = Preins-2024-Juny
ALL_FILE = $(NOTES_FILE_PATH) $(POND_FILE_PATH) $(PREINSCRIPTION_FILE_PATH)

DIR_PDF = ./formateo/dades_pdf
DIR_CSV = ./formateo/dades_csv
DIR_FORMATED = ./formateo/dades_formated
DIR_INPUT = ./dades/2024

run:
	python3 ./parent_src/filter.py

format_pdf_to_csv:
	for file in $(DIR_PDF)/*; do \
		python3 ./formateo/pdfToCsv.py "$$file" $(DIR_CSV); \
	done

# Second step: process files using formateo.py
format_aline:
	for file in $(DIR_CSV)/*; do \
		python3 ./formateo/format_aline.py "$$file" $(DIR_FORMATED); \
	done

format_pond:
	python3 ./formateo/format_pond.py $(DIR_FORMATED)/$(POND_FILE_PATH)*.csv $(DIR_FORMATED); \

format_notes:
	python3 ./formateo/format_notes.py $(DIR_FORMATED)/$(NOTES_FILE_PATH)*.csv $(DIR_FORMATED); \

format_preins:
	python3 ./formateo/format_preins.py $(DIR_FORMATED)/$(PREINS_FILE_PATH)*.csv $(DIR_FORMATED); \

format_join:
	python3 ./formateo/format_join.py ./formateo/dades_formated ./result.csv \
  	--merge_columns Codi \
  	--columns Codi,"Nom del centre destudi",Població,Universitat,"Tipus de centre","Places orientatives","Preu orientatiu",Observacions,\
	"PAU / CFGS","Més grans de 25 anys","Titulats universitaris","Més grans de 45 anys",\
	Branca,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27


copy_dades:
	for file in $(DIR_FORMATED)/*; do \
		cp "$$file" $(DIR_INPUT);\
	done

# install_all_packages:
# 	python3 ./formateo/install_pip.py; \

format_all: format_pdf_to_csv format_aline format_notes format_pond  format_preins copy_dades
format: format_aline format_notes format_pond format_preins copy_dades


clean:
	rm -r ./build/

clean_format:
	rm ./formateo/dades_csv/* ./formateo/dades_formated/*

-include $(OBJECTS:.o=.d)

