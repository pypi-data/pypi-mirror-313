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
from phrase_api.api.release_triggers_api import ReleaseTriggersApi  # noqa: E501
from phrase_api.rest import ApiException


class TestReleaseTriggersApi(unittest.TestCase):
    """ReleaseTriggersApi unit test stubs"""

    def setUp(self):
        self.api = phrase_api.api.release_triggers_api.ReleaseTriggersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_release_triggers_create(self):
        """Test case for release_triggers_create

        Create a release trigger  # noqa: E501
        """
        pass

    def test_release_triggers_destroy(self):
        """Test case for release_triggers_destroy

        Delete a single release trigger  # noqa: E501
        """
        pass

    def test_release_triggers_list(self):
        """Test case for release_triggers_list

        List release triggers  # noqa: E501
        """
        pass

    def test_release_triggers_show(self):
        """Test case for release_triggers_show

        Get a single release trigger  # noqa: E501
        """
        pass

    def test_release_triggers_update(self):
        """Test case for release_triggers_update

        Update a release trigger  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
