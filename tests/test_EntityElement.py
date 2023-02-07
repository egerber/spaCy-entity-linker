import unittest
import spacy
from spacy_entity_linker.EntityLinker import EntityLinker


class TestEntityElement(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestEntityElement, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def test_is_intersecting(self):

        self.nlp.add_pipe("entityLinker", last=True)

        doc = self.nlp(
            "Elon Musk was born in South Africa. Bill Gates and Steve Jobs come from in the United States")

        all_linked_entities = doc._.linkedEntities
        # trivial test, only to test if this throws an error
        assert not all_linked_entities[0].is_intersecting(all_linked_entities[1])

        self.nlp.remove_pipe("entityLinker")
