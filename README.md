
# Welcome to **UniversitiesFilter**!

This guide will help you set up and run the program.

---

## **1. Set Up Your Development Environment**

Follow these steps to set up the environment:

### **Install Visual Studio Code (VSCode)**
1. Download and install [VSCode](https://code.visualstudio.com).
2. Open VSCode and use the following shortcuts:
   - `Ctrl + K + O` to open a folder.
   - `Ctrl + Ñ` to open the terminal.

### **Install Windows Subsystem for Linux (WSL)**
1. Open the VSCode terminal and run the following commands to install WSL:
   ```bash
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\install_wsl_setup.sh
   ```
   - This will ask you to create a username and password for WSL.

### **Install Python and Required Pip Packages**
1. In the VSCode terminal, run the following command to install necessary packages, only have to do it once:
   ```bash
   make init
   ```

### **Create CSV Files**
1. To create the necessary CSV files, run the following command. This step is only required if there are no PDF files added:
   ```bash
   make format
   ```

### **Run the Program**
1. Once everything is set up, you can run the program with the following command:
   ```bash
   make run
   ```

---

## **Available Commands**
- To see all available commands, run:
  ```bash
  make help
  ```

---

## **Usage**

1. **Code in Python**: You will write your Python code in the `./child_src` directory.
   
2. **Create Python Files**: You can create new `.py` files and define functions. Refer to the `example.py` file for implementation examples.

3. **Use `DataFrameProcessor.py`**: In the `./child_src` folder, the `DataFrameProcessor.py` file contains a class that can assist you in implementing your functions.

4. **Ignore the `__init__.py` file**: This file is for internal use and should not be modified.

---

## **Rules**
- **Do not modify any files outside of the `./child_src` directory** unless you are familiar with the system.
- **Have fun!** 😄

---

## **Annex: PDF Resources**

The program uses the following websites to access PDF data:

1. [Ponderations (Ponderacions)](https://universitats.gencat.cat/ca/preinscripcions/sobre-preinscripcio/ponderacions/)
2. [Cut-off Scores (Notes de tall)](https://universitats.gencat.cat/ca/preinscripcions/sobre-preinscripcio/notes-tall/#notes-de-tall--preinscripcio-2024)
3. [University Places (Places universitaries)](https://universitats.gencat.cat/ca/preinscripcions/sobre-preinscripcio/places-universitaries/)

---

Enjoy coding and building your project! 😊
