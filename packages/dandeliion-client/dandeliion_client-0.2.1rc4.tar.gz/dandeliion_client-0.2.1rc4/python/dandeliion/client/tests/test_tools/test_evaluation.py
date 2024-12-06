import unittest
import numpy as np

from numpy.testing import assert_allclose
from dandeliion.client.tools.evaluation import (
    evaluate_function,
    evaluate_div_function,
    evaluate_int_function
)


class EvaluateFunctionTest(unittest.TestCase):
    def test_sin(self):
        '''Test function evaluation all finite with derivative and integral'''
        expected_x_eval = np.linspace(0, 1, 1001)
        expected_f_x = np.sin(expected_x_eval)
        expected_f_div_x = np.cos(expected_x_eval)
        expected_f_int_x = 1 - np.cos(expected_x_eval)

        f_string = 'sin(x)'
        result_x_eval, result_f_x = evaluate_function(
            f_string,
            lower=0,
            upper=1,
            steps=1001
        )
        result_x_div_eval, result_f_div_x = evaluate_div_function(
            f_string,
            lower=0,
            upper=1,
            steps=1001
        )
        result_x_int_eval, result_f_int_x = evaluate_int_function(
            (result_x_eval, result_f_x)
        )
        # check returned as list
        self.assertIsInstance(result_x_eval, list)
        self.assertIsInstance(result_x_div_eval, list)
        self.assertIsInstance(result_x_int_eval, list)
        self.assertIsInstance(result_f_x, list)
        self.assertIsInstance(result_f_div_x, list)
        self.assertIsInstance(result_f_int_x, list)
        # check values
        assert_allclose(result_x_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_x_div_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_x_int_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_x, expected_f_x, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_div_x, expected_f_div_x, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_int_x, expected_f_int_x, rtol=1e-7, atol=1e-7)

    def test_ln(self):
        '''Test function evaluation with divide by zero with derivative and integral'''
        expected_x_eval = np.linspace(0, 1, 1001)

        # set first value to finite interpolation
        expected_f_x = np.log(expected_x_eval)
        expected_f_x[0] = 2 * expected_f_x[1] - expected_f_x[2]

        # set first value to finite interpolation
        expected_f_div_x = 1 / expected_x_eval
        expected_f_div_x[0] = 2 * expected_f_div_x[1] - expected_f_div_x[2]

        # Offset chosen to match closely with the one found using trap rule
        # first value set to zero
        expected_f_int_x = expected_x_eval * (np.log(expected_x_eval) - 1) + 0.00057
        expected_f_int_x[0] = 0

        f_string = 'log(x)'
        result_x_eval, result_f_x = evaluate_function(
            f_string,
            lower=0,
            upper=1,
            steps=1001
        )
        result_x_div_eval, result_f_div_x = evaluate_div_function(
            f_string,
            lower=0,
            upper=1,
            steps=1001
        )
        result_x_int_eval, result_f_int_x = evaluate_int_function(
            (result_x_eval, result_f_x)
        )
        assert_allclose(result_x_eval, expected_x_eval, rtol=1e-4, atol=1e-4)
        assert_allclose(result_x_div_eval, expected_x_eval, rtol=1e-4, atol=1e-4)
        assert_allclose(result_x_int_eval, expected_x_eval, rtol=1e-4, atol=1e-4)
        assert_allclose(result_f_x, expected_f_x, rtol=1e-4, atol=1e-4)
        assert_allclose(result_f_div_x, expected_f_div_x, rtol=1e-4, atol=1e-4)
        assert_allclose(result_f_int_x, expected_f_int_x, rtol=1e-4, atol=1e-4)

    def test_constant_int(self):
        '''Test when function is a constant integer with derivative and integral'''
        expected_x_eval = np.linspace(0, 1, 1001)
        expected_f_x = 3 * np.ones_like(expected_x_eval)
        expected_f_div_x = np.zeros_like(expected_x_eval)
        expected_f_int_x = 3 * expected_x_eval

        f_string = '3'
        result_x_eval, result_f_x = evaluate_function(
            f_string,
            lower=0,
            upper=1,
            steps=1001
        )
        result_x_div_eval, result_f_div_x = evaluate_div_function(
            f_string,
            lower=0,
            upper=1,
            steps=1001
        )
        result_x_int_eval, result_f_int_x = evaluate_int_function(
            (result_x_eval, result_f_x)
        )
        assert_allclose(result_x_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_x_div_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_x_int_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_x, expected_f_x, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_div_x, expected_f_div_x, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_int_x, expected_f_int_x, rtol=1e-5, atol=1e-5)

    def test_constant_float(self):
        '''Test when function is a constant float with derivative and integral'''
        expected_x_eval = np.linspace(-1, 2, 50)
        expected_f_x = 3e-2 * np.ones_like(expected_x_eval)
        expected_f_div_x = np.zeros_like(expected_x_eval)
        expected_f_int_x = 3e-2 * expected_x_eval
        expected_f_int_x -= expected_f_int_x[0]

        f_string = '3e-2'
        result_x_eval, result_f_x = evaluate_function(
            f_string,
            lower=-1,
            upper=2,
            steps=50
        )
        result_x_div_eval, result_f_div_x = evaluate_div_function(
            f_string,
            lower=-1,
            upper=2,
            steps=50
        )
        result_x_int_eval, result_f_int_x = evaluate_int_function(
            (result_x_eval, result_f_x)
        )
        assert_allclose(result_x_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_x_div_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_x_int_eval, expected_x_eval, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_x, expected_f_x, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_div_x, expected_f_div_x, rtol=1e-7, atol=1e-7)
        assert_allclose(result_f_int_x, expected_f_int_x, rtol=1e-7, atol=1e-7)

    def test_no_import(self):
        '''Test "import" attack'''
        f_string = 'import os; 3'
        with self.assertRaises(SyntaxError):
            evaluate_function(f_string)

    def test_no_load(self):
        '''Test "loadtxt" attack'''
        f_string = 'loadtxt("__init__.py"); 3'
        with self.assertRaises(SyntaxError):
            evaluate_function(f_string)

    def test_non_finite_function(self):
        '''Test function evaluation fails when it is not finite in middle of range'''
        f_string = '1 / (x - 0.5)'
        with self.assertRaises(ValueError):
            evaluate_function(f_string)
