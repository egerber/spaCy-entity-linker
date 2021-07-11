MAX_ITEMS_PREVIEW=20

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

    def __repr__(self) -> str:
        preview_str=""
        for index,entity_element in enumerate(self):
            if index>MAX_ITEMS_PREVIEW:
                break
            preview_str+="{}\n".format(entity_element.get_preview_string())
        
        return preview_str

    def __str__(self):
        return str(["entity {}: {} (<{}>)".format(i, entity.get_label(), entity.get_description()) for i, entity in
                    enumerate(self.entity_elements)])
