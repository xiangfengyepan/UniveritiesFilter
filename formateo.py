import re
from unidecode import unidecode
import string

# Example usage:
input_filename = 'input.txt'
output_filename = 'output.txt'

def process_lines(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        i = 0
        combined_line = ""
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if the line starts with a 5-digit number (career code)
            if re.match(r'^\d{5}', line):
                # If there is a combined line, write it to the output
                if combined_line:
                    outfile.write(combined_line + "\n")
                
                # Start a new line with the current 5-digit code
                combined_line = line
                
            else:
                # If the line doesn't start with a 5-digit number, merge it into the current line
                combined_line += " " + line.strip()
            
            i += 1
        
        # Write the last combined line (if any)
        if combined_line:
            outfile.write(combined_line + "\n")

process_lines(input_filename, "aux_text.txt")

def is_first_and_last_uppercase(word):
    return word[0].isupper() and word[-1].isupper() if word else False

def is_number_with_comma(word):
    word = word.strip()
    if ',' in word:
        return all(c.isdigit() or c == ',' for c in word)
    return False

def format_word(word):
    # print(f"Original word: {word} ({type(word)})")
    word = word.strip()
    word = re.sub(r'\s*/\s*', '/', str(word))
    word = word.replace(' ', '_')
    return word

def format_career_data(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    final_lines = []
    for line in lines:
        atrr = line.split(" ")

        code = atrr[0]
        university = []
        degree = ""
        score = ""
        for word in atrr[1:len(atrr)]:
            if is_first_and_last_uppercase(word):
                university.append(word)
            elif len(university) == 0:
                degree += word + str(' ')
            elif score == "" and is_number_with_comma(word):
                score = word 
        degree = format_word(degree)
        university = " /".join(university)
        score = score.replace(',', '.')

        final_line = f"{code} {degree} {university} {score}"
        final_lines.append(final_line)

    with open(output_filename, 'w') as outfile:
        for line in final_lines:
            outfile.write(line + '\n')

format_career_data("aux_text.txt", output_filename)

