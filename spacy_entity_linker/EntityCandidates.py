class EntityCandidates:

    def __init__(self, entity_elements):
        self.entity_elements = entity_elements

    def __iter__(self):
        for entity in self.entity_elements:
            yield entity

    def __len__(self):
        return len(self.entity_elements)

    def __getitem__(self, item):
        return self.entity_elements[item]

    def pretty_print(self):
        for entity in self.entity_elements:
            entity.pretty_print()

    def __str__(self):
        return str(["entity {}: {} (<{}>)".format(i, entity.get_label(), entity.get_description()) for i, entity in
                    enumerate(self.entity_elements)])
