import unittest
import spacy
import spacyEntityLinker.TermCandidateExtractor


class TestCandidateExtractor(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestCandidateExtractor, self).__init__(arg, *args, **kwargs)
