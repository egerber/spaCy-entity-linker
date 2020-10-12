import unittest
import spacy
from spacyEntityLinker.EntityLinker import EntityLinker


class TestEntityLinker(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestEntityLinker, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def test_initialization(self):
        entityLinker = EntityLinker()

        self.nlp.add_pipe(entityLinker, last=True, name="entityLinker")

        doc = self.nlp(
            "Elon Musk was born in South Africa. Bill Gates and Steve Jobs come from in the United States")

        doc._.linkedEntities.pretty_print()
        doc._.linkedEntities.print_super_entities()
        for sent in doc.sents:
            sent._.linkedEntities.pretty_print()

        self.nlp.remove_pipe("entityLinker")
