import unittest
from cron_translator import CronTranslator

class TestCronTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = CronTranslator()

    def test_translate(self):
        expression = '*/5 * * * *'
        result = self.translator.translate(expression)
        self.assertIn('cada minuto', result)

    def test_get_next_executions(self):
        expression = '*/5 * * * *'
        executions = self.translator.get_next_executions(expression, 3)
        self.assertEqual(len(executions), 3)

if __name__ == '__main__':
    unittest.main()