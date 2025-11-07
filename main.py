#!/usr/bin/env python3
"""
RegEx For Automated Redactions
Converts search terms into regex patterns to handle OCR issues for automated redaction.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict

# Configuration
INPUT_FILE = "searchterms.txt"
OUTPUT_FILE = "regex_searchterms.txt"
WORD_BOUNDARY = True

# OCR character replacement mappings
# Maps characters that are commonly confused by OCR to regex character classes
OCR_REPLACEMENTS: Dict[str, str] = {
    "l": "[l|1|I]",
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

# Pre-compile the regex pattern for better performance
# Escape keys to handle any special regex characters, then join with |
_PATTERN = re.compile("|".join(re.escape(key) for key in OCR_REPLACEMENTS.keys()))


def replace_with_regex(searchterm: str, add_word_boundary: bool = WORD_BOUNDARY) -> str:
    """
    Replaces characters in the search term with regex patterns to handle OCR issues.

    Args:
        searchterm: The original search term to convert
        add_word_boundary: Whether to add word boundaries (\\b) around the pattern

    Returns:
        A regex pattern string with OCR-tolerant character replacements
    """
    # Use the pre-compiled pattern for better performance
    updated_searchterm = _PATTERN.sub(lambda match: OCR_REPLACEMENTS[match.group(0)], searchterm)

    if add_word_boundary:
        updated_searchterm = f"\\b{updated_searchterm}\\b"

    return updated_searchterm


def process_file(input_path: Path, output_path: Path, add_word_boundary: bool = WORD_BOUNDARY) -> int:
    """
    Process the input file and generate regex patterns for each search term.

    Args:
        input_path: Path to the input file containing search terms
        output_path: Path to the output file for regex patterns
        add_word_boundary: Whether to add word boundaries around patterns

    Returns:
        Number of search terms processed

    Raises:
        FileNotFoundError: If input file doesn't exist
        IOError: If there are issues reading/writing files
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    processed_count = 0

    try:
        with input_path.open("r", encoding="utf-8") as input_file, \
             output_path.open("w", encoding="utf-8") as output_file:

            for line in input_file:
                stripped_line = line.strip()

                # Skip empty lines
                if not stripped_line:
                    continue

                regex_searchterm = replace_with_regex(stripped_line, add_word_boundary)
                output_file.write(regex_searchterm + "\n")
                processed_count += 1

        return processed_count

    except IOError as e:
        raise IOError(f"Error processing files: {e}") from e


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Convert search terms to OCR-tolerant regex patterns for automated redaction."
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        default=INPUT_FILE,
        help=f"Input file containing search terms (default: {INPUT_FILE})"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=OUTPUT_FILE,
        help=f"Output file for regex patterns (default: {OUTPUT_FILE})"
    )
    parser.add_argument(
        "--no-word-boundary",
        action="store_true",
        help="Don't add word boundaries (\\b) around patterns"
    )

    args = parser.parse_args()

    try:
        count = process_file(
            args.input,
            args.output,
            add_word_boundary=not args.no_word_boundary
        )
        print(f"Successfully processed {count} search term(s)")
        print(f"Output written to: {args.output}")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())



