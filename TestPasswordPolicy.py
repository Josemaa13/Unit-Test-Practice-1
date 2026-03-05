from ToDoItem import ToDoItem
import unittest
from lab_2_part_1 import PasswordValidationResult, PasswordPolicy
from tests import *

class TestPasswordPolicy(unittest.TestCase):
    def setUp(self):
        self.default_policy = PasswordPolicy()
        self.strict_policy = PasswordPolicy(require_special=True)
    
    #1
    def test_valid_password(self):
        result = self.default_policy.validate("Hola1Mundo")
        #result = self.strict_policy.validate("Hola1Mundo")
        
        self.assertTrue(result.ok)
        self.assertEqual(len(result.errors), 0)

    
    #2
    def test_shorter_min_length(self):
        result = self.default_policy.validate("A1b")
        
        self.assertFalse(result.ok)
        self.assertIn("length<8", result.errors)
            
            
    #3
    def test_longer_max_length(self):
        result = self.default_policy.validate("aBcdefghijklmnopq1")
        
        self.assertFalse(result.ok)
        self.assertIn("length>16", result.errors)
    
    
    #4
    def test_missing_uppercase_digit_special_character(self):
        #Falta upper
        res_no_upper = self.strict_policy.validate("holamundo1!")
        self.assertFalse(res_no_upper.ok)
        self.assertIn("missing_upper", res_no_upper.errors)

        #Falta digit
        res_no_digit = self.strict_policy.validate("Holamundo!")
        self.assertFalse(res_no_digit.ok)
        self.assertIn("missing_digit", res_no_digit.errors)

        #Falta special character
        res_no_special = self.strict_policy.validate("Hola1mundo")
        self.assertFalse(res_no_special.ok)
        self.assertIn("missing_special", res_no_special.errors)
        
        
    #5
    def test_spaces(self):
        result = self.default_policy.validate("Hola Mundo1")
        self.assertFalse(result.ok)
        self.assertIn("contains_space", result.errors)
    
    
    #6
    def test_multiple_violations(self):
        result = self.default_policy.validate("a b")
        self.assertFalse(result.ok)
        self.assertIn("length<8", result.errors)
        self.assertIn("missing_upper", result.errors)
        self.assertIn("missing_digit", result.errors)
        self.assertIn("contains_space", result.errors)
    
if __name__ == '__main__':
    unittest.main()
    
