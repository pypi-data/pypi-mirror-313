import unittest
from click.testing import CliRunner
from sjcli import cli
import os

MOCK_DATA=os.path.join(os.getcwd(),"tests","mocks","mock_test.json")

class SJCLI_JSON_Test(unittest.TestCase):
    
    def test_cli_utils_preview_json_lines(self):
        runner=CliRunner()
        cli_command=["utils",'json',MOCK_DATA,"-n","1"]
        result=runner.invoke(cli,cli_command)
        expected_output="["
        self.assertEqual(result.output.strip("\n"),expected_output)
    
    def test_cli_utils_preview_json_indent(self):
        runner=CliRunner()
        cli_command=["utils",'json',MOCK_DATA,"-i","0"]
        result=runner.invoke(cli,cli_command)
        expected_output='[{"name": "A","age": 40},{"name": "B","age": 40}]'
        self.assertEqual(result.output.strip('\n'),expected_output)

    def test_cli_utils_preview_json_filename_argument_missing(self):
        runner=CliRunner()
        cli_command=["utils",'json']
        result=runner.invoke(cli,cli_command)
        actual_output=result.output.strip().split('\n')[-1]
        expected_output=f"Error: Missing argument 'FILE_NAME'."
        self.assertEqual(actual_output,expected_output)
        
if __name__=="__main__":
    unittest.main()