import unittest
from click.testing import CliRunner
from sjcli import cli
from sjcli import utils
from utils.file_helpers import write_csv_data
import os
from tests import TestConstants,clear_test_output_dir,check_file_exist

MOCK_DATA=os.path.join(os.getcwd(),"tests","mocks","mock_test.csv")
TEST_OUTPUT_DIR=os.path.join(os.getcwd(),"tests","output")

class SJCLI_CSV_Test(unittest.TestCase):
    def setup(self):
        clear_test_output_dir()
    
    def test_cli_utils_preview_csv_filename_argument_missing(self):
        runner=CliRunner()
        cli_command=["utils",'csv']
        result=runner.invoke(cli,cli_command)
        actual_output=result.output.strip().split('\n')[-1]
        expected_output=f"Error: Missing argument 'FILE_NAME'."
        self.assertEqual(actual_output,expected_output)
    
    def test_cli_utils_preview_csv(self):
        runner=CliRunner()
        cli_command=["utils",'csv',TestConstants.MOCK_DATA_CSV.value,"-n","1"]
        result=runner.invoke(cli,cli_command)
        expected_output="A  B  C"
        self.assertEqual(result.output.split('\n')[1],expected_output)
    
    def test_cli_utils_write_csv(self):
        output_file=os.path.join(TestConstants.TEST_OUTPUT_DIR.value,"test.csv")
        result=write_csv_data(output_file,[["A","B"],[1,2]])
        self.assertTrue(check_file_exist(output_file))

    def tearDown(self):
        clear_test_output_dir()
        

if __name__=="__main__":
    unittest.main()