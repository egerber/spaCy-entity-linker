from spacyEntityLinker.EntityClassifier import EntityClassifier
from spacyEntityLinker.EntityCollection import EntityCollection
from spacyEntityLinker.TermCandidateExtractor import TermCandidateExtractor
from spacy.tokens import Doc, Span


class EntityLinker:

    def __init__(self):
        Doc.set_extension("linkedEntities", default=EntityCollection(), force=True)
        Span.set_extension("linkedEntities", default=None, force=True)

    def __call__(self, doc):
        tce = TermCandidateExtractor(doc)
        classifier = EntityClassifier()

        for sent in doc.sents:
            sent._.linkedEntities = EntityCollection([])

        entities = []
        for termCandidates in tce:
            entityCandidates = termCandidates.get_entity_candidates()
            if len(entityCandidates) > 0:
                entity = classifier(entityCandidates)
                entity.span.sent._.linkedEntities.append(entity)
                entities.append(entity)

        doc._.linkedEntities = EntityCollection(entities)

        return doc
