from .DatabaseConnection import get_wikidata_instance
from .EntityCollection import EntityCollection


class EntityElement:
    def __init__(self, row, span):
        self.identifier = row[0]
        self.prior = 0
        self.original_alias = None
        self.in_degree = None

        if len(row) > 1:
            self.label = row[1]
        if len(row) > 2:
            self.description = row[2]
        if len(row) > 3 and row[3]:
            self.prior = row[3]
        if len(row) > 4 and row[4]:
            self.in_degree = row[4]
        if len(row) > 5 and row[5]:
            self.original_alias = row[5]

        self.url="https://www.wikidata.org/wiki/Q{}".format(self.get_id())
        self.span = span

        self.chain = None
        self.chain_ids = None

        self.wikidata_instance = get_wikidata_instance()

    def get_in_degree(self):
        return self.in_degree

    def get_original_alias(self):
        return self.original_alias

    def is_singleton(self):
        return len(self.get_chain()) == 0

    def get_span(self):
        return self.span

    def get_label(self):
        return self.label

    def get_id(self):
        return self.identifier

    def get_prior(self):
        return self.prior

    def get_chain(self):
        if self.chain is None:
            self.chain = self.wikidata_instance.get_chain(self.identifier, max_depth=10, property=31)
        return self.chain

    def is_category(self):
        pass

    def is_leaf(self):
        pass

    def get_categories(self, max_depth=10):
        return self.wikidata_instance.get_categories(self.identifier, max_depth=max_depth)

    def get_sub_entities(self, limit=10):
        return EntityCollection(
            [EntityElement(row, None) for row in self.wikidata_instance.get_children(self.get_id(), limit)])

    def get_super_entities(self, limit=10):
        return EntityCollection(
            [EntityElement(row, None) for row in self.wikidata_instance.get_parents(self.get_id(), limit)])

    def get_subclass_hierarchy(self):
        chain = self.wikidata_instance.get_chain(self.identifier, max_depth=5, property=279)
        return [self.wikidata_instance.get_entity_name(el[0]) for el in chain]

    def get_instance_of_hierarchy(self):
        chain = self.wikidata_instance.get_chain(self.identifier, max_depth=5, property=31)
        return [self.wikidata_instance.get_entity_name(el[0]) for el in chain]

    def get_chain_ids(self, max_depth=10):
        if self.chain_ids is None:
            self.chain_ids = set([el[0] for el in self.get_chain(max_depth=max_depth)])

        return self.chain_ids

    def get_description(self):
        if self.description:
            return self.description
        else:
            return ""

    def is_intersecting(self, other_element):
        return len(self.get_chain_ids().intersection(other_element.get_chain_ids())) > 0

    def serialize(self):
        return {
            "id": self.get_id(),
            "label": self.get_label(),
            "span": self.get_span()
        }

    def pretty_print(self):
        print(self.__repr__())
    
    def get_url(self):
        return self.url

    def __repr__(self):
        return "<EntityElement: {}>".format(self.get_preview_string())

    def get_preview_string(self):
        return "{0:<10} {1:<25} {2:<50}".format(self.get_url(),self.get_label(),self.get_description()[:100])

    def pretty_string(self, description=False):
        if description:
            return ','.join([span.text for span in self.span]) + "  => {} <{}>".format(self.get_label(),
                                                                                       self.get_description())
        else:
            return ','.join([span.text for span in self.span]) + "  => {}".format(self.get_label())

    def save(self, category):
        for span in self.span:
            span.sent._.linked_entities.append(
                {"id": self.identifier, "range": [span.start, span.end + 1], "category": category})

    def __str__(self):
        label = self.get_label()
        if label:
            return label
        else:
            return ""

    def __eq__(self, other):
        return isinstance(other, EntityElement) and other.get_id() == self.get_id()
