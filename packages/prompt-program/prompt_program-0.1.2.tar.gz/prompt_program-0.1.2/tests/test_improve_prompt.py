import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prompts.improve_prompt import get_improved_prompt


class TestSystemPrompt(unittest.TestCase):

	def test_system_prompt(self):
		self.assertTrue(get_improved_prompt("List places to visit in Japan."))
if __name__ == '__main__': 
      unittest.main()