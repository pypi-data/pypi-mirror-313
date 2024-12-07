import unittest
from utils.decorators import pprint

class DecoratorsTest(unittest.TestCase):
    
    def test_pprint_str(self):
        message="Hello"
        expected_output="\n"+"-"*50+"\n"+message+"\n"+"-"*50
        result=pprint(message=message,return_result=True)
        self.assertEqual(expected_output,result)
    
    def test_pprint_list(self):
        message=[(1, 'A'), (2, 'B')]
        # expected_output="\n"+"-"*50+"\n"+message+"\n"+"-"*50
        expected_output="\n"+"-"*50+"\n( 1 ,   ' A ' )\n( 2 ,   ' B ' )\n"+"-"*50
        result=pprint(message=message,return_result=True)
        self.assertEqual(expected_output,result)
    
    def test_pprint_tuple(self):
        message=(1, 'A')
        # expected_output="\n"+"-"*50+"\n"+message+"\n"+"-"*50
        expected_output="\n"+"-"*50+"\n( 1 ,   ' A ' )\n"+"-"*50
        result=pprint(message=message,return_result=True)
        self.assertEqual(expected_output,result)
  