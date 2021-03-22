import unittest

from Algorithms.RandomChoice import RandomChoice
from Algorithms.RotateForever import RotateForever


class TestAlgorithms(unittest.TestCase):
    class FieldTest(unittest.TestCase):
        def setUp(self) -> None:
            pass

        def tearDown(self) -> None:
            pass

    def test_random_instantiation(self):
        alg = RandomChoice()
        self.assertIsNotNone(alg)

    def test_rotate_instantiation(self):
        alg = RotateForever()
        self.assertIsNotNone(alg)

