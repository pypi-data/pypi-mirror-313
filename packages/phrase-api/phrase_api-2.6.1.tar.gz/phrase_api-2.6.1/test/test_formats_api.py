# coding: utf-8

"""
    Phrase Strings API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import phrase_api
from phrase_api.api.formats_api import FormatsApi  # noqa: E501
from phrase_api.rest import ApiException


class TestFormatsApi(unittest.TestCase):
    """FormatsApi unit test stubs"""

    def setUp(self):
        self.api = phrase_api.api.formats_api.FormatsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_formats_list(self):
        """Test case for formats_list

        List formats  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
