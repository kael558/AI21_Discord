import unittest

from colorama import init, Fore

from bot import Bot

# Initialize colorama
init()


class TestScraper(unittest.TestCase):
    pass


def print_expected_actual(history, expected, actual):
    print(Fore.CYAN + "\n".join(history) + Fore.RESET)
    print(Fore.RED + f"\nExpected: {expected}" + Fore.RESET)
    print(Fore.GREEN + f"Actual: {actual}\n" + Fore.RESET)


class TestBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot: Bot = Bot()
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)

    def test_basic(self):
        history = ['User: Hello, how are you?']
        response = self.bot.generate_response(history)
        print_expected_actual(history, 'Great! How are you?', response)

    def test_basic_history(self):
        history = ['User: My name is John and I like cheese',
                   'AI21 Discord Bot: Hello, John',
                   'User: What did I say my name is and what do I like?']
        response = self.bot.generate_response(history)
        print_expected_actual(history, 'Your name is John and you like cheese.', response)

    def test_ignore_some_context(self):
        history = ['User: Who is Canada\'s favorite figure skating pair?',
                   'AI21 Discord Bot: Tessa Virtue and Scott Moir',
                   'User: Describe what Africa is like to visit',
                   'AI21 Discord Bot: Africa is a continent in the southern hemisphere. It is bordered by the Atlantic Ocean to the west, the Indian Ocean to the east, and the Mediterranean Sea to the north. It is the second largest continent in the world after Asia. Africa has a population of over 1 billion people and is home to some of the world\'s most diverse cultures and languages. The continent is also home to some of the world\'s most diverse wildlife, including elephants, lions, giraffes, zebras, and rhinos. Africa is also home to some of the world\'s most diverse landscapes, including the Sahara Desert, the Nile River, and the Congo River. Africa is also home to some of the world\'s most diverse climates, including the Sahara Desert, the Nile River, and the Congo River. Africa is also home to some of the world\'s most diverse cultures and languages. Africa is also home to some of the world\'s most diverse wildlife, including elephants, lions, giraffes, zebras, and rhinos.',
                   'User: When did they win the Olympics?']
        response = self.bot.generate_response(history)
        print_expected_actual(history,
                              'Tessa Virtue and Scott Moir won gold at the 2018 Winter Olympics in Pyeongchang, South Korea',
                              response)

    def test_ai21(self):
        history = ['User: What foundation models are offered by AI21?']
        response = self.bot.generate_response(history, verbose=True)
        print_expected_actual(history, 'J2-Large, J1-Jumbo etc... See links as well', response)

    def test_generate_code(self):
        history = ['User: Write me a python function that prints "Hello World"']
        response = self.bot.generate_response(history, verbose=True)
        print_expected_actual(history, 'def hello(): print("Hello world!")', response)

    def test_paraphrase(self):
        pass

    def test_long_form_generation(self):
        pass

    def test_question_answering(self):
        pass


if __name__ == '__main__':
    unittest.main()
