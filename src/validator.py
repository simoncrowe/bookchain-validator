# -*- coding: utf-8 -*-
"""Validation logic."""

import random
import string

import spacy
from spacy.tokenizer import Tokenizer


nlp = spacy.load("en_core_web_sm")


def validate_text(latest_text, proposed_text, valid_strings=None):

    if valid_strings:
        for valid_string in valid_strings:
            if valid_string in proposed_text:
                return True

    required_string = get_required_string(latest_text)
    return required_string in proposed_text


def get_required_string(text):
    """Gets the last noun phrase or word in some text."""
    document = nlp(text)

    # Attempt to get a noun phrase
    last_noun_phrase = list(document.noun_chunks)[-1]
    if last_noun_phrase:
        return last_noun_phrase

    # Attempt to get a word
    tokenizer = Tokenizer(nlp.vocab)
    words = [
        token for token in tokenizer(text)
        if token not in nlp.Defaults.stop_words
    ]
    return words[-1]
