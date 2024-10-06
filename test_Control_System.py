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
import Control_System

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Media/Images'))

###########################################################################################################################

# Add new tests here
@parameterized_class([
    {
        'image_path': os.path.join(IMAGE_DIR, 'Regice_720p.png'),
        'has_text_box': True,
        'has_life_box': False,
        'has_black_screen': False,
        'has_white_screen': False,
    },
    {
        'image_path': os.path.join(IMAGE_DIR, 'Regice_1080p.png'),
        'has_text_box': True,
        'has_life_box': False,
        'has_black_screen': False,
        'has_white_screen': False,
    },
    {
        'image_path': os.path.join(IMAGE_DIR, 'white_screen_test1_720p.png'),
        'has_text_box': False,
        'has_life_box': False,
        'has_black_screen': False,
        'has_white_screen': False,
    },
])
class Test_Control_System(unittest.TestCase): 
    def setUp(self):
        # Ensure the file exists
        self.assertTrue(os.path.exists(self.image_path), f'File not found: {self.image_path}')

        # Initialize the ImageProcessor object
        self.image = Image_Processing(self.image_path)
        self.image.resize_image()
    
    #######################################################################################################################

    def test_text_box_visibility(self):
        # Test if the text box is visible
        text_box_visible = Control_System.is_text_box_visible(self.image)
        self.assertEqual(self.has_text_box, text_box_visible, 'Failed to recognize text box')

    #######################################################################################################################

    def test_is_black_screen_visible(self):
        # Test if black screen is visible
        black_screen_visible = Control_System.is_black_screen_visible(self.image)
        self.assertEqual(self.has_black_screen, black_screen_visible, 'Failed to recognize black screen')

    #######################################################################################################################

    def test_is_life_box_visible(self):
        # Test if life box is visible
        life_box_visible = Control_System.is_life_box_visible(self.image)
        self.assertEqual(self.has_life_box, life_box_visible, 'Failed to recognize life box')

    #######################################################################################################################

    def test_is_load_fight_white_screen(self):
        # Test if the white screen is visible
        white_screen_visible = Control_System.is_load_fight_white_screen(self.image)
        self.assertEqual(self.has_white_screen, white_screen_visible, 'Failed to recognize white screen')

    #######################################################################################################################

    def tearDown(self):
        # Clean up any resources if needed
        pass

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()
