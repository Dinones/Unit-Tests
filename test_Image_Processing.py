###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import unittest
from parameterized import parameterized_class

import sys
folders = ['../', '../Modules']
for folder in folders: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))

from Image_Processing import Image_Processing
import Constants as CONST
import Control_System

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Media/Images'))

###########################################################################################################################

@parameterized_class([
    {
        'image_path': os.path.join(IMAGE_DIR, 'Regice_720p.png'),
        'image_size': (1280, 720),
        'has_pokemon_name': True,
        'pokemon_name': 'Regice', # Leave empty if 'has_pokemon_name' is False
    },
    {
        'image_path': os.path.join(IMAGE_DIR, 'Regice_1080p.png'),
        'image_size': (1920, 1080),
        'has_pokemon_name': True,
        'pokemon_name': 'Regice', # Leave empty if 'has_pokemon_name' is False
    },
])
class Test_Image_Processing(unittest.TestCase):
    def setUp(self):
        # Ensure the file exists
        self.assertTrue(os.path.exists(self.image_path), f'File not found: {self.image_path}')

        # Initialize the ImageProcessor object
        self.image = Image_Processing(self.image_path)
        self.image.resized_image = None

    #######################################################################################################################

    def test_load_image(self):
        # Test loading an image
        self.assertIsNotNone(self.image.original_image, f'Failed to load {self.image_path}')

        size = self.image.original_image.shape[1::-1]
        self.assertEqual(size, self.image_size, f'Failed to load {self.image_path}')

    #######################################################################################################################

    def test_resize_image(self):
        # Test resizing an image
        self.image.resize_image()
        self.assertIsNotNone(self.image.resized_image, 'Failed to resize image')

        size = self.image.resized_image.shape[1::-1]
        self.assertEqual(size, CONST.MAIN_FRAME_SIZE, 'Failed to resize image')

    #######################################################################################################################

    def test_is_pokemon_name_recognized(self):
        # Test if the pokémon name is recognized correctly
        # Skip the test if has_pokemon_name is False
        if not self.has_pokemon_name: self.skipTest("Skipping because 'has_pokemon_name' is False")

        self.image.resize_image()
        pokemon_name = self.image.recognize_pokemon()
        self.assertEqual(self.pokemon_name, pokemon_name, f'Failed to recognize pokémon name')

    #######################################################################################################################

    def tearDown(self):
        # Clean up any resources if needed
        pass

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()