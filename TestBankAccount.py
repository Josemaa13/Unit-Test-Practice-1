import unittest
from tests import *
from lab_2_part_1 import Transaction, BankAccount
from decimal import Decimal


class testBankAccount(unittest.TestCase):
   def setUp(self):
      self.poor = BankAccount()
      self.rich = BankAccount(Decimal("100000"))
    
   def test_init_and_get_balance(self):
      self.assertEqual(self.poor.get_balance(), Decimal("0"))
      self.assertEqual(self.rich.get_balance(), Decimal("100000"))

      with self.assertRaises(TypeError):
         self.bad_account = BankAccount(3)
    
   def test_deposit(self):
      self.poor.deposit(Decimal("50.00"), "Regalo")
      self.assertEqual(self.poor.get_balance(), Decimal("50.00"))
      self.assertEqual(len(self.poor.get_statement()),1)
      statement = self.poor.get_statement()
      self.assertEqual(statement[0].kind, "deposit")
      
      
      with self.assertRaises(ValueError):
         self.poor.withdraw(Decimal("10.00"))
      
      with self.assertRaises(ValueError):
         self.poor.deposit(Decimal("-5.0"))
         
      with self.assertRaises(ValueError):
         self.poor.deposit(Decimal("0"))
      
   def test_withdraw(self):
      self.rich.withdraw(Decimal("4500.01"))
      self.assertEqual(self.rich.get_balance(), Decimal("95499.99"))
      record = self.rich.get_statement()
      self.assertEqual(len(record), 1)
      self.assertEqual(record[0].kind, "withdraw")
      
      with self.assertRaises(ValueError):
         self.rich.withdraw(Decimal("-3.29"))
      
      with self.assertRaises(ValueError):
         self.rich.withdraw(Decimal("0"))
         
   def test_statement_is_immutable(self):
      self.poor.deposit(Decimal("35.00"), "Regalo")
      historial = self.poor.get_statement()
      
      with self.assertRaises(TypeError):
         historial[0] = "Hackeado :)"
      
         

if __name__ == "__main__":
    unittest.main()
