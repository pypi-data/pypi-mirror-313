import unittest
from click.testing import CliRunner
from sjcli import cli
from utilities import clear_test_output_dir

class SJCLITest(unittest.TestCase):

    def test_version_exit_code(self):
        runner=CliRunner()
        result=runner.invoke(cli,["--version"])
        self.assertEqual(0,result.exit_code)

    def test_version_number(self):
        runner=CliRunner()
        result=runner.invoke(cli,["--version"])
        self.assertEqual("cli, version 0.2.0",result.stdout.strip('\n'))

    def test_invalid_cli_option_status(self):
        runner=CliRunner()
        cli_command="utilss"
        result=runner.invoke(cli,cli_command)
        self.assertNotEqual(0, result.exit_code)
        
    def test_invalid_cli_option(self):
        runner=CliRunner()
        cli_command="utilss"
        result=runner.invoke(cli,cli_command)
        actual_output=result.output.strip().split('\n')[-1]
        expected_output=f"Error: No such command '{cli_command}'."
        self.assertEqual(actual_output,expected_output)
    def tearDown(self):
        clear_test_output_dir()
    
if __name__=="__main__":
    unittest.main()