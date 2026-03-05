from ToDoItem import ToDoItem
import unittest
from lab_2_part_1 import PasswordValidationResult, PasswordPolicy
from tests import *

class TestPasswordPolicy(unittest.TestCase):
    def setUp(self):
        self.default_policy = PasswordPolicy()
    
    #1
    def test_valid_password(self):
        result = self.default_policy.validate("Hola1Mundo")
        
        self.assertTrue(result.ok)
        self.assertEqual(len(result.errors), 0)

    
    #2
    
    
    #3
    
    
    #4
    
    
    #5