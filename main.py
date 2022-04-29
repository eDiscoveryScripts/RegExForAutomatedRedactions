
import re

inputfile ="searchterms.txt"
outputfile = "regex_searchterms.txt"

#add word boundary
wordboundary = True

#function that replaces letters with other letters to cover for OCR issues for certain letters
def replacewithRegex(searchterm):
    replaces = {"l": "[l|1|I]",
                "O": "[O|0|Q]",
                "0": "[O|0|Q]",
                "Q": "[O|0|Q]",
                "8": "[8|B]",
                "B": "[8|B]",
                "w": "[w|vv]",
                "v": "[v|u|y]",
                "y": "[v|u|y]",
                "u": "[u|v]",
                "5": "[5|S]",
                "S": "[5|S]",
                "A": "[4|A]",
                "t": "[t|f|i]",
                "f": "[t|f]",
                "e": "[e|c]",
                "c": "[e|c]",
                "h": "[h|b|li]",
                "b": "[b|h]",
                "i": "[i|1|l]",
                "I": "[I|l|1]",
                "G": "[G|6]",
                "6": "[G|6|o]",
                "1": "[1|I|l]"
                }
    updated_searchterm = re.sub("|".join(replaces.keys()), lambda match: replaces[match.string[match.start():match.end()]], searchterm)
    if wordboundary:
        updated_searchterm = "\\b"+updated_searchterm+"\\b"
    return updated_searchterm


if __name__ == '__main__':
    with open(inputfile, "r") as input_file:
        with open(outputfile,"w") as output_file:
            for line in input_file:
                stripped_line = line.strip()
                regex_searchterm=replacewithRegex(stripped_line)
                output_file.write(regex_searchterm+"\r\n")



