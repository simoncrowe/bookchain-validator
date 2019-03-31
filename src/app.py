#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides validation API for bookchain JS."""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from webargs import fields
from webargs.flaskparser import use_kwargs

from validator import validate_text, get_required_string

app = Flask(__name__)
# TODO: implement narrower CORS headers
CORS(app)
app.config.from_pyfile('settings.cfg')


@app.route('/greeting', methods=['post'])
@use_kwargs(
    {
        'latest_block_text': fields.Str(missing=None),
    }
)
def message(latest_block_text):
    required_string = get_required_string(latest_block_text)
    if required_string:
        return jsonify(
            render_template_string(
                source=app.config['GREETING_TEMPLATE_WITH_REQUIRED_STRING'],
                required_string=required_string
            )
        )
    else:
        return jsonify(app.config['GREETING_NO_REQUIRED_STRING'])


@app.route('/validate', methods=['post'])
@use_kwargs(
    {
        'proposed_block_text': fields.Str(required=True, allow_none=False),
        'latest_block_text': fields.Str(missing=None),
    }
)
def validate(proposed_block_text, latest_block_text):
    valid = validate_text(
        latest_text=latest_block_text,
        proposed_text=proposed_block_text,
        valid_strings=app.config['VALID_STRINGS']
    )
    if valid:
        return jsonify(
            {
                'valid': True,
                'message': app.config['PROPOSAL_VALID_MESSAGE'],
            }
        )
    else:
        return jsonify(
            {
                'valid': False,
                'message': app.config['PROPOSAL_INVALID_MESSAGE']
            }
        )


if __name__ == '__main__':
    app.run(port=8008)
