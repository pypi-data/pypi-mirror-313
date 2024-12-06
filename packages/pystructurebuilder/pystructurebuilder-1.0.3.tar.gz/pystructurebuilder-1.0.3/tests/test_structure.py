import unittest
import os
from utils.structure import Structure
from utils.logger import setup_logging

class TestStructure(unittest.TestCase):
    def setUp(self):
        self.root_path = "test_directory"
        self.output_file_path = "test_output.txt"
        self.display_structure = False

        # Configure logging
        self.log_message, self.log_separator = setup_logging()

        # Create a test directory with some files and subdirectories
        self.log_message("Setting up test directory and files.")
        os.makedirs(self.root_path, exist_ok=True)
        with open(os.path.join(self.root_path, "test_file.txt"), 'w') as f:
            f.write("This is a test file.")
        os.makedirs(os.path.join(self.root_path, "subdir"), exist_ok=True)
        with open(os.path.join(self.root_path, "subdir", "sub_test_file.txt"), 'w') as f:
            f.write("This is a test file in a subdirectory.")

    def tearDown(self):
        # Remove the test directory and its contents after the tests
        self.log_message("Tearing down test directory and files.")
        for root, dirs, files in os.walk(self.root_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.root_path)
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)

    def test_generate_structure(self):
        self.log_message("Testing generate_structure method.")
        structure = Structure(self.root_path, self.display_structure)
        structure.generate_structure(self.output_file_path)

        # Check that the output file was created
        self.log_message("Checking if the output file was created.")
        self.assertTrue(os.path.exists(self.output_file_path))

        # Check the content of the output file
        self.log_message("Checking the content of the output file.")
        with open(self.output_file_path, 'r') as f:
            content = f.read()
            self.assertIn("test_file.txt", content)
            self.assertIn("subdir/", content)
            self.assertIn("sub_test_file.txt", content)

    def test_unique_filename(self):
        self.log_message("Testing _get_unique_filename method.")
        structure = Structure(self.root_path, self.display_structure)
        
        # Create the original file to ensure a unique filename is generated
        self.log_message("Creating the original file to ensure a unique filename is generated.")
        with open(self.output_file_path, 'w') as f:
            f.write("This is a test output file.")
        
        unique_filename = structure._get_unique_filename(self.output_file_path)

        # Check that the unique filename is different if the file already exists
        self.log_message("Checking that the unique filename is different if the file already exists.")
        self.assertNotEqual(unique_filename, self.output_file_path)

if __name__ == '__main__':
    unittest.main()
