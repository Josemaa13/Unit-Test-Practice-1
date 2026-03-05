from ToDoItem import ToDoItem
import unittest
from lab_2_part_1 import Money
from tests import *

class TestMoney(unittest.TestCase):
    #1
    def test_add_same_currency_returns_correct_result(self):
        m1 = Money(Decimal("10.50"), "EUR")
        m2 = Money(Decimal("5.25"), "EUR")
    
        result = m1.add(m2)
        
        self.assertEqual(result, Money(Decimal("15.75"), "EUR"))
    
    #2    
    def test_add_different_currency(self):
        m1 = Money(Decimal("5.00"), "EUR")
        m2 = Money(Decimal("2.55"), "USD")
        
        with self.assertRaises(ValueError):
            m1.add(m2)

    #3
    def test_substract_with_positive_and_negative_results(self):
        m1 = Money(Decimal("10.50"), "EUR")
        m2 = Money(Decimal("5.25"), "EUR")
        m3 = Money(Decimal("2.25"), "EUR")
        
        result_pos = m2.subtract(m3)
        result_neg = m3.subtract(m1)
        
        self.assertEqual(result_pos.amount, Decimal("3.00"))
        self.assertFalse(result_pos.is_negative())
        
        self.assertEqual(result_neg.amount, Decimal("-8.25"))
        self.assertTrue(result_neg.is_negative())        

    #4
    def test_multiply_positive_zero_negative_factors(self):
        m1 = Money(Decimal("10.00"), "EUR")
        
        result_pos = m1.multiply(2)
        self.assertEqual(result_pos.amount, Decimal("20.00"))        
        
        result_neg = m1.multiply(-1)
        self.assertEqual(result_neg.amount, Decimal("-10.00"))

        result_zero = m1.multiply(0)
        self.assertEqual(result_zero.amount, Decimal("0.00"))

    #5
    def test_compare_less_equal_greater_than(self):
        m_large = Money(Decimal("10.50"), "EUR")
        m_equal = Money(Decimal("5.25"), "EUR")
        m_small = Money(Decimal("5.25"), "EUR")
        
        self.assertEqual(m_small.compare_to(m_large), -1)
        self.assertEqual(m_small.compare_to(m_equal), 0)
        self.assertEqual(m_large.compare_to(m_small), 1)
        
    def test_equality_behavior(self):
        m1 = Money(Decimal("10.00"), "EUR")
        m2 = Money(Decimal("10.00"), "EUR") 
        m3 = Money(Decimal("10.00"), "USD")  
        m4 = Money(Decimal("5.00"), "EUR")   
        
        # Son iguales si coinciden cantidad y moneda
        self.assertTrue(m1 == m2)
        
        # Falsos si falla uno de los dos atributos
        self.assertFalse(m1 == m3)
        self.assertFalse(m1 == m4)
        
        # Falso si se compara con otro tipo de objeto
        self.assertFalse(m1 == "10.00 EUR")

if __name__ == '__main__':
    unittest.main()
    
