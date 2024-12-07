import unittest
from clarity import parse_app_access
from tests import TestConstants,clear_test_output_dir
import os

class TestClarityParsers(unittest.TestCase):
    def test_parse_app_access(self):
        result=parse_app_access(filepath=TestConstants.MOCK_DATA_APP_ACCESS.value,output_dir=TestConstants.TEST_OUTPUT_DIR.value,file_prefix="mock_app-access",ignore_extension=".csv")
        output_path=os.path.join(TestConstants.TEST_OUTPUT_DIR.value,'mock_app-access.csv')
        with open(output_path,'r') as f:
            lines =f.readlines()
        self.assertEqual(len(lines),5)
        output_path=os.path.join(TestConstants.TEST_OUTPUT_DIR.value,'mock_app-access_non_api.csv')
        with open(output_path,'r') as f:
            lines =f.readlines()
        self.assertEqual(len(lines),2)
    
    def tearDown(self):
        clear_test_output_dir()
        # pass