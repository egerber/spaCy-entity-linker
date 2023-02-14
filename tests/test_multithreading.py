import unittest
import spacy
from multiprocessing.pool import ThreadPool


class TestMultiThreading(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestMultiThreading, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def test_is_multithread_safe(self):
        self.nlp.add_pipe("entityLinker", last=True)

        ents = [
            'Apple',
            'Microsoft',
            'Google',
            'Amazon',
            'Facebook',
            'IBM',
            'Twitter',
            'Tesla',
            'SpaceX',
            'Alphabet',
        ]
        text = "{} is looking at buying U.K. startup for $1 billion"

        def thread_func(i):
            doc = self.nlp(text.format(ents[i]))
            print(doc)

            for ent in doc.ents:
                print(ent.text, ent.label_, ent._.linkedEntities)
            return i

        with ThreadPool(10) as pool:
            for res in pool.imap_unordered(thread_func, range(10)):
                pass

        self.nlp.remove_pipe("entityLinker")
