# tests/test_core.py
import unittest
from codingnow.core import hello_world

class TestCore(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(hello_world(), "Hello, CodingNow!")