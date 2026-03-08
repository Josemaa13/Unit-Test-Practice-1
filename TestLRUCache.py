import unittest
from tests import *
from lab_2_part_1 import LRUCache
from decimal import Decimal
from ToDoItem import ToDoItem

class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(3)
        self.cache.put(3,"a")
        self.cache.put(4,"b")
    
    def test_init(self):
        with self.assertRaises(TypeError):
            c = LRUCache(Decimal("3.20"))
        
        with self.assertRaises(ValueError):
            c = LRUCache(-1)
    
    def test_size(self):
        self.assertEqual(self.cache.size(),2)
        
    def test_contains_key(self):
        self.assertTrue(self.cache.contains_key(3))
        self.assertFalse(self.cache.contains_key(2))
    
    def test_get(self):
        self.assertEqual(self.cache.get(3), 'a')
        self.assertEqual(self.cache.get(2), None)
        
    def test_put(self):
        self.assertEqual(self.cache.size(), 2)
        self.cache.put(5,'c')
        self.assertEqual(self.cache.size(), 3)
        self.assertEqual(self.cache.get(5), 'c')
        
    def test_eviction(self):
        self.cache.put(5,'c')
        self.cache.put(6,'d')
        self.assertIsNone(self.cache.get(3))
        self.assertEqual(self.cache.size(), 3)
        self.cache._touch(4)
        self.cache.put(7,'e')
        self.assertIsNone(self.cache.get(5))
        self.assertEqual(self.cache.size(), 3)


        
    
    
    
    
if __name__ == "__main__":
    unittest.main()


