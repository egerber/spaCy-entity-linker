from .TermCandidate import TermCandidate


class TermCandidateExtractor:
    def __init__(self, doc):
        self.doc = doc

    def __iter__(self):
        for sent in self.doc.sents:
            for candidate in self._get_candidates_in_sent(sent, self.doc):
                yield candidate

    def _get_candidates_in_sent(self, sent, doc):
        root = list(filter(lambda token: token.dep_ == "ROOT", sent))[0]

        excluded_children = []
        candidates = []

        def get_candidates(node, doc):

            if (node.pos_ in ["PROPN", "NOUN"]) and node.pos_ not in ["PRON"]:
                term_candidates = TermCandidate(doc[node.i:node.i + 1])

                for child in node.children:

                    start_index = min(node.i, child.i)
                    end_index = max(node.i, child.i)

                    if child.dep_ == "compound" or child.dep_ == "amod":
                        subtree_tokens = list(child.subtree)
                        if all([c.dep_ == "compound" for c in subtree_tokens]):
                            start_index = min([c.i for c in subtree_tokens])
                        term_candidates.append(doc[start_index:end_index + 1])

                        if not child.dep_ == "amod":
                            term_candidates.append(doc[start_index:start_index + 1])
                        excluded_children.append(child)

                    if child.dep_ == "prep" and child.text == "of":
                        end_index = max([c.i for c in child.subtree])
                        term_candidates.append(doc[start_index:end_index + 1])

                candidates.append(term_candidates)

            for child in node.children:
                if child in excluded_children:
                    continue
                get_candidates(child, doc)

        get_candidates(root, doc)

        return candidates
