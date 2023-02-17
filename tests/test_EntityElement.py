import unittest
import spacy


class TestEntityElement(unittest.TestCase):

    def __init__(self, arg, *args, **kwargs):
        super(TestEntityElement, self).__init__(arg, *args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def setUp(self):
        self.nlp.add_pipe("entityLinker", last=True)
        self.doc = self.nlp(
            "Elon Musk was born in South Africa. Bill Gates and Steve Jobs come from the United States. The US are located in North America. A ship is made of wood.")
        
    def tearDown(self):
        self.nlp.remove_pipe("entityLinker")

    def test_get_in_degree(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        in_degree = all_linked_entities[0].get_in_degree()
        assert in_degree > 0

    def test_get_original_alias(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        original_alias = all_linked_entities[0].get_original_alias()
        assert original_alias == "Elon Musk"

    def test_is_singleton(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        is_singleton = all_linked_entities[0].is_singleton()
        assert is_singleton == False
        is_singleton = all_linked_entities[-1].is_singleton()
        assert is_singleton == True

    def test_get_span(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        span = all_linked_entities[0].get_span()
        real_span = doc[0:2]
        assert span.text == real_span.text
        assert span.start == real_span.start
        assert span.end == real_span.end

    def test_get_label(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        label = all_linked_entities[0].get_label()
        assert label == "Elon Musk"

    def test_get_id(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        id = all_linked_entities[0].get_id()
        assert id > 0

    def test_get_prior(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        prior = all_linked_entities[0].get_prior()
        assert prior > 0

    def test_get_chain(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        chain = all_linked_entities[0].get_chain()
        assert chain != None
        assert len(chain) > 0

    def test_get_categories(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        categories = all_linked_entities[0].get_categories()
        assert categories != None
        assert len(categories) > 0

    def test_get_sub_entities(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        # [-1] --> wood
        sub_entities = all_linked_entities[-1].get_sub_entities()
        assert sub_entities != None
        assert len(sub_entities) > 0

    def test_get_super_entities(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        super_entities = all_linked_entities[0].get_super_entities()
        assert super_entities != None
        assert len(super_entities) > 0

    def test_get_subclass_hierarchy(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        # [5] --> US
        hierarchy = all_linked_entities[5].get_subclass_hierarchy()
        assert hierarchy != None
        assert len(hierarchy) > 0
        assert 'country' in hierarchy

    def test_get_instance_of_hierarchy(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        # [5] --> US
        hierarchy = all_linked_entities[5].get_instance_of_hierarchy()
        assert hierarchy != None
        assert len(hierarchy) > 0
        assert 'country' in hierarchy

    def test_get_chain_ids(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        chain_ids = all_linked_entities[0].get_chain_ids()
        assert chain_ids != None
        assert len(chain_ids) > 0
    
    def test_get_description(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        description = all_linked_entities[0].get_description()
        assert description != None
        assert len(description) > 0

    def test_is_intersecting(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        assert not all_linked_entities[0].is_intersecting(all_linked_entities[1])
        # United States and US
        assert all_linked_entities[4].is_intersecting(all_linked_entities[5])

    def test_serialize(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        serialized = all_linked_entities[0].serialize()
        assert serialized != None
        assert len(serialized) > 0
        assert 'id' in serialized
        assert 'label' in serialized
        assert 'span' in serialized

    def test_pretty_print(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        all_linked_entities[0].pretty_print()
    
    def test_get_url(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        url = all_linked_entities[0].get_url()
        assert url != None
        assert len(url) > 0
        assert 'wikidata.org/wiki/Q' in url

    def test___repr__(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        repr = all_linked_entities[0].__repr__()
        assert repr != None
        assert len(repr) > 0

    def test___eq__(self):
        doc = self.doc

        all_linked_entities = doc._.linkedEntities
        assert not all_linked_entities[0] == all_linked_entities[1]
        assert all_linked_entities[4] == all_linked_entities[5]
