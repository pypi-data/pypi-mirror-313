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


class ReleaseUpdateParameters(object):
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
        'description': 'str',
        'platforms': 'List[str]',
        'app_min_version': 'str',
        'app_max_version': 'str',
        'branch': 'str'
    }

    attribute_map = {
        'description': 'description',
        'platforms': 'platforms',
        'app_min_version': 'app_min_version',
        'app_max_version': 'app_max_version',
        'branch': 'branch'
    }

    def __init__(self, description=None, platforms=None, app_min_version=None, app_max_version=None, branch=None, local_vars_configuration=None):  # noqa: E501
        """ReleaseUpdateParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._description = None
        self._platforms = None
        self._app_min_version = None
        self._app_max_version = None
        self._branch = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if platforms is not None:
            self.platforms = platforms
        if app_min_version is not None:
            self.app_min_version = app_min_version
        if app_max_version is not None:
            self.app_max_version = app_max_version
        if branch is not None:
            self.branch = branch

    @property
    def description(self):
        """Gets the description of this ReleaseUpdateParameters.  # noqa: E501

        Description of the release  # noqa: E501

        :return: The description of this ReleaseUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ReleaseUpdateParameters.

        Description of the release  # noqa: E501

        :param description: The description of this ReleaseUpdateParameters.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def platforms(self):
        """Gets the platforms of this ReleaseUpdateParameters.  # noqa: E501

        List of platforms the release should support.  # noqa: E501

        :return: The platforms of this ReleaseUpdateParameters.  # noqa: E501
        :rtype: List[str]
        """
        return self._platforms

    @platforms.setter
    def platforms(self, platforms):
        """Sets the platforms of this ReleaseUpdateParameters.

        List of platforms the release should support.  # noqa: E501

        :param platforms: The platforms of this ReleaseUpdateParameters.  # noqa: E501
        :type: List[str]
        """

        self._platforms = platforms

    @property
    def app_min_version(self):
        """Gets the app_min_version of this ReleaseUpdateParameters.  # noqa: E501

        Minimum version of the app that the release supports in semver format  # noqa: E501

        :return: The app_min_version of this ReleaseUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._app_min_version

    @app_min_version.setter
    def app_min_version(self, app_min_version):
        """Sets the app_min_version of this ReleaseUpdateParameters.

        Minimum version of the app that the release supports in semver format  # noqa: E501

        :param app_min_version: The app_min_version of this ReleaseUpdateParameters.  # noqa: E501
        :type: str
        """

        self._app_min_version = app_min_version

    @property
    def app_max_version(self):
        """Gets the app_max_version of this ReleaseUpdateParameters.  # noqa: E501

        Maximum version of the app that the release supports in semver format  # noqa: E501

        :return: The app_max_version of this ReleaseUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._app_max_version

    @app_max_version.setter
    def app_max_version(self, app_max_version):
        """Sets the app_max_version of this ReleaseUpdateParameters.

        Maximum version of the app that the release supports in semver format  # noqa: E501

        :param app_max_version: The app_max_version of this ReleaseUpdateParameters.  # noqa: E501
        :type: str
        """

        self._app_max_version = app_max_version

    @property
    def branch(self):
        """Gets the branch of this ReleaseUpdateParameters.  # noqa: E501

        Branch used for release  # noqa: E501

        :return: The branch of this ReleaseUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._branch

    @branch.setter
    def branch(self, branch):
        """Sets the branch of this ReleaseUpdateParameters.

        Branch used for release  # noqa: E501

        :param branch: The branch of this ReleaseUpdateParameters.  # noqa: E501
        :type: str
        """

        self._branch = branch

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
        if not isinstance(other, ReleaseUpdateParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReleaseUpdateParameters):
            return True

        return self.to_dict() != other.to_dict()
