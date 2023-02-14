import unittest
import spacy
from multiprocessing.pool import ThreadPool


class TestSerialize(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestSerialize, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def test_serialize(self):
        self.nlp.add_pipe("entityLinker", last=True)

        text = "Apple is looking at buying U.K. startup for $1 billion"
        doc = self.nlp(text)
        serialised = doc.to_bytes()

        doc2 = spacy.tokens.Doc(doc.vocab).from_bytes(serialised)
        for ent, ent2 in zip(doc.ents, doc2.ents):
            assert ent.text == ent2.text
            assert ent.label_ == ent2.label_
            linked = ent._.linkedEntities
            linked2 = ent2._.linkedEntities
            if linked:
                assert linked.get_description() == linked2.get_description()
                assert linked.get_id() == linked2.get_id()
                assert linked.get_label() == linked2.get_label()
                assert linked.get_span() == linked2.get_span()
                assert linked.get_url() == linked2.get_url()


        self.nlp.remove_pipe("entityLinker")
