"""
File: pystructurebuilder.py
Creation Date: 2024-11-28
Last Update: 2024-11-28
Creator: eis-x
Git Repository: https://github.com/eis-x/pystructurebuilder
"""

import os
import argparse
import webbrowser
from utils import Structure, setup_logging, name, version

class PyStructureBuilder:
    def __init__(self, root_path: str, output_file_path: str | None=None, open_file: bool=False, display_structure: bool=False) -> None:
        self.root_path = os.path.abspath(root_path)
        
        if output_file_path is None:
            self.output_file_path:str = os.path.join(self.root_path, os.path.basename(self.root_path) + "_structure.txt")
        else:
            self.output_file_path = os.path.join(self.root_path, os.path.basename(os.path.abspath(output_file_path)))
        self.log_message, self.log_separator = setup_logging()
        self.output_file_path = self._get_unique_filename(self.output_file_path)
        self.open_file = open_file
        self.display_structure = display_structure
        self.log_message(f"Output file determined: {self.output_file_path}")
        with open(self.output_file_path, 'w', encoding='utf-8') as file:
                file.write("")

    def generate_structure(self) -> None:
        structure_generator = Structure(self.root_path, self.display_structure)
        self.log_message(f"Generating structure for the root path: '{os.path.abspath(self.root_path)}'...")
        structure_generator.generate_structure(self.output_file_path)
        self.log_message("Structure generation process completed.")
        self.log_message(f"Project structure of '{os.path.basename(self.root_path)}' has been saved to '{os.path.abspath(self.output_file_path)}'.")
        if self.open_file:
            opening_output_file_message = f"Opening the output file: {os.path.abspath(self.output_file_path)}"
            webbrowser.open(self.output_file_path)
            self.log_message(opening_output_file_message)
        if self.display_structure:
            print(f"\n{structure_generator.structure}")
        self.log_separator(f"\n{'*'*75}\n")

    def _get_unique_filename(self, filename) -> str:
        base, extension = os.path.splitext(filename)
        counter = 1
        unique_filename = filename
        while os.path.exists(unique_filename):
            unique_filename = f"{base}{counter}{extension}"
            counter += 1
        self.log_message(f"Unique filename generated: {unique_filename}")
        return unique_filename

def main():
    parser = argparse.ArgumentParser(description="Generate a project structure from a directory path")
    parser.add_argument('-r', '--root-path', type=str, required=True, help='Path to the root directory')
    parser.add_argument('-o', '--output-file-path', type=str, help='Path to the output file path (default: root-path.txt)')
    parser.add_argument('--version', action='version', version=f'{name.title()} {version}', help="Show program's version number and exit")
    parser.add_argument('--no-open', dest='open_file', action='store_false', help='Do not open the output file in the default program')
    parser.add_argument('-d', '--display-structure', action='store_true', help='Display the generated structure in the terminal')

    args = parser.parse_args()

    try:
        generator = PyStructureBuilder(args.root_path, args.output_file_path, args.open_file, args.display_structure)
        generator.generate_structure()
    except Exception as e:
        log_message, _ = setup_logging()
        log_message(f"An error occurred in the main function: {str(e)}")
