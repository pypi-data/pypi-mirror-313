import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prompts.system_prompt import get_system_prompt
openai_api_key = os.getenv("OPENAI_API_KEY")


class TestSystemPrompt(unittest.TestCase):

	def test_system_prompt(self):
		self.assertTrue(get_system_prompt("You are data analyst", "By analysis of the data", "Give me insinghts to take decision", openai_api_key))
if __name__ == '__main__': 
      unittest.main()