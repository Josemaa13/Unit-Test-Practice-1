import unittest
from lab_2_part_1 import DateRange
from tests import *
from ToDoItem import ToDoItem
from datetime import date


class TestDateRange(unittest.TestCase):
    
    def setUp(self):
        self.d1 = date(2025,1,1)
        self.d2 = date(2025,2,23)
        self.d3 = date(2025,1,30)
        
        self.range = DateRange(self.d3, self.d2)
        
    def test_init(self):
        with self.assertRaises(ValueError):
            bad_range1 = DateRange(self.d2, self.d1)
            
        with self.assertRaises(TypeError):  
            bad_range2 = DateRange(self.d2, 2)  

    def test_contains(self):
        fecha_media = date(2025,2,2)
        range1 = self.range.contains(self.d1)
        range2 = self.range.contains(self.d2)
        range3 = self.range.contains(fecha_media)
        self.assertFalse(range1)
        self.assertTrue(range2)
        self.assertTrue(range3)
    
    
    def test_days_inclusive(self):
        result = self.range.days_inclusive()
        self.assertEqual(result,25)

    def test_overlap(self):
        rango_abril_1_15 = DateRange(date(2025,4,1), date(2025,4,15))
        rango_abril_16_30 = DateRange(date(2025,4,16), date(2025,4,30))
        rango_abril_10_20 = DateRange(date(2025,4,15), date(2025,4,30))
        
        self.assertFalse(rango_abril_1_15.overlaps(rango_abril_16_30))
        self.assertTrue(rango_abril_1_15.overlaps(rango_abril_10_20))
     
        
        with self.assertRaises(TypeError):
            rango_abril_1_15.overlaps("AaAa")
    
    def test_intersection(self):    
        rango_abril = DateRange(date(2025,4,1), date(2025,4,30))
        rango_abril_mayo = DateRange(date(2025,4,1), date(2025,5,5))
        rango_esperado = DateRange(date(2025,5,1), date(2025,5,5))
        rango_mayo = DateRange(date(2025,5,1), date(2025,5,31))
        result = rango_abril.intersection(rango_mayo)
        new_result = rango_abril_mayo.intersection(rango_mayo)
        
        self.assertEqual(result, None)
        self.assertEqual(new_result, rango_esperado)
                    


if __name__ == '__main__':
        unittest.main()