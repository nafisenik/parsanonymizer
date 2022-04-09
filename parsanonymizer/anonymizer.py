from parsanonymizer.utils.normalizer import Normalizer
from parsanonymizer.utils.pattern_to_regex import Patterns
from parsanonymizer.utils.spans import create_spans
from parsanonymizer.utils.spans import merge_spans


class Model(object):
    def __init__(self):
        # Normalizer: convert arabic YE and KAF to persian ones.
        self.normalizer = Normalizer()
        # Patterns: patterns to regex generator
        self.patterns = Patterns()
        super(Model, self).__init__()

    def extract_span(self, text: str):

        # apply normalizer on input text
        text = self.normalizer.normalize(text)

        # Create spans
        spans = create_spans(self.patterns, text)
        spans = merge_spans(spans, text)

        return spans
