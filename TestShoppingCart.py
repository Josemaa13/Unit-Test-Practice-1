import unittest
from tests import *
from lab_2_part_1 import CartItem, ShoppingCart
from decimal import Decimal

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.carrito_1 = ShoppingCart(Decimal("1.10"))

    def test_init(self):
        with self.assertRaises(ValueError):
            cheese = CartItem("", Decimal("2.20"), 1)
        
        with self.assertRaises(TypeError):
            cheese = CartItem("1234d", 3, 1)
            
        with self.assertRaises(ValueError):
            cheese = CartItem("1234d", Decimal("-1.5"), 1)
            
        with self.assertRaises(TypeError):
            cheese = CartItem("1234d", Decimal("1.5"), Decimal("1.4"))
            
        with self.assertRaises(ValueError):
            cheese = CartItem("1234d", Decimal("2.20"), 0)
            
        with self.assertRaises(TypeError):
            carrito_f = ShoppingCart(3)
            
        with self.assertRaises(ValueError):
            carrito_f1 = ShoppingCart(Decimal("124"))
        
        
    def test_add_to_shoppingcart(self):
        self.carrito_1.add_item("12b34", Decimal("5.65"), 1)
        self.assertEqual(self.carrito_1.subtotal(), Decimal("5.65"))
    
    def test_add_the_same_sku(self):
        carrito_1 = ShoppingCart(Decimal("1.10"))
        carrito_1.add_item("12b34", Decimal("5.65"), 1)
        carrito_1.add_item("12b34", Decimal("5.65"), 1)
        self.assertEqual(carrito_1.subtotal(), Decimal("11.30"))
        
    def test_remove_sku(self):
        carrito_1 = ShoppingCart(Decimal("1.10"))
        carrito_1.add_item("12b34", Decimal("5.65"), 1)
        self.assertEqual(carrito_1.subtotal(), Decimal("5.65"))
        carrito_1.remove_sku("12b34")
        self.assertEqual(carrito_1.total_items(), 0)
        
    def test_total_item(self):
        carrito_1 = ShoppingCart(Decimal("1.10"))
        carrito_1.add_item("12b34", Decimal("5.65"), 1)
        carrito_1.add_item("123c4", Decimal("10.25"), 4)
        self.assertEqual(carrito_1.total_items(), 5)
        
    def test_apply_discount(self):
        carrito_1 = ShoppingCart(Decimal("50"))
        carrito_1.add_item("12b34", Decimal("5.65"), 1)
        self.assertEqual(carrito_1.total(), Decimal("2.83"))

    
    def test_negative_price(self):
        carrito_1 = ShoppingCart(Decimal("1.10"))
        with self.assertRaises(ValueError):
            carrito_1.add_item("12b34", Decimal("-1.45"), 1)

    
    
if __name__ == '__main__':
    unittest.main()