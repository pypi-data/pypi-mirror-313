from melting_schemas.utils import wrap

from .text_encoding import RawTextEncodingRequest


def raw_text_encoding_examples():
    minimal = RawTextEncodingRequest(
        model="sentence-transformers/all-MiniLM-L6-v2",
        snippets=["I like to eat apples."],
    )
    return [wrap(name="Minimal", value=minimal)]
