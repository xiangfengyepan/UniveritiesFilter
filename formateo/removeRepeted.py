import argparse
import re

debug = False  # Set to True to enable debug prints, False to disable them

def process_lines(file_path):
    seen_codes = {}
    lines_to_keep = []
    print("Processing duplicates: " + file_path)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        if len(line) >= 5 and line[:5].isdigit():
            code = line[:5]
            if code in seen_codes:
                if str(seen_codes[code]) == str(line.strip()):
                    if debug: print(f"Auto removing identical duplicate: {line.strip()}")
                    continue
                
                if check_if_branches_are_the_same(seen_codes[code], line.strip()):
                    combined_line = combine_branches(seen_codes[code], line.strip())
                    if debug: print(f"Auto combining lines: {combined_line}")
                    seen_codes[code] = combined_line
                    continue
                
                while True:
                    print(f"Duplicate found for code {code}:")
                    print(f"1. {seen_codes[code]}")
                    print(f"2. {line.strip()}")
                    
                    user_input = input("Which line do you want to keep? (1/2), or combine (3): ").strip()

                    if user_input == "admin":
                        admin_line = input("Admin enter line: ").strip()
                        print(f"Admin entered line: \n{admin_line}")
                        confirm = input("Is this correct? (Yes/no): ").strip().lower()
                        
                        if confirm in ["yes", ""]:
                            print(f"Replacing both lines with: {admin_line}")
                            seen_codes[code] = admin_line
                            break
                        elif confirm in ["no"]:
                            print("Returning to selection.")
                            continue
                        
                    elif user_input == "2":
                        print(f"Line removed: 1. {seen_codes[code]}")
                        seen_codes[code] = line.strip()
                        break
                    elif user_input == "1":
                        print(f"Line removed: 2. {line.strip()}")
                        break
                        
                    elif user_input == "3":
                        print(f"Combined lines: ")
                        print("Different numbers, picking the highest.")
                        combined_line = combine_branches(seen_codes[code], line.strip())
                        print(combined_line)
                        confirm = input("Is this correct? (Yes/no): ").strip().lower()
                        if confirm in ["yes", ""]:
                            seen_codes[code] = combined_line
                            break
                        elif confirm in ["no"]:
                            print("Returning to selection.")
                            continue
                    
                    print("Command wrong: try again")
            else:
                seen_codes[code] = line.strip()
        lines_to_keep.append(line)

    # Filter lines based on seen_codes to ensure only final versions remain
    final_lines = [line for line in lines_to_keep if line.strip()[:5] not in seen_codes or seen_codes[line.strip()[:5]] == line.strip()]

    with open(file_path, 'w') as file:
        file.writelines(final_lines)

    print("Processing complete. Duplicates handled as per user input.")

def combine_branches(line1, line2):
    allowed_branches = ["AH", "C", "CS", "CSJ", "EA"]
    
    parts1 = line1.split()
    parts2 = line2.split()
    
    code = parts1[0]
    
    branch1 = parts1[1]
    branch2 = parts2[1]
    
    combined_branches = sorted(set([branch1, branch2]))
    
    numbers1 = list(map(int, parts1[2:]))
    numbers2 = list(map(int, parts2[2:]))
    
    combined_numbers = [str(max(n1, n2)) for n1, n2 in zip(numbers1, numbers2)]

    return f"{code} {' '.join(combined_branches)} {' '.join(combined_numbers)}"

def check_if_branches_are_the_same(line1, line2):
    """Check if the numerical data after the branch name is the same in both lines."""
    parts1 = re.split(r'\s+', line1.strip())
    parts2 = re.split(r'\s+', line2.strip())
    
    branch1 = parts1[1]
    branch2 = parts2[1]
    
    numerical_data1 = " ".join(parts1[2:])
    numerical_data2 = " ".join(parts2[2:])
    
    if numerical_data1 == numerical_data2:
        if debug: print(f"Branches {branch1} and {branch2} have the same numerical data.")
        return True
    else:
        if debug: print(f"Branches {branch1} and {branch2} have different numerical data.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and format lines in a file.')
    parser.add_argument('filename', type=str, help='Name of the input file (without extension).')
    
    args = parser.parse_args()
    
    input_filename = "./formateo/dades_input/" + args.filename + ".txt"
    process_lines(input_filename)
