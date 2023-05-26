import unittest

from colorama import init, Fore

from index import Indexer
from bot import Bot
import warnings

# Initialize colorama
init()


def print_expected_actual(history, expected, actual):
    if isinstance(history, str):
        history = [history]
    print("------------------------------------------------------------")
    print(Fore.CYAN + "\n".join(history) + Fore.RESET)
    print(Fore.RED + f"Expected: {expected}" + Fore.RESET)
    print(Fore.GREEN + f"Actual: {actual}\n" + Fore.RESET)


class TestIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index: Indexer = Indexer()
        warnings.simplefilter('ignore', category=ResourceWarning)  # Ignores socket warnings on AI21 API

    @classmethod
    def tearDownClass(cls):
        warnings.resetwarnings()

    @unittest.skip
    def test_apis(self):
        request = "what specialized API's are offered by AI21?"
        context_str, verbose_str = self.index.get_context(request)
        print_expected_actual(request, '', context_str + '\n' + verbose_str)

    @unittest.skip
    def test_pricing(self):
        request = "What is the pricing for models?"
        context_str, verbose_str = self.index.get_context(request)
        print_expected_actual(request, '', context_str + '\n' + verbose_str)

    @unittest.skip
    def test_basic(self):
        request = "When was Jurassic-1 released?"
        context_str, verbose_str = self.index.get_context(request)
        print_expected_actual(request, '', context_str + '\n' + verbose_str)


class TestBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot: Bot = Bot()
        warnings.simplefilter('ignore', category=ResourceWarning)  # Ignores socket warnings on AI21 API

    @classmethod
    def tearDownClass(cls):
        warnings.resetwarnings()

    @unittest.skip
    def test_basic(self):
        history = ['User: Hello, how are you?']
        response, verbose_str = self.bot.generate_response(history)
        print_expected_actual(history, 'Great! How are you?', response + '\n' + verbose_str)

    @unittest.skip
    def test_basic_history(self):
        history = ['User: My name is John and I like cheese',
                   'AI21 Discord ChatBot: Hello, John',
                   'User: What did I say my name is and what do I like?']
        response, verbose_str = self.bot.generate_response(history)
        print_expected_actual(history, 'Your name is John and you like cheese.', response + '\n' + verbose_str)

    @unittest.skip
    def test_ignore_some_context(self):
        history = ['User: Who is Canada\'s favorite figure skating pair?',
                   'AI21 Discord ChatBot: Tessa Virtue and Scott Moir',
                   'User: Describe what Africa is like to visit',
                   'AI21 Discord ChatBot: Africa is a continent in the southern hemisphere. It is bordered by the Atlantic Ocean to the west, the Indian Ocean to the east, and the Mediterranean Sea to the north. It is the second largest continent in the world after Asia. Africa has a population of over 1 billion people and is home to some of the world\'s most diverse cultures and languages. The continent is also home to some of the world\'s most diverse wildlife, including elephants, lions, giraffes, zebras, and rhinos. Africa is also home to some of the world\'s most diverse landscapes, including the Sahara Desert, the Nile River, and the Congo River. Africa is also home to some of the world\'s most diverse climates, including the Sahara Desert, the Nile River, and the Congo River. Africa is also home to some of the world\'s most diverse cultures and languages. Africa is also home to some of the world\'s most diverse wildlife, including elephants, lions, giraffes, zebras, and rhinos.',
                   'User: When did they win the Olympics?']
        response, verbose_str = self.bot.generate_response(history)
        print_expected_actual(history,
                              'Tessa Virtue and Scott Moir won gold at the 2018 Winter Olympics in Pyeongchang, South Korea',
                              response + '\n' + verbose_str)

    def test_ai21(self):
        history = ["""User: How does the segmentation works? And what are the possible types?"""]
        response, verbose_str = self.bot.generate_response(history, verbose=True)
        print_expected_actual(history, 'J2-Large, J1-Jumbo etc... See links as well', response + '\n' + verbose_str)

    @unittest.skip
    def test_generate_code(self):
        history = ['User: Write me a python function that prints "Hello World"']
        response, verbose_str = self.bot.generate_response(history)
        print_expected_actual(history, 'def hello(): print("Hello world!")', response + '\n' + verbose_str)

    @unittest.skip
    def test_paraphrase(self):
        history = [
            "AI21 Discord ChatBot: Africa is a huge and diverse continent, with a wide range of cultures, natural landscapes, and travel experiences available. The continent has 54 countries, each with its own unique history, politics, and people."
            "If you're planning a trip to Africa, it's a good idea to research the specific countries or regions you're interested in visiting. Some African countries are highly developed, with thriving cities and modern infrastructure, while others are more rural and less developed."
            "In general, Africa is known for its rich culture and history, vibrant nightlife, stunning landscapes and wildlife, and its unique blend of traditional and modern cultures. Many African countries also offer opportunities for adventure travel and ecotourism, including safaris, hiking, and scuba diving."
            "Africa is also known for its friendly and welcoming people, as well as its delicious food and vibrant music, dance, and art cultures. No matter what you're interested in or what you're looking for in a travel experience, Africa has something to offer.",
            "User: Can you write a shorter description in 1-2 lines and focus on the culture"]
        response, verbose_str = self.bot.generate_response(history)
        print_expected_actual(history, '1-2 lines of Africa description with a focus on the culture...',
                              response + '\n' + verbose_str)

    @unittest.skip
    def test_long_form_generation(self):
        history = ["User: Write a short poem about the 'Paul is dead' conspiracy theory"]
        response, verbose_str = self.bot.generate_response(history)
        print_expected_actual(history, 'A poem about the Paul is dead conspiracy', response + '\n' + verbose_str)

    @unittest.skip
    def test_question_answering(self):
        history = ["User: What sort of questions can I expect at a Software Engineering job interview?"]
        response, verbose_str = self.bot.generate_response(history)
        print_expected_actual(history, 'Interview questions about a job interview', response + '\n' + verbose_str)

    @unittest.skip
    def test_verbose(self):
        history = ["User: What is the capital of Canada?"]
        response, verbose_str = self.bot.generate_response(history, verbose=True)
        print_expected_actual(history, 'Ottawa and model parameters', response + '\n' + verbose_str)
