import unittest
from src.petljapub.messages import set_language, msg

class TestMessages(unittest.TestCase):
    def test_msg(self):
        set_language("en")
        self.assertEqual(msg("TASK"), "Task")
        set_language("sr")
        self.assertEqual(msg("TASK"), "Zadatak")
        set_language("sr-Cyrl")        
        self.assertEqual(msg("TASK"), "Задатак")
        
        self.assertEqual(msg("TASK", "en"), "Task")
