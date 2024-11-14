import re
from unidecode import unidecode
import string
import argparse


def is_first_and_last_uppercase(word):
    return word[0].isupper() and word[-1].isupper() if word else False

def is_number_with_comma(word):
    word = word.strip()
    if ',' in word:
        return all(c.isdigit() or c == ',' for c in word)
    return False


def is_word_with_parentheses(word):
    pattern1 = r'^\([A-Z].*\)$'
    pattern2 = r'^\(el_[A-Z].*\)$'
    
    return re.match(pattern1, word) or re.match(pattern2, word)

def format_word(word):
    word = word.strip()
    word = unidecode(word)
    word = re.sub(r'\s*/\s*', '/', word)
    word = word.replace(' ', '_')
    return word

def replace_spaces_in_parentheses(text):
    # Use re.sub to find the content inside parentheses and replace spaces with underscores
    return re.sub(r'\((.*?)\)', lambda match: f"({match.group(1).replace(' ', '_')})", text)

def format_career_data(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    final_lines = []
    for line in lines:
        line = replace_spaces_in_parentheses(line)
        atrr = line.split(" ")
  
        code = atrr[0]
        university = []
        city = ""
        degree = ""
        score = ""
        for word in atrr[1:len(atrr)]:
            if is_word_with_parentheses(word):
                city = word
                
            if city == "":
                degree += word + str(' ')
                
            if score == "" and is_number_with_comma(word):
                score = word 
            if is_first_and_last_uppercase(word):
                university.append(word)
         
       
        degree = format_word(degree)
        university = "/".join(university)
        city = city.strip('()')
        score = score.replace(',', '.')

        final_line = f"{code} {degree} {university} {city} {score}"
        final_lines.append(final_line)

    with open(output_filename, 'w') as outfile:
        for line in final_lines:
            outfile.write(line + '\n')

def format_places_data(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            parts = line.strip().split()
            codi = parts[0]

            # Find 'tipus'
            tipus_match = next((t for t in ["U. Públ. CA", "U. Públ.", "U. Priv."] if t in line), "")
            tipus = unidecode(tipus_match.replace(" ", ""))

            # Extract places after 'tipus'
            after_tipus = line.split(tipus_match, 1)[-1].strip() if tipus_match else line.strip()
            places_match = re.search(r'\b\d+\b', after_tipus)
            places = places_match.group() if places_match else "0"

            # Extract a single valid price if present
            preu_match = re.search(r'\d+\.\d{3} €|\d+,\d{2} €', line)
            preu = preu_match.group().replace(" ", "") if preu_match else "0,00€"

            # Determine 'observacio' position
            if preu_match:
                observacio_start = line.split(preu_match.group(), 1)[-1].strip()
            elif places_match:
                observacio_start = after_tipus.split(places, 1)[-1].strip()
            else:
                observacio_start = ""

            # Format observacio
            observacio = observacio_start.replace(" ", "")

            # Ensure 0,00€ is not written if a valid price exists
            if preu != "0,00€":
                outfile.write(f"{codi} {tipus} {places} {preu} {observacio}\n")
            else:
                outfile.write(f"{codi} {tipus} {places} 0,00€ {observacio}\n")


def format_pont_data(input_filename, output_filename):
    valid_br_values = {"AH", "C", "CS", "CSJ", "EA"}

    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            parts = line.strip().split("\t")
            
            code = parts[0]
            br = parts[3]
            
            if br in valid_br_values:
                points = [
                    "2" if "2" in col else "1" if "1" in col else "0" 
                    for col in parts[4:]
                ]

                formatted_line = f"{code} {br}\t" + " ".join(points)
                outfile.write(formatted_line + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Proces de formateo')
    parser.add_argument('filename', type=str, help='Path to the file.')
    
    args = parser.parse_args()
    
    input_filename = "./formateo/dades_alineades/" + args.filename + ".txt"
    output_filename = "./formateo/dades_input/" + args.filename + ".txt"

    if args.filename == "nota":
        format_career_data(input_filename, output_filename)
    if args.filename == "ponderacions":
        format_pont_data(input_filename, output_filename)
    if args.filename == "places":
        format_places_data(input_filename, output_filename)

