import unittest
import spacy
from spacy_entity_linker.EntityCollection import EntityCollection


class TestEntityCollection(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestEntityCollection, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def setUp(self):
        self.nlp.add_pipe("entityLinker", last=True)
        self.doc = self.nlp(
            "Elon Musk was born in South Africa. Bill Gates and Steve Jobs come from the United States")
        
    def tearDown(self):
        self.nlp.remove_pipe("entityLinker")

    def test_categories(self):
        doc = self.doc

        res = doc._.linkedEntities.get_distinct_categories()
        print(res)
        assert res != None
        assert len(res) > 0

        res = doc._.linkedEntities.grouped_by_super_entities()
        print(res)
        assert res != None
        assert len(res) > 0

    def test_printing(self):
        doc = self.doc

        # pretty print
        doc._.linkedEntities.pretty_print()

        # repr
        print(doc._.linkedEntities)

    def test_super_entities(self):
        doc = self.doc

        doc._.linkedEntities.print_super_entities()
        
    def test_iterable_indexable(self):
        doc = self.doc

        ents = list(doc._.linkedEntities)
        assert len(ents) > 0

        ent = doc._.linkedEntities[0]
        assert ent != None

        length = len(doc._.linkedEntities)
        assert length > 0