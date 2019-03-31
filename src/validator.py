# -*- coding: utf-8 -*-
"""Validation logic."""

import string

import spacy
from spacy.tokenizer import Tokenizer


nlp = spacy.load("en_core_web_sm")


def validate_text(latest_text, proposed_text, valid_strings=None):

    if valid_strings:
        for valid_string in valid_strings:
            if valid_string in proposed_text:
                return True

    if latest_text:
        required_string = get_required_string(latest_text)
        return required_string in proposed_text
    else:
        return False


def get_required_string(text):
    """Gets the last noun phrase or word in some text."""
    if text:
        document = nlp(text)

        # Attempt to get a noun phrase
        noun_phrases = list(document.noun_chunks)
        if noun_phrases:
            return str(noun_phrases[-1])

        # Attempt to get a word
        tokenizer = Tokenizer(nlp.vocab)
        punctuation_dict = {
            ord(char): None
            for char in string.punctuation.replace('\'', '')
        }
        words = [
            str(word).translate(punctuation_dict) for word in tokenizer(text)
            if str(word).lower() not in nlp.Defaults.stop_words
        ]
        return words[-1] if words else None
