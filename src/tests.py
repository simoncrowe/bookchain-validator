#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick and dirty "unit" tests for API. Too complex but do the job."""

from multiprocessing import Process
import unittest
import time

import requests

from app import app


class CallLocalApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_server = Process(target=app.run)
        cls.test_server.start()
        # Wait for the test server to start
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.test_server.terminate()
        cls.test_server.join()

    def test_greeting_without_latest_text(self):
        response = requests.post('http://127.0.0.1:5000/greeting')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            app.config['GREETING_NO_REQUIRED_STRING']
        )

    def test_greeting_with_latest_block_text_containing_stop_word(self):
        response = requests.post(
            'http://127.0.0.1:5000/greeting',
            data={'latest_block_text': 'Almost'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            app.config['GREETING_NO_REQUIRED_STRING']
        )

    def test_greeting_with_latest_block_text_containing_verbs(self):
        response = requests.post(
            'http://127.0.0.1:5000/greeting',
            data={'latest_block_text': 'subsist exist.'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            app.config['GREETING_TEMPLATE_WITH_REQUIRED_STRING'].replace(
                '{{ required_string }}',
                'exist'
            )
        )

    def test_greeting_with_latest_block_text_containing_noun_phrases(self):
        response = requests.post(
            'http://127.0.0.1:5000/greeting',
            data={'latest_block_text': 'The quick brown fox jumps over the lazy dog.'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            app.config['GREETING_TEMPLATE_WITH_REQUIRED_STRING'].replace(
                '{{ required_string }}',
                'the lazy dog'
            )
        )

    def test_validate_with_no_latest_text_and_no_matching_pattern(self):

        response = requests.post(
            'http://127.0.0.1:5000/validate',
            data={'proposed_block_text': 'I am a the lazy dog.'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'valid': False,
                'message': app.config['PROPOSAL_INVALID_MESSAGE']
            }

        )

    def test_validate_with_latest_text_and_no_matching_pattern(self):

        response = requests.post(
            'http://127.0.0.1:5000/validate',
            data={
                'latest_block_text': 'I once was a spoon.',
                'proposed_block_text': 'I am a the lazy dog.'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'valid': False,
                'message': app.config['PROPOSAL_INVALID_MESSAGE']
            }
        )

    def test_validate_with_latest_text_and_matching_pattern(self):

        response = requests.post(
            'http://127.0.0.1:5000/validate',
            data={
                'latest_block_text': 'I paid £1 for my spoon.',
                'proposed_block_text': 'I did not earn my $1,000,000,000.'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'valid': True,
                'message': app.config['PROPOSAL_VALID_MESSAGE']
            }
        )

    def test_validate_with_latest_text_and_matching_phrase(self):

        response = requests.post(
            'http://127.0.0.1:5000/validate',
            data={
                'latest_block_text': 'I hated her.',
                'proposed_block_text': 'I loved her.'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'valid': True,
                'message': app.config['PROPOSAL_VALID_MESSAGE']
            }
        )

    def test_validate_with_latest_text_matching_phrase_and_pattern(self):

        response = requests.post(
            'http://127.0.0.1:5000/validate',
            data={
                'latest_block_text': 'I hated her £500 shoes.',
                'proposed_block_text': 'I loved her £500 shoes.'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'valid': True,
                'message': app.config['PROPOSAL_VALID_MESSAGE']
            }
        )


if __name__ == '__main__':
    unittest.main()