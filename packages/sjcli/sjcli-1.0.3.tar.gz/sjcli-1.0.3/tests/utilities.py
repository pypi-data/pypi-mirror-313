from enum import Enum
import os
class TestConstants(Enum):
    MOCK_DATA_DIR=os.path.join(os.getcwd(),"tests","mocks")
    MOCK_DATA_CSV=os.path.join(os.getcwd(),"tests","mocks","mock_test.csv")
    MOCK_DATA_JSON=os.path.join(os.getcwd(),"tests","mocks","mock_test.json")
    MOCK_DATA_APP_ACCESS=os.path.join(os.getcwd(),"tests","mocks",'mock_app-access.log')
    TEST_OUTPUT_DIR=os.path.join(os.getcwd(),"tests","output")

# common tear down function
def clear_test_output_dir():
    if os.path.exists(TestConstants.TEST_OUTPUT_DIR.value):
        files=os.listdir(TestConstants.TEST_OUTPUT_DIR.value)
        for file in files:
            file_path=os.path.join(TestConstants.TEST_OUTPUT_DIR.value,file)
            if os.path.exists(file_path):
                os.remove(file_path)

# common file existence function
def check_file_exist(filepath):
    return os.path.exists(filepath)
