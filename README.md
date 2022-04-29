# RegExForBlackout
A short script which creates a regex for a list of search terms used for automated redaction, to take care of OCR related issues for Milyli Blackout within Relativity and RelativityOne Redact. 

You can easily add new replacements for additional charaters, just add a new rule "source chracter": "replacements": 

 replaces = {   "l": "[l|1|I]",
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
