import re
from typing import Dict
import numpy as np
from parstdex.utils import const


def merge_spans(spans: Dict, text: str):
    result, encoded = dict(), dict()

    encoded['personalname'] = encode_span(spans['personalname'],
                                  spans['adversarial'],
                                  text)

    encoded['personalname'] = encode_space(encoded['personalname'], spans['space'])
    result['personalname'] = find_spans(encoded['personalname'])

    return result


def create_spans(patterns, text):
    # add pattern keys to dictionaries and define a list structure for each key
    spans = {}
    for key in patterns.regexes.keys():
        spans[key]: list = []

    # apply regexes on normalized sentence and store extracted markers
    for key in patterns.regexes.keys():
        for regex_value in patterns.regexes[key]:
            # apply regex
            matches = list(
                re.finditer(
                    fr'\b(?:{regex_value})(?:\b|(?!{const.FA_SYM}|\d+))',
                    text)
            )
            # ignore empty markers
            if len(matches) > 0:
                # store extracted markers
                for match in matches:
                    start = match.regs[0][0]
                    end = match.regs[0][1]
                    spans[key].append((start, end))

    return spans


def encode_span(normal_spans, adv_spans, text):
    encoded_sent = np.zeros(len(text))

    for span in normal_spans:
        encoded_sent[span[0]: span[1]] = 1

    for span in adv_spans:
        encoded_sent[span[0]: span[1]] = 0

    return encoded_sent


def find_spans(encoded_sent):
    """
    Find spans in a given encoding
    :param encoded_sent: list
    :return: list[tuple]
    """
    spans = []
    i: int = 0
    len_sent = len(encoded_sent)

    while i < len_sent:
        # ignore if it starts with 0(nothing matched) or -1(space)
        if encoded_sent[i] <= 0:
            i += 1
            continue
        else:
            # it means it starts with 1
            start = i
            end = i + 1
            # continue if you see 1 or -1
            while i < len_sent and (encoded_sent[i] == 1 or encoded_sent[i] == -1):
                # store the last time you see 1
                if encoded_sent[i] == 1:
                    end = i + 1
                i += 1

            spans.append([start, end])
    return spans



def encode_space(encoded_sent, space_spans):
    """
    Encoded spaces to -1 in sentence encoding
    :param encoded_sent: list
    :param space_spans: list[tuple]
    :return: list
    """
    for span in space_spans:
        encoded_sent[span[0]: span[1]] = -1

    return encoded_sent


def sgn(num: int):
    if num >= 1:
        return 1
    elif num <= -1:
        return -1
    else:
        return 0


def merge_encodings(encoded_time, encoded_date):
    merged_encoding = [sgn(a+b) for a, b in zip(encoded_time, encoded_date)]
    return merged_encoding