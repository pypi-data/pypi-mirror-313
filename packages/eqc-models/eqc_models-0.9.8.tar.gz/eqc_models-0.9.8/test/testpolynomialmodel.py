# (C) Quantum Computing Inc., 2024.
from unittest import TestCase
from eqc_models import PolynomialModel

class EvalPolynomialTestCase(TestCase):

    def setUp(self):
        coefficients = [1, 2, 3]
        indices = [[0, 0, 1], [0, 1, 1], [1, 1, 1]]
        self.polynomial = PolynomialModel(coefficients, indices)

    def testEval1(self):
        polynomial = self.polynomial
        solution = [1]
        value = polynomial.evaluate(solution)
        self.assertEqual(value, 6)

    def testEval10(self):
        polynomial = self.polynomial
        solution = [10]
        value = polynomial.evaluate(solution)
        self.assertEqual(value, 1*solution[0]+2*solution[0]**2+3*solution[0]**3)

class PolynomialAttributesTestCase(TestCase):

    def setUp(self):
        self.coefficients = [1, 2, 3]
        self.indices = [[0, 0, 1], [0, 1, 1], [1, 1, 1]]
        self.polynomial = PolynomialModel(self.coefficients, self.indices)

    def testH(self):
        self.polynomial.H == (self.coefficients, self.indices)