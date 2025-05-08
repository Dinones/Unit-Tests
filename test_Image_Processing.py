###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
import json
import unittest
import PyQt5.QtGui as pyqt_g
from PyQt5.QtWidgets import QApplication
from parameterized import parameterized_class

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Modules.Image_Processing import Image_Processing
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Define absolute paths to required resources
IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Media/Images'))
TESTS_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tests Data/Image_Processing_Data.json'))

# Load test case definitions from JSON
with open(TESTS_DATA_FILE, 'r') as file: 
    TEST_DATA = json.load(file)

# Prepend absolute path to each image_path in the test data
for item in TEST_DATA: 
    item['image_path'] = os.path.join(IMAGE_DIR, item['image_path'])

app = QApplication(sys.argv)

###########################################################################################################################
###########################################################################################################################

@parameterized_class(TEST_DATA)
class Test_Image_Processing(unittest.TestCase):
    def setUp(self):
    
        """
        Prepares the test case by verifying image existence and initializing the image processor. This function will run
        before every test function.
        """

        # Check that the test image file exists
        self.assertTrue(os.path.exists(self.image_path), f'File not found: {self.image_path}')

        # Create the Image_Processing object with the image path
        self.image = Image_Processing(self.image_path)

        # Reset resized image to None before each test
        self.image.resized_image = None

    #######################################################################################################################
    #######################################################################################################################

    def test_load_image(self):
        
        """
        Tests whether the image is correctly loaded and has the expected dimensions.

        Asserts:
            - The image object is not None.
            - The image size matches the expected dimensions.
        """

        # Ensure the image was loaded
        self.assertIsNotNone(self.image.original_image, f'Failed to load image: {self.image_path}')

        # Check the loaded image size
        width, height = self.image.original_image.shape[1::-1]
        self.assertEqual((width, height), tuple(self.image_original_size), f'Image size mismatch for {self.image_path}')

    #######################################################################################################################
    #######################################################################################################################

    def test_resize_image(self):

        """
        Tests whether the image is resized correctly to fit within the target frame size, while maintaining aspect ratio.

        Asserts:
            - The resized image is not None.
            - The resized image fits within the desired bounding box (CONST.MAIN_FRAME_SIZE).
        """

        # Perform the resizing operation
        self.image.resize_image()

        # Ensure the resized image exists
        self.assertIsNotNone(self.image.resized_image, 'Failed to resize image')

        # Get width and height of the resized image
        width, height = self.image.resized_image.shape[1::-1]

        # Check that the resized dimensions fit within the desired bounding box
        self.assertLessEqual(width, CONST.MAIN_FRAME_SIZE[0], 'Resized width exceeds limit')
        self.assertLessEqual(height, CONST.MAIN_FRAME_SIZE[1], 'Resized height exceeds limit')

        # Assert aspect ratio is preserved within reasonable error of ±1 pixel
        original_ratio = self.image.original_image.shape[1] / self.image.original_image.shape[0]
        resized_ratio = width / height
        self.assertAlmostEqual(resized_ratio, original_ratio, places = 2, msg = 'Aspect ratio not preserved')

    #######################################################################################################################
    #######################################################################################################################

    def test_is_pokemon_name_recognized(self):

        """
        Tests whether the Pokémon name is correctly recognized from the image. Skips the test if the current test case does
        not include a Pokémon name.

        Asserts:
            - The recognized Pokémon name matches the expected one.
        """

        # Skip this test if the image doesn't contain a Pokémon name
        if not self.has_pokemon_name:
            self.skipTest("Skipping because image is not showing a pokémon name (has_pokemon_name = False)")

        # Resize the image to standard dimensions before recognition
        self.image.resize_image()

        # Attempt to recognize the Pokémon name from the image
        recognized_name = self.image.recognize_pokemon()

        # Assert that the recognized name matches the expected one
        self.assertEqual(self.pokemon_name, recognized_name, 'Failed to recognize Pokémon name')
  
    #######################################################################################################################
    #######################################################################################################################
  
    def test_get_pyqt_image(self):

        """
        Tests whether an OpenCV image (color or grayscale) is correctly converted into a PyQt QPixmap.

        Asserts:
            - The resulting PyQt image is not None.
            - The resulting type is QPixmap.
            - The dimensions match the original input image.
        """

        # Use the resized image to convert
        self.image.resize_image()
        input_image = self.image.resized_image

        # Simulate grayscale image if needed (forcefully convert)
        if len(input_image.shape) == 3 and self.force_pyqt_grayscale:
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        self.image.get_pyqt_image(input_image)

        # Check that the output is a valid QPixmap
        self.assertIsNotNone(self.image.pyqt_image, 'Failed to convert to PyQt image')
        self.assertIsInstance(self.image.pyqt_image, pyqt_g.QPixmap, 'Result is not a QPixmap')

        # Verify that dimensions match the input
        expected_width, expected_height = input_image.shape[1::-1]
        self.assertEqual(self.image.pyqt_image.width(), expected_width, 'QPixmap width mismatch')
        self.assertEqual(self.image.pyqt_image.height(), expected_height, 'QPixmap height mismatch')

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()