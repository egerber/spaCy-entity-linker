from itertools import groupby
import numpy as np


class EntityClassifier:
    def __init__(self):
        pass

    def _get_grouped_by_length(self, entities):
        sorted_by_len = sorted(entities, key=lambda entity: len(entity.get_span()), reverse=True)

        entities_by_length = {}
        for length, group in groupby(sorted_by_len, lambda entity: len(entity.get_span())):
            entities = list(group)
            entities_by_length[length] = entities

        return entities_by_length

    def _filter_max_length(self, entities):
        entities_by_length = self._get_grouped_by_length(entities)
        max_length = max(list(entities_by_length.keys()))

        return entities_by_length[max_length]

    def _select_max_prior(self, entities):
        priors = [entity.get_prior() for entity in entities]
        return entities[np.argmax(priors)]

    def _get_casing_difference(self, word1, original):
        difference = 0
        for w1, w2 in zip(word1, original):
            if w1 != w2:
                difference += 1

        return difference

    def _filter_most_similar(self, entities):
        similarities = np.array(
            [self._get_casing_difference(entity.get_span().text, entity.get_original_alias()) for entity in entities])

        min_indices = np.where(similarities == similarities.min())[0].tolist()

        return [entities[i] for i in min_indices]

    def __call__(self, entities):
        filtered_by_length = self._filter_max_length(entities)
        filtered_by_casing = self._filter_most_similar(filtered_by_length)

        return self._select_max_prior(filtered_by_casing)
