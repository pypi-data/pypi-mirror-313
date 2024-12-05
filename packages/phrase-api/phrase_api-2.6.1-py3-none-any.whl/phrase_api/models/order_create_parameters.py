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


class OrderCreateParameters(object):
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
        'branch': 'str',
        'name': 'str',
        'lsp': 'str',
        'source_locale_id': 'str',
        'target_locale_ids': 'List[str]',
        'translation_type': 'str',
        'tag': 'str',
        'message': 'str',
        'styleguide_id': 'str',
        'unverify_translations_upon_delivery': 'bool',
        'include_untranslated_keys': 'bool',
        'include_unverified_translations': 'bool',
        'category': 'str',
        'quality': 'bool',
        'priority': 'bool'
    }

    attribute_map = {
        'branch': 'branch',
        'name': 'name',
        'lsp': 'lsp',
        'source_locale_id': 'source_locale_id',
        'target_locale_ids': 'target_locale_ids',
        'translation_type': 'translation_type',
        'tag': 'tag',
        'message': 'message',
        'styleguide_id': 'styleguide_id',
        'unverify_translations_upon_delivery': 'unverify_translations_upon_delivery',
        'include_untranslated_keys': 'include_untranslated_keys',
        'include_unverified_translations': 'include_unverified_translations',
        'category': 'category',
        'quality': 'quality',
        'priority': 'priority'
    }

    def __init__(self, branch=None, name=None, lsp=None, source_locale_id=None, target_locale_ids=None, translation_type=None, tag=None, message=None, styleguide_id=None, unverify_translations_upon_delivery=None, include_untranslated_keys=None, include_unverified_translations=None, category=None, quality=None, priority=None, local_vars_configuration=None):  # noqa: E501
        """OrderCreateParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._branch = None
        self._name = None
        self._lsp = None
        self._source_locale_id = None
        self._target_locale_ids = None
        self._translation_type = None
        self._tag = None
        self._message = None
        self._styleguide_id = None
        self._unverify_translations_upon_delivery = None
        self._include_untranslated_keys = None
        self._include_unverified_translations = None
        self._category = None
        self._quality = None
        self._priority = None
        self.discriminator = None

        if branch is not None:
            self.branch = branch
        self.name = name
        self.lsp = lsp
        if source_locale_id is not None:
            self.source_locale_id = source_locale_id
        if target_locale_ids is not None:
            self.target_locale_ids = target_locale_ids
        if translation_type is not None:
            self.translation_type = translation_type
        if tag is not None:
            self.tag = tag
        if message is not None:
            self.message = message
        if styleguide_id is not None:
            self.styleguide_id = styleguide_id
        if unverify_translations_upon_delivery is not None:
            self.unverify_translations_upon_delivery = unverify_translations_upon_delivery
        if include_untranslated_keys is not None:
            self.include_untranslated_keys = include_untranslated_keys
        if include_unverified_translations is not None:
            self.include_unverified_translations = include_unverified_translations
        if category is not None:
            self.category = category
        if quality is not None:
            self.quality = quality
        if priority is not None:
            self.priority = priority

    @property
    def branch(self):
        """Gets the branch of this OrderCreateParameters.  # noqa: E501

        specify the branch to use  # noqa: E501

        :return: The branch of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._branch

    @branch.setter
    def branch(self, branch):
        """Sets the branch of this OrderCreateParameters.

        specify the branch to use  # noqa: E501

        :param branch: The branch of this OrderCreateParameters.  # noqa: E501
        :type: str
        """

        self._branch = branch

    @property
    def name(self):
        """Gets the name of this OrderCreateParameters.  # noqa: E501

        the name of the order, default name is: Translation order from 'current datetime'  # noqa: E501

        :return: The name of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrderCreateParameters.

        the name of the order, default name is: Translation order from 'current datetime'  # noqa: E501

        :param name: The name of this OrderCreateParameters.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def lsp(self):
        """Gets the lsp of this OrderCreateParameters.  # noqa: E501

        Name of the LSP that should process this order. Can be one of gengo, textmaster.  # noqa: E501

        :return: The lsp of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._lsp

    @lsp.setter
    def lsp(self, lsp):
        """Sets the lsp of this OrderCreateParameters.

        Name of the LSP that should process this order. Can be one of gengo, textmaster.  # noqa: E501

        :param lsp: The lsp of this OrderCreateParameters.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and lsp is None:  # noqa: E501
            raise ValueError("Invalid value for `lsp`, must not be `None`")  # noqa: E501

        self._lsp = lsp

    @property
    def source_locale_id(self):
        """Gets the source_locale_id of this OrderCreateParameters.  # noqa: E501

        Source locale for the order. Can be the name or id of the source locale. Preferred is id.  # noqa: E501

        :return: The source_locale_id of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._source_locale_id

    @source_locale_id.setter
    def source_locale_id(self, source_locale_id):
        """Sets the source_locale_id of this OrderCreateParameters.

        Source locale for the order. Can be the name or id of the source locale. Preferred is id.  # noqa: E501

        :param source_locale_id: The source_locale_id of this OrderCreateParameters.  # noqa: E501
        :type: str
        """

        self._source_locale_id = source_locale_id

    @property
    def target_locale_ids(self):
        """Gets the target_locale_ids of this OrderCreateParameters.  # noqa: E501

        List of target locales you want the source content translate to. Can be the name or id of the target locales. Preferred is id.  # noqa: E501

        :return: The target_locale_ids of this OrderCreateParameters.  # noqa: E501
        :rtype: List[str]
        """
        return self._target_locale_ids

    @target_locale_ids.setter
    def target_locale_ids(self, target_locale_ids):
        """Sets the target_locale_ids of this OrderCreateParameters.

        List of target locales you want the source content translate to. Can be the name or id of the target locales. Preferred is id.  # noqa: E501

        :param target_locale_ids: The target_locale_ids of this OrderCreateParameters.  # noqa: E501
        :type: List[str]
        """

        self._target_locale_ids = target_locale_ids

    @property
    def translation_type(self):
        """Gets the translation_type of this OrderCreateParameters.  # noqa: E501

        Name of the quality level, availability depends on the LSP. Can be one of:  standard, pro (for orders processed by Gengo) and one of regular, premium, enterprise (for orders processed by TextMaster)  # noqa: E501

        :return: The translation_type of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._translation_type

    @translation_type.setter
    def translation_type(self, translation_type):
        """Sets the translation_type of this OrderCreateParameters.

        Name of the quality level, availability depends on the LSP. Can be one of:  standard, pro (for orders processed by Gengo) and one of regular, premium, enterprise (for orders processed by TextMaster)  # noqa: E501

        :param translation_type: The translation_type of this OrderCreateParameters.  # noqa: E501
        :type: str
        """

        self._translation_type = translation_type

    @property
    def tag(self):
        """Gets the tag of this OrderCreateParameters.  # noqa: E501

        Tag you want to order translations for.  # noqa: E501

        :return: The tag of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this OrderCreateParameters.

        Tag you want to order translations for.  # noqa: E501

        :param tag: The tag of this OrderCreateParameters.  # noqa: E501
        :type: str
        """

        self._tag = tag

    @property
    def message(self):
        """Gets the message of this OrderCreateParameters.  # noqa: E501

        Message that is displayed to the translators for description.  # noqa: E501

        :return: The message of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this OrderCreateParameters.

        Message that is displayed to the translators for description.  # noqa: E501

        :param message: The message of this OrderCreateParameters.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def styleguide_id(self):
        """Gets the styleguide_id of this OrderCreateParameters.  # noqa: E501

        Style guide for translators to be sent with the order.  # noqa: E501

        :return: The styleguide_id of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._styleguide_id

    @styleguide_id.setter
    def styleguide_id(self, styleguide_id):
        """Sets the styleguide_id of this OrderCreateParameters.

        Style guide for translators to be sent with the order.  # noqa: E501

        :param styleguide_id: The styleguide_id of this OrderCreateParameters.  # noqa: E501
        :type: str
        """

        self._styleguide_id = styleguide_id

    @property
    def unverify_translations_upon_delivery(self):
        """Gets the unverify_translations_upon_delivery of this OrderCreateParameters.  # noqa: E501

        Unverify translations upon delivery.  # noqa: E501

        :return: The unverify_translations_upon_delivery of this OrderCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._unverify_translations_upon_delivery

    @unverify_translations_upon_delivery.setter
    def unverify_translations_upon_delivery(self, unverify_translations_upon_delivery):
        """Sets the unverify_translations_upon_delivery of this OrderCreateParameters.

        Unverify translations upon delivery.  # noqa: E501

        :param unverify_translations_upon_delivery: The unverify_translations_upon_delivery of this OrderCreateParameters.  # noqa: E501
        :type: bool
        """

        self._unverify_translations_upon_delivery = unverify_translations_upon_delivery

    @property
    def include_untranslated_keys(self):
        """Gets the include_untranslated_keys of this OrderCreateParameters.  # noqa: E501

        Order translations for keys with untranslated content in the selected target locales.  # noqa: E501

        :return: The include_untranslated_keys of this OrderCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._include_untranslated_keys

    @include_untranslated_keys.setter
    def include_untranslated_keys(self, include_untranslated_keys):
        """Sets the include_untranslated_keys of this OrderCreateParameters.

        Order translations for keys with untranslated content in the selected target locales.  # noqa: E501

        :param include_untranslated_keys: The include_untranslated_keys of this OrderCreateParameters.  # noqa: E501
        :type: bool
        """

        self._include_untranslated_keys = include_untranslated_keys

    @property
    def include_unverified_translations(self):
        """Gets the include_unverified_translations of this OrderCreateParameters.  # noqa: E501

        Order translations for keys with unverified content in the selected target locales.  # noqa: E501

        :return: The include_unverified_translations of this OrderCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._include_unverified_translations

    @include_unverified_translations.setter
    def include_unverified_translations(self, include_unverified_translations):
        """Sets the include_unverified_translations of this OrderCreateParameters.

        Order translations for keys with unverified content in the selected target locales.  # noqa: E501

        :param include_unverified_translations: The include_unverified_translations of this OrderCreateParameters.  # noqa: E501
        :type: bool
        """

        self._include_unverified_translations = include_unverified_translations

    @property
    def category(self):
        """Gets the category of this OrderCreateParameters.  # noqa: E501

        Category to use (required for orders processed by TextMaster).  # noqa: E501

        :return: The category of this OrderCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this OrderCreateParameters.

        Category to use (required for orders processed by TextMaster).  # noqa: E501

        :param category: The category of this OrderCreateParameters.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def quality(self):
        """Gets the quality of this OrderCreateParameters.  # noqa: E501

        Extra proofreading option to ensure consistency in vocabulary and style. Only available for orders processed by TextMaster.  # noqa: E501

        :return: The quality of this OrderCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._quality

    @quality.setter
    def quality(self, quality):
        """Sets the quality of this OrderCreateParameters.

        Extra proofreading option to ensure consistency in vocabulary and style. Only available for orders processed by TextMaster.  # noqa: E501

        :param quality: The quality of this OrderCreateParameters.  # noqa: E501
        :type: bool
        """

        self._quality = quality

    @property
    def priority(self):
        """Gets the priority of this OrderCreateParameters.  # noqa: E501

        Indicates whether the priority option should be ordered which decreases turnaround time by 30%. Available only for orders processed by TextMaster.  # noqa: E501

        :return: The priority of this OrderCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this OrderCreateParameters.

        Indicates whether the priority option should be ordered which decreases turnaround time by 30%. Available only for orders processed by TextMaster.  # noqa: E501

        :param priority: The priority of this OrderCreateParameters.  # noqa: E501
        :type: bool
        """

        self._priority = priority

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
        if not isinstance(other, OrderCreateParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderCreateParameters):
            return True

        return self.to_dict() != other.to_dict()
