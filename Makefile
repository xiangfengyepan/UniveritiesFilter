SOURCES := $(wildcard codi/*/*.cpp codi/*.cpp codi/*/*.cc codi/*.cc)
OBJECTS := $(SOURCES:codi/%.cpp=build/%.o)

CPP_FLAGS := -Wno-unused-result -std=c++17 -O3

FORMAT = nota places ponderacions

all: build/main.exe

run: all
	./build/main.exe

build/main.exe: $(OBJECTS)
	@mkdir -p $(dir $@)
	g++ $(CPP_FLAGS) -o $@ $(OBJECTS)

build/%.o: codi/%.cpp
	@mkdir -p $(dir $@)
	g++ $(CPP_FLAGS) -MMD -o $@ -c $<


format_line:
	for file in $(FORMAT); do \
		python3 ./formateo/formateo_line.py $$file; \
	done

# Second step: process files using formateo.py
format_main:
	for file in $(FORMAT); do \
		python3 ./formateo/formateo.py $$file; \
	done
	
format: clean_format format_line format_main

clean:
	rm -r ./build/

clean_format:
	rm ./formateo/dades_input/* ./formateo/dades_alineades/* 

-include $(OBJECTS:.o=.d)

