import regex as re
import os
from parsanonymizer.utils import const



def process_file(path):
    with open(path, 'r', encoding='utf-8-sig') as file:
        text = file.readlines()
        text = [x.strip() for x in text if not x.startswith('#') and len(x.strip()) > 0]  # remove \n
        return text



class Annotation:
    """
    Annotation class is used to create annotation dictionary which will be used for creating regex from patterns
    in following steps.
    """

    annotation_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'annotation')
    annotations_dict = {}
    
    def __init__(self):
        # regex_annotations
        regex_annotations = self.create_regex_annotation_dict()
        # time annotation dictionary includes all annotations of time folder
        main_annotations = self.create_annotation_dict(self.annotation_path)


        self.annotations_dict = {**regex_annotations,
                                 **main_annotations}




    @staticmethod
    def create_annotation(path):
        text = process_file(path)
        annotation_mark = "|".join(text)
        return annotation_mark

    @staticmethod
    def create_regex_annotation_dict():
        annotation_dict = {
            'NUM10': r'\\d{10}', 
            'NUMR10': r'[0-9]{10}',
            'PASSNO': r'[A-Z][0-9]{8}',
            'FMPF': fr'(\\u200c)?[{const.FA_ALPHABET}]+[^\\s]',
            'EMAIL': r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",
            'URL': r"""((http|ftp|https):\\/\\/)?([\\w_-]+(?:(?:\\.[\\w_-]+)+))([\\w.,@?^=%&:\\/~+#-]*[\\w@?^=%&\\/~+#-])""",
            'PHONENUMBER': r"""(((([+]|00)98)[-\\s]?)|0)?9\\d{2}[-\\s]?\\d{3}[-\\s]?\\d{2}[-\\s]?\\d{2}(?!\\d)""",
            'CARDNUM': r'(\\d{2})(-|_|\\s{1,3})?(\\d{4})(-|_|\\s{1,3})?(\\d{4})',
            'ONE_W': r"""(\\w)+[^\\s]""",
            'ALL_W':r'(.)*'

        }

        return annotation_dict

    def create_annotation_dict(self, annotation_path):
        """
        create_annotation_dict will read all annotation text files in utilities/annotations folder and
        create corresponding regex for the annotation folder
        :return: dict
        """
        annotation_dict = {}
        files = os.listdir(annotation_path)
        for f in files:
            key = f.replace('.txt', '')
            annotation_dict[key] = self.create_annotation(f"{annotation_path}/{f}")

        return annotation_dict


class Patterns:
    """
    Patterns class is used to create regexes corresponding to patterns defined in utilities/pattern folder.
    """
    regexes = {}
    cumulative_annotations = {}
    cumulative_annotations_keys = []

    def __init__(self):
        annotations = Annotation()
        self.patterns_path = os.path.join(os.path.dirname(__file__), 'pattern', "")
        self.cumulative_annotations = annotations.annotations_dict
        self.cumulative_annotations_keys = sorted(self.cumulative_annotations, key=len, reverse=True)
        files = os.listdir(self.patterns_path)
        for f in files:
            self.regexes[f.replace('.txt', '').lower()] = self.create_regexes_from_patterns(f"{self.patterns_path}/{f}")

        self.regexes['space'] = [rf"\u200c+", rf"\s+"]

    def pattern_to_regex(self, pattern):
        """
        pattern_to_regex takes pattern and return corresponding regex
        :param pattern: str
        :return: str
        """
        pattern = pattern.replace(" ", r'[\u200c\s]{1,3}')
        annotation_keys = "|".join(self.cumulative_annotations_keys)
        matches = re.findall(annotation_keys, pattern)
        for key in matches:
            pattern = re.sub(f'{key}', fr"(?:{self.cumulative_annotations[key]})", pattern)

        pattern = pattern.replace("<>", r'(?:[\s\u200c])*')
        return pattern

    def create_regexes_from_patterns(self, path):
        """
        create_regexes_from_patterns takes path of pattern folder and return list of regexes corresponding to
        pattern folder.
        :param path: str
        :return: list
        """
        patterns = process_file(path)
        regexes = [self.pattern_to_regex(pattern) for pattern in patterns]
        return regexes
