"""
SpanInfo class
Stores the info of spacy.tokens.Span (start, end and text of a span) by making it serializable
"""

import spacy
import srsly

class SpanInfo:

    @staticmethod
    def from_span(span: spacy.tokens.Span):
        return SpanInfo(span.start, span.end, span.text)
    
    def __init__(self, start: int, end: int, text: str):
        self.start = start
        self.end = end
        self.text = text


    def __repr__(self) -> str:
        return self.text
    
    def __len__(self):
        return self.end - self.start
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, SpanInfo) or isinstance(__o, spacy.tokens.Span):
            return self.start == __o.start and self.end == __o.end and self.text == __o.text
        return False
    
    def get_span(self, doc: spacy.tokens.Doc):
        """
        Returns the real spacy.tokens.Span of the doc from the stored info"""
        return doc[self.start:self.end]


@srsly.msgpack_encoders("SpanInfo")
def serialize_spaninfo(obj, chain=None):
    if isinstance(obj, SpanInfo):
        result = {
            "start": obj.start,
            "end": obj.end,
            "text": obj.text,
        }
        return result
    # otherwise return the original object so another serializer can handle it
    return obj if chain is None else chain(obj)

@srsly.msgpack_decoders("SpanInfo")
def deserialize_spaninfo(obj, chain=None):
    if "start" in obj:
        return SpanInfo(obj['start'], obj['end'], obj['text'])
    # otherwise return the original object so another serializer can handle it
    return obj if chain is None else chain(obj)