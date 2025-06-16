import unittest

from calc import Calculator


class TestCalc(unittest.TestCase):
    def test_add(self):
        calc = Calculator()
        self.assertEqual(calc.add(2, 1), 3)
        self.assertEqual(calc.add(), 0)

    def test_subtract(self):
        calc = Calculator()
        self.assertEqual(calc.subtract(2, 1), 1)
        self.assertEqual(calc.subtract(), 0)

    def test_multiply(self):
        calc = Calculator()
        self.assertEqual(calc.multiply(2, 1), 2)
        self.assertEqual(calc.multiply(), 0)

    def test_divide(self):
        calc = Calculator()
        self.assertEqual(calc.divide(2, 1), 2)
        with self.assertRaises(ZeroDivisionError):
            calc.divide()
        self.assertEqual(calc.divide(2), 1)


if __name__ == "__main__":
    unittest.main()
