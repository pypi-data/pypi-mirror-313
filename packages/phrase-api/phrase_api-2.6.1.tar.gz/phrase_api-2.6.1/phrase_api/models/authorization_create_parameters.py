# coding: utf-8

"""
    Phrase Strings API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from phrase_api.configuration import Configuration


class AuthorizationCreateParameters(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'note': 'str',
        'scopes': 'List[str]',
        'expires_at': 'datetime'
    }

    attribute_map = {
        'note': 'note',
        'scopes': 'scopes',
        'expires_at': 'expires_at'
    }

    def __init__(self, note=None, scopes=None, expires_at=None, local_vars_configuration=None):  # noqa: E501
        """AuthorizationCreateParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._note = None
        self._scopes = None
        self._expires_at = None
        self.discriminator = None

        self.note = note
        if scopes is not None:
            self.scopes = scopes
        if expires_at is not None:
            self.expires_at = expires_at

    @property
    def note(self):
        """Gets the note of this AuthorizationCreateParameters.  # noqa: E501

        A note to help you remember what the access is used for.  # noqa: E501

        :return: The note of this AuthorizationCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note):
        """Sets the note of this AuthorizationCreateParameters.

        A note to help you remember what the access is used for.  # noqa: E501

        :param note: The note of this AuthorizationCreateParameters.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and note is None:  # noqa: E501
            raise ValueError("Invalid value for `note`, must not be `None`")  # noqa: E501

        self._note = note

    @property
    def scopes(self):
        """Gets the scopes of this AuthorizationCreateParameters.  # noqa: E501

        A list of scopes that the access can be used for.  # noqa: E501

        :return: The scopes of this AuthorizationCreateParameters.  # noqa: E501
        :rtype: List[str]
        """
        return self._scopes

    @scopes.setter
    def scopes(self, scopes):
        """Sets the scopes of this AuthorizationCreateParameters.

        A list of scopes that the access can be used for.  # noqa: E501

        :param scopes: The scopes of this AuthorizationCreateParameters.  # noqa: E501
        :type: List[str]
        """

        self._scopes = scopes

    @property
    def expires_at(self):
        """Gets the expires_at of this AuthorizationCreateParameters.  # noqa: E501

        Expiration date for the authorization token. Null means no expiration date (default).  # noqa: E501

        :return: The expires_at of this AuthorizationCreateParameters.  # noqa: E501
        :rtype: datetime
        """
        return self._expires_at

    @expires_at.setter
    def expires_at(self, expires_at):
        """Sets the expires_at of this AuthorizationCreateParameters.

        Expiration date for the authorization token. Null means no expiration date (default).  # noqa: E501

        :param expires_at: The expires_at of this AuthorizationCreateParameters.  # noqa: E501
        :type: datetime
        """

        self._expires_at = expires_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AuthorizationCreateParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AuthorizationCreateParameters):
            return True

        return self.to_dict() != other.to_dict()
