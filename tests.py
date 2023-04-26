import unittest
from bot import Bot

class TestScraper(unittest.TestCase):
    pass


class TestBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = Bot()

    @classmethod
    def tearDownClass(cls):
        # Clean up resources used by all the tests in the class
        cls.bot.stop()
        cls.bot = None

    def test_basic(self):
        history = ['User: Hello, how are you?']
        response = self.bot.generate_response(history)
        print(response)

    def test_basic_history(self):
        history = ['hello']
        response = self.bot.generate_response(history)
        print(response)

    def test_ignore_some_context(self):
        history = ['hello']
        response = self.bot.generate_response(history)
        print(response)

    @unittest.skip("Not implemented")
    def test_ai21(self):
        history = ['hello']
        response = self.bot.generate_response(history)
        print(response)

    def test_generate_code(self):
        pass

    def test_paraphrase(self):
        pass

    def test_long_form_generation(self):
        pass

    def test_question_answering(self):
        pass

if __name__ == '__main__':
    unittest.main()