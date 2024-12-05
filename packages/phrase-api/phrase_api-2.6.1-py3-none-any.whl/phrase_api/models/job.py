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


class Job(object):
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
        'id': 'str',
        'name': 'str',
        'briefing': 'str',
        'due_date': 'datetime',
        'state': 'str',
        'ticket_url': 'str',
        'project': 'ProjectShort',
        'branch': 'BranchName',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'briefing': 'briefing',
        'due_date': 'due_date',
        'state': 'state',
        'ticket_url': 'ticket_url',
        'project': 'project',
        'branch': 'branch',
        'created_at': 'created_at',
        'updated_at': 'updated_at'
    }

    def __init__(self, id=None, name=None, briefing=None, due_date=None, state=None, ticket_url=None, project=None, branch=None, created_at=None, updated_at=None, local_vars_configuration=None):  # noqa: E501
        """Job - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._briefing = None
        self._due_date = None
        self._state = None
        self._ticket_url = None
        self._project = None
        self._branch = None
        self._created_at = None
        self._updated_at = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if briefing is not None:
            self.briefing = briefing
        self.due_date = due_date
        if state is not None:
            self.state = state
        if ticket_url is not None:
            self.ticket_url = ticket_url
        if project is not None:
            self.project = project
        if branch is not None:
            self.branch = branch
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def id(self):
        """Gets the id of this Job.  # noqa: E501


        :return: The id of this Job.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Job.


        :param id: The id of this Job.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Job.  # noqa: E501


        :return: The name of this Job.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Job.


        :param name: The name of this Job.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def briefing(self):
        """Gets the briefing of this Job.  # noqa: E501


        :return: The briefing of this Job.  # noqa: E501
        :rtype: str
        """
        return self._briefing

    @briefing.setter
    def briefing(self, briefing):
        """Sets the briefing of this Job.


        :param briefing: The briefing of this Job.  # noqa: E501
        :type: str
        """

        self._briefing = briefing

    @property
    def due_date(self):
        """Gets the due_date of this Job.  # noqa: E501


        :return: The due_date of this Job.  # noqa: E501
        :rtype: datetime
        """
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        """Sets the due_date of this Job.


        :param due_date: The due_date of this Job.  # noqa: E501
        :type: datetime
        """

        self._due_date = due_date

    @property
    def state(self):
        """Gets the state of this Job.  # noqa: E501


        :return: The state of this Job.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Job.


        :param state: The state of this Job.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def ticket_url(self):
        """Gets the ticket_url of this Job.  # noqa: E501


        :return: The ticket_url of this Job.  # noqa: E501
        :rtype: str
        """
        return self._ticket_url

    @ticket_url.setter
    def ticket_url(self, ticket_url):
        """Sets the ticket_url of this Job.


        :param ticket_url: The ticket_url of this Job.  # noqa: E501
        :type: str
        """

        self._ticket_url = ticket_url

    @property
    def project(self):
        """Gets the project of this Job.  # noqa: E501


        :return: The project of this Job.  # noqa: E501
        :rtype: ProjectShort
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this Job.


        :param project: The project of this Job.  # noqa: E501
        :type: ProjectShort
        """

        self._project = project

    @property
    def branch(self):
        """Gets the branch of this Job.  # noqa: E501


        :return: The branch of this Job.  # noqa: E501
        :rtype: BranchName
        """
        return self._branch

    @branch.setter
    def branch(self, branch):
        """Sets the branch of this Job.


        :param branch: The branch of this Job.  # noqa: E501
        :type: BranchName
        """

        self._branch = branch

    @property
    def created_at(self):
        """Gets the created_at of this Job.  # noqa: E501


        :return: The created_at of this Job.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Job.


        :param created_at: The created_at of this Job.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Job.  # noqa: E501


        :return: The updated_at of this Job.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Job.


        :param updated_at: The updated_at of this Job.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

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
        if not isinstance(other, Job):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Job):
            return True

        return self.to_dict() != other.to_dict()
