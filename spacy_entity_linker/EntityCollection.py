from collections import Counter, defaultdict
from .DatabaseConnection import get_wikidata_instance

MAX_ITEMS_PREVIEW=20


class EntityCollection:

    def __init__(self, entities=[]):
        self.entities = entities

    def __iter__(self):
        for entity in self.entities:
            yield entity

    def __getitem__(self, item):
        return self.entities[item]

    def __len__(self):
        return len(self.entities)

    def append(self, entity):
        self.entities.append(entity)

    def get_categories(self, max_depth=1):
        categories = []
        for entity in self.entities:
            categories += entity.get_categories(max_depth)

        return categories

    def print_super_entities(self, max_depth=1, limit=10):
        wikidataInstance = get_wikidata_instance()

        all_categories = []
        category_to_entites = defaultdict(list)

        for e in self.entities:
            for category in e.get_categories(max_depth):
                category_to_entites[category].append(e)
                all_categories.append(category)

        counter = Counter()
        counter.update(all_categories)

        for category, frequency in counter.most_common(limit):
            print("{} ({}) : {}".format(wikidataInstance.get_entity_name(category), frequency,
                                        ','.join([str(e) for e in category_to_entites[category]])))

    def __repr__(self) -> str:
        preview_str="<EntityCollection ({} entities):".format(len(self))
        for index,entity_element in enumerate(self):
            if index>MAX_ITEMS_PREVIEW:
                preview_str+="\n...{} more".format(len(self)-MAX_ITEMS_PREVIEW)
                break
            preview_str+="\n-{}".format(entity_element.get_preview_string())
        
        preview_str+=">"
        return preview_str

    def pretty_print(self):
        for entity in self.entities:
            entity.pretty_print()

    def grouped_by_super_entities(self, max_depth=1):
        counter = Counter()
        counter.update(self.get_categories(max_depth))

        return counter

    def get_distinct_categories(self, max_depth=1):
        return list(set(self.get_categories(max_depth)))
