import unittest
import spacy
from multiprocessing.pool import ThreadPool


class TestPipe(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestPipe, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def test_serialize(self):
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

        texts = [text.format(ent) for ent in ents]
        docs = self.nlp.pipe(texts, n_process=2)
        for doc in docs:
            print(doc)
            for ent in doc.ents:
                print(ent.text, ent.label_, ent._.linkedEntities)


        self.nlp.remove_pipe("entityLinker")
