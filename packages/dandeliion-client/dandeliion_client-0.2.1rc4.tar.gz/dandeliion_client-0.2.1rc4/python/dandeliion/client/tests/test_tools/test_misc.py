from unittest import TestCase
from copy import deepcopy

from dandeliion.client.tools.misc import (
    update_dict,
    get_dict,
    flatten_dict,
    unflatten_dict,
)


class Dict_TestCase(TestCase):

    def test_update_dict(self):
        '''Test updating nested dicts'''

        input_dict = {'A': 1, 'B': {'BA': 'apple', 'BB': 3, 'BC': {'BCA': 4}}, 'C': 5}
        updates = {'A': 6, 'B': {'BA': 'orange', 'BC': 8}}
        expected_dict = {'A': 6, 'B': {'BA': 'orange', 'BB': 3, 'BC': 8}, 'C': 5}

        # with defaults i.e. inline
        updated_dict = deepcopy(input_dict)
        update_dict(updated_dict, updates)
        self.assertDictEqual(updated_dict, expected_dict)

        # without inline
        updated_dict = update_dict(input_dict, updates, inline=False)
        self.assertDictEqual(updated_dict, expected_dict)

        # with None (should change nothing)
        updated_dict = update_dict(input_dict, None, inline=False)
        self.assertDictEqual(updated_dict, input_dict)

    def test_get_dict(self):
        '''Test accessing nested dicts'''

        input_dict = {'A': 1, 'B': {'BA': 'apple', 'BB': 3, 'BC': {'BCA': 4}}, 'C': 5}

        # first with defaults
        self.assertEqual(5, get_dict(input_dict, 'C'))
        self.assertDictEqual(input_dict['B'], get_dict(input_dict, 'B'))
        self.assertEqual('apple', get_dict(input_dict, 'B', 'BA'))
        self.assertEqual(4, get_dict(input_dict, 'B', 'BC', 'BCA'))

        # with custom default
        self.assertEqual(1, get_dict(input_dict, 'A', default='something'))
        self.assertEqual('something', get_dict(input_dict, 'D', default='something'))

    def test_flatten_dict(self):
        '''Test flattening nested dicts'''

        input_dict = {'A': 1, 'B': {'BA': 'apple', 'BB': 3, 'BC': {'BCA': 4}}, 'C': 5}

        # first with defaults
        expected_dict = {'A': 1, 'B.BA': 'apple', 'B.BB': 3, 'B.BC.BCA': 4, 'C': 5}
        self.assertDictEqual(flatten_dict(input_dict), expected_dict)

        # first with custom sep
        expected_dict = {'A': 1, 'B-BA': 'apple', 'B-BB': 3, 'B-BC-BCA': 4, 'C': 5}
        self.assertDictEqual(flatten_dict(input_dict, sep='-'), expected_dict)

    def test_unflatten_dict(self):
        '''Test unflattening nested dicts'''

        expected_dict = {'A': 1, 'B': {'BA': 'apple', 'BB': 3, 'BC': {'BCA': 4}}, 'C': 5}

        # first with defaults
        input_dict = {'A': 1, 'B.BA': 'apple', 'B.BB': 3, 'B.BC.BCA': 4, 'C': 5}
        self.assertDictEqual(unflatten_dict(input_dict), expected_dict)

        # first with custom sep
        input_dict = {'A': 1, 'B-BA': 'apple', 'B-BB': 3, 'B-BC-BCA': 4, 'C': 5}
        self.assertDictEqual(unflatten_dict(input_dict, sep='-'), expected_dict)
