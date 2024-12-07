import unittest
from sjcli import utils
from utils.helpers import get_files_path, build_filename_from_path, get_timestamp_stats_from_csv, normalize_timestamp
from tests import TestConstants,clear_test_output_dir,check_file_exist
import os

class HelpersTest(unittest.TestCase):
    def test_get_files_path_csv(self):
        """Validate get the files 'ABSOLUTE PATH' with specific 'FILE EXTENSION' from respective directory/filepath."""
        actual_output=get_files_path(TestConstants.MOCK_DATA_CSV.value,file_prefix="",ignore_extension="")
        self.assertEqual(actual_output[0],TestConstants.MOCK_DATA_CSV.value,msg="Failed Reason: Files Path are not equal")

    def test_get_files_path_returns_list(self):
        """Validate get the files 'ABSOLUTE PATH' with specific 'FILE EXTENSION' from respective directory/filepath return list"""
        actual_output=get_files_path(TestConstants.MOCK_DATA_CSV.value,file_prefix="",ignore_extension="")
        self.assertEqual(type(actual_output).__name__,'list',msg="Failed Reason: Return type is not list.")

    def test_get_files_path_dir(self):
        """Validate get the files 'ABSOLUTE PATH' with specific 'FILE EXTENSION' from respective directory/filepath."""
        actual_output=get_files_path(TestConstants.MOCK_DATA_DIR.value,file_prefix="mock_test",ignore_extension=".csv")
        self.assertEqual(actual_output[0],TestConstants.MOCK_DATA_JSON.value)
        self.assertEqual(len(actual_output),1,msg="Failed Reason: The return list if not of length 1")
        

    def test_build_file_name_from_path(self):
        """Validate get the file name from given 'FILE PATH' dropping 'FILE EXTENSION' """
        actual_output=build_filename_from_path(filepath=TestConstants.MOCK_DATA_CSV.value,extension="xlsx")
        expected_output='mock_test.xlsx'
        self.assertEqual(expected_output,actual_output,msg="Failed Reason: File name are not equal")
    
    def test_build_file_name_from_path_with_noextension(self):
        """Validate get the file name from given 'FILE PATH' dropping 'FILE EXTENSION' """
        actual_output=build_filename_from_path(filepath=TestConstants.MOCK_DATA_CSV.value,extension=None)
        expected_output='mock_test'
        self.assertEqual(expected_output,actual_output,msg="Failed Reason: File name are not equal")

    def test_get_timestamp_stats_from_csv_at_index1(self):
        output_file=os.path.join(TestConstants.TEST_OUTPUT_DIR.value,'timestamp_stats.csv')
        result=get_timestamp_stats_from_csv(input_dir=TestConstants.MOCK_DATA_DIR.value,date_col_index=1,output_dir=TestConstants.TEST_OUTPUT_DIR.value,
                                     file_prefix='mock_timestamp_test',ignore_extension='.json')
        expected_result=check_file_exist(output_file)
        self.assertTrue(expected_result,f"ERROR: Output file {output_file} not created")
    
    def test_get_timestamp_stats_from_csv_at_index0(self):
        output_file=os.path.join(TestConstants.TEST_OUTPUT_DIR.value,'timestamp_stats_col0.csv')
        result=get_timestamp_stats_from_csv(input_dir=TestConstants.MOCK_DATA_DIR.value,date_col_index=0,output_dir=TestConstants.TEST_OUTPUT_DIR.value,output_file='timestamp_stats_col0.csv',
                                     file_prefix='mock_timestamp_col0_test',ignore_extension='.json')
        expected_result=check_file_exist(output_file)
        self.assertTrue(expected_result,f"ERROR: Output file {output_file} not created")
    
    def test_normalize_time_stamp_with_timezone(self):
        result=normalize_timestamp(value="[22/Nov/2024:01:02:36 -0600]")
        self.assertEqual(result,"22/Nov/2024:01:02:36 -0600")

    def test_normalize_time_stamp_without_timezone(self):
        result=normalize_timestamp(value="[22/Nov/2024:01:02:36 -0600]",remove_timezone=True)
        self.assertEqual(result,"22/Nov/2024:01:02:36")

    def tearDown(self):
        clear_test_output_dir()
        # pass
    