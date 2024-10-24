SOURCES := $(wildcard codi/*/*.cpp codi/*.cpp codi/*/*.cc codi/*.cc)
OBJECTS := $(SOURCES:codi/%.cpp=build/%.o)

CPP_FLAGS := -Wno-unused-result -std=c++17 -O3


all: build/main.exe

run: all
	./build/main.exe

build/main.exe: $(OBJECTS)
	@mkdir -p $(dir $@)
	g++ $(CPP_FLAGS) -o $@ $(OBJECTS)

build/%.o: codi/%.cpp
	@mkdir -p $(dir $@)
	g++ $(CPP_FLAGS) -MMD -o $@ -c $<

clean:
	rm -r ./build/

ultraclean:
	rm -r ./build/ ./dades

-include $(OBJECTS:.o=.d)

