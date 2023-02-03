import unittest
import spacy
from spacy_entity_linker.EntityLinker import EntityLinker


class TestEntityLinker(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestEntityLinker, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def test_initialization(self):

        self.nlp.add_pipe("entityLinker", last=True)

        doc = self.nlp(
            "Elon Musk was born in South Africa. Bill Gates and Steve Jobs come from in the United States")

        doc._.linkedEntities.pretty_print()
        doc._.linkedEntities.print_super_entities()
        for sent in doc.sents:
            sent._.linkedEntities.pretty_print()

        self.nlp.remove_pipe("entityLinker")

    def test_empty_root(self):
        # test empty lists of roots (#9)
        self.nlp.add_pipe("entityLinker", last=True)

        doc = self.nlp(
            'I was right."\n\n     "To that extent."\n\n     "But that was all."\n\n     "No, no, m')
        for sent in doc.sents:
            sent._.linkedEntities.pretty_print()
        # empty document
        doc = self.nlp('\n\n')
        for sent in doc.sents:
            sent._.linkedEntities.pretty_print()

        self.nlp.remove_pipe("entityLinker")
