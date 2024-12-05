# coding: utf-8

"""
    Phrase Strings API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import phrase_api
from phrase_api.models.custom_metadata_property_create422_response_errors_inner import CustomMetadataPropertyCreate422ResponseErrorsInner  # noqa: E501
from phrase_api.rest import ApiException

class TestCustomMetadataPropertyCreate422ResponseErrorsInner(unittest.TestCase):
    """CustomMetadataPropertyCreate422ResponseErrorsInner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CustomMetadataPropertyCreate422ResponseErrorsInner
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = phrase_api.models.custom_metadata_property_create422_response_errors_inner.CustomMetadataPropertyCreate422ResponseErrorsInner()  # noqa: E501

        """
        if include_optional :
            return CustomMetadataPropertyCreate422ResponseErrorsInner(
                resource = '', 
                field = '', 
                message = ''
            )
        else :
            return CustomMetadataPropertyCreate422ResponseErrorsInner(
        )
        """

    def testCustomMetadataPropertyCreate422ResponseErrorsInner(self):
        """Test CustomMetadataPropertyCreate422ResponseErrorsInner"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
