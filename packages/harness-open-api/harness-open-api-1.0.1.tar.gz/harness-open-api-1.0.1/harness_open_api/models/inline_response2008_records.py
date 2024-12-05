# coding: utf-8

"""
    Harness NextGen Software Delivery Platform API Reference

    The Harness Software Delivery Platform uses OpenAPI Specification v3.0. Harness constantly improves these APIs. Please be aware that some improvements could cause breaking changes. # Introduction     The Harness API allows you to integrate and use all the services and modules we provide on the Harness Platform. If you use client-side SDKs, Harness functionality can be integrated with your client-side automation, helping you reduce manual efforts and deploy code faster.    For more information about how Harness works, read our [documentation](https://developer.harness.io/docs/getting-started) or visit the [Harness Developer Hub](https://developer.harness.io/).  ## How it works    The Harness API is a RESTful API that uses standard HTTP verbs. You can send requests in JSON, YAML, or form-data format. The format of the response matches the format of your request. You must send a single request at a time and ensure that you include your authentication key. For more information about this, go to [Authentication](#section/Introduction/Authentication).  ## Get started    Before you start integrating, get to know our API better by reading the following topics:    * [Harness key concepts](https://developer.harness.io/docs/getting-started/learn-harness-key-concepts/)   * [Authentication](#section/Introduction/Authentication)   * [Requests and responses](#section/Introduction/Requests-and-Responses)   * [Common Parameters](#section/Introduction/Common-Parameters-Beta)   * [Status Codes](#section/Introduction/Status-Codes)   * [Errors](#tag/Error-Response)   * [Versioning](#section/Introduction/Versioning-Beta)   * [Pagination](/#section/Introduction/Pagination-Beta)    The methods you need to integrate with depend on the functionality you want to use. Work with  your Harness Solutions Engineer to determine which methods you need.  ## Authentication  To authenticate with the Harness API, you need to:   1. Generate an API token on the Harness Platform.   2. Send the API token you generate in the `x-api-key` header in each request.  ### Generate an API token  To generate an API token, complete the following steps:   1. Go to the [Harness Platform](https://app.harness.io/).   2. On the left-hand navigation, click **My Profile**.   3. Click **+API Key**, enter a name for your key and then click **Save**.   4. Within the API Key tile, click **+Token**.   5. Enter a name for your token and click **Generate Token**. **Important**: Make sure to save your token securely. Harness does not store the API token for future reference, so make sure to save your token securely before you leave the page.  ### Send the API token in your requests  Send the token you created in the Harness Platform in the x-api-key header. For example:   `x-api-key: YOUR_API_KEY_HERE`  ## Requests and Responses    The structure for each request and response is outlined in the API documentation. We have examples in JSON and YAML for every request and response. You can use our online editor to test the examples.  ## Common Parameters [Beta]  | Field Name | Type    | Default | Description    | |------------|---------|---------|----------------| | identifier | string  | none    | URL-friendly version of the name, used to identify a resource within it's scope and so needs to be unique within the scope.                                                                                                            | | name       | string  | none    | Human-friendly name for the resource.                                                                                       | | org        | string  | none    | Limit to provided org identifiers.                                                                                                                     | | project    | string  | none    | Limit to provided project identifiers.                                                                                                                 | | description| string  | none    | More information about the specific resource.                                                                                    | | tags       | map[string]string  | none    | List of labels applied to the resource.                                                                                                                         | | order      | string  | desc    | Order to use when sorting the specified fields. Type: enum(asc,desc).                                                                                                                                     | | sort       | string  | none    | Fields on which to sort. Note: Specify the fields that you want to use for sorting. When doing so, consider the operational overhead of sorting fields. | | limit      | int     | 30      | Pagination: Number of items to return.                                                                                                                 | | page       | int     | 1       | Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page.                  | | created    | int64   | none    | Unix timestamp that shows when the resource was created (in milliseconds).                                                               | | updated    | int64   | none    | Unix timestamp that shows when the resource was last edited (in milliseconds).                                                           |   ## Status Codes    Harness uses conventional HTTP status codes to indicate the status of an API request.    Generally, 2xx responses are reserved for success and 4xx status codes are reserved for failures. A 5xx response code indicates an error on the Harness server.    | Error Code  | Description |   |-------------|-------------|   | 200         |     OK      |   | 201         |   Created   |   | 202         |   Accepted  |   | 204         |  No Content |   | 400         | Bad Request |   | 401         | Unauthorized |   | 403         | Forbidden |   | 412         | Precondition Failed |   | 415         | Unsupported Media Type |   | 500         | Server Error |    To view our error response structures, go [here](#tag/Error-Response).  ## Versioning [Beta]  ### Harness Version   The current version of our Beta APIs is yet to be announced. The version number will use the date-header format and will be valid only for our Beta APIs.  ### Generation   All our beta APIs are versioned as a Generation, and this version is included in the path to every API resource. For example, v1 beta APIs begin with `app.harness.io/v1/`, where v1 is the API Generation.    The version number represents the core API and does not change frequently. The version number changes only if there is a significant departure from the basic underpinnings of the existing API. For example, when Harness performs a system-wide refactoring of core concepts or resources.  ## Pagination [Beta]  We use pagination to place limits on the number of responses associated with list endpoints. Pagination is achieved by the use of limit query parameters. The limit defaults to 30. Its maximum value is 100.  Following are the pagination headers supported in the response bodies of paginated APIs:   1. X-Total-Elements : Indicates the total number of entries in a paginated response.   2. X-Page-Number : Indicates the page number currently returned for a paginated response.   3. X-Page-Size : Indicates the number of entries per page for a paginated response.  For example:    ``` X-Total-Elements : 30 X-Page-Number : 0 X-Page-Size : 10   ```   # noqa: E501

    OpenAPI spec version: 1.0
    Contact: contact@harness.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InlineResponse2008Records(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'ou_id': 'str',
        'name': 'str',
        'tags': 'list[str]',
        'managers': 'list[str]',
        'admins': 'list[str]',
        'sections': 'list[str]',
        'version': 'str',
        'no_of_dashboards': 'int',
        'path': 'str',
        'ou_category_id': 'str',
        'default_dashboard_id': 'int',
        'workspace_id': 'int',
        'created_at': 'int',
        'parent_ref_id': 'int',
        'workflow_profile_id': 'str',
        'workflow_profile_name': 'str'
    }

    attribute_map = {
        'id': 'id',
        'ou_id': 'ou_id',
        'name': 'name',
        'tags': 'tags',
        'managers': 'managers',
        'admins': 'admins',
        'sections': 'sections',
        'version': 'version',
        'no_of_dashboards': 'no_of_dashboards',
        'path': 'path',
        'ou_category_id': 'ou_category_id',
        'default_dashboard_id': 'default_dashboard_id',
        'workspace_id': 'workspace_id',
        'created_at': 'created_at',
        'parent_ref_id': 'parent_ref_id',
        'workflow_profile_id': 'workflow_profile_id',
        'workflow_profile_name': 'workflow_profile_name'
    }

    def __init__(self, id=None, ou_id=None, name=None, tags=None, managers=None, admins=None, sections=None, version=None, no_of_dashboards=None, path=None, ou_category_id=None, default_dashboard_id=None, workspace_id=None, created_at=None, parent_ref_id=None, workflow_profile_id=None, workflow_profile_name=None):  # noqa: E501
        """InlineResponse2008Records - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._ou_id = None
        self._name = None
        self._tags = None
        self._managers = None
        self._admins = None
        self._sections = None
        self._version = None
        self._no_of_dashboards = None
        self._path = None
        self._ou_category_id = None
        self._default_dashboard_id = None
        self._workspace_id = None
        self._created_at = None
        self._parent_ref_id = None
        self._workflow_profile_id = None
        self._workflow_profile_name = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if ou_id is not None:
            self.ou_id = ou_id
        if name is not None:
            self.name = name
        if tags is not None:
            self.tags = tags
        if managers is not None:
            self.managers = managers
        if admins is not None:
            self.admins = admins
        if sections is not None:
            self.sections = sections
        if version is not None:
            self.version = version
        if no_of_dashboards is not None:
            self.no_of_dashboards = no_of_dashboards
        if path is not None:
            self.path = path
        if ou_category_id is not None:
            self.ou_category_id = ou_category_id
        if default_dashboard_id is not None:
            self.default_dashboard_id = default_dashboard_id
        if workspace_id is not None:
            self.workspace_id = workspace_id
        if created_at is not None:
            self.created_at = created_at
        if parent_ref_id is not None:
            self.parent_ref_id = parent_ref_id
        if workflow_profile_id is not None:
            self.workflow_profile_id = workflow_profile_id
        if workflow_profile_name is not None:
            self.workflow_profile_name = workflow_profile_name

    @property
    def id(self):
        """Gets the id of this InlineResponse2008Records.  # noqa: E501


        :return: The id of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse2008Records.


        :param id: The id of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def ou_id(self):
        """Gets the ou_id of this InlineResponse2008Records.  # noqa: E501


        :return: The ou_id of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._ou_id

    @ou_id.setter
    def ou_id(self, ou_id):
        """Sets the ou_id of this InlineResponse2008Records.


        :param ou_id: The ou_id of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._ou_id = ou_id

    @property
    def name(self):
        """Gets the name of this InlineResponse2008Records.  # noqa: E501


        :return: The name of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse2008Records.


        :param name: The name of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def tags(self):
        """Gets the tags of this InlineResponse2008Records.  # noqa: E501


        :return: The tags of this InlineResponse2008Records.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this InlineResponse2008Records.


        :param tags: The tags of this InlineResponse2008Records.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def managers(self):
        """Gets the managers of this InlineResponse2008Records.  # noqa: E501


        :return: The managers of this InlineResponse2008Records.  # noqa: E501
        :rtype: list[str]
        """
        return self._managers

    @managers.setter
    def managers(self, managers):
        """Sets the managers of this InlineResponse2008Records.


        :param managers: The managers of this InlineResponse2008Records.  # noqa: E501
        :type: list[str]
        """

        self._managers = managers

    @property
    def admins(self):
        """Gets the admins of this InlineResponse2008Records.  # noqa: E501


        :return: The admins of this InlineResponse2008Records.  # noqa: E501
        :rtype: list[str]
        """
        return self._admins

    @admins.setter
    def admins(self, admins):
        """Sets the admins of this InlineResponse2008Records.


        :param admins: The admins of this InlineResponse2008Records.  # noqa: E501
        :type: list[str]
        """

        self._admins = admins

    @property
    def sections(self):
        """Gets the sections of this InlineResponse2008Records.  # noqa: E501


        :return: The sections of this InlineResponse2008Records.  # noqa: E501
        :rtype: list[str]
        """
        return self._sections

    @sections.setter
    def sections(self, sections):
        """Sets the sections of this InlineResponse2008Records.


        :param sections: The sections of this InlineResponse2008Records.  # noqa: E501
        :type: list[str]
        """

        self._sections = sections

    @property
    def version(self):
        """Gets the version of this InlineResponse2008Records.  # noqa: E501


        :return: The version of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this InlineResponse2008Records.


        :param version: The version of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def no_of_dashboards(self):
        """Gets the no_of_dashboards of this InlineResponse2008Records.  # noqa: E501


        :return: The no_of_dashboards of this InlineResponse2008Records.  # noqa: E501
        :rtype: int
        """
        return self._no_of_dashboards

    @no_of_dashboards.setter
    def no_of_dashboards(self, no_of_dashboards):
        """Sets the no_of_dashboards of this InlineResponse2008Records.


        :param no_of_dashboards: The no_of_dashboards of this InlineResponse2008Records.  # noqa: E501
        :type: int
        """

        self._no_of_dashboards = no_of_dashboards

    @property
    def path(self):
        """Gets the path of this InlineResponse2008Records.  # noqa: E501


        :return: The path of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this InlineResponse2008Records.


        :param path: The path of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def ou_category_id(self):
        """Gets the ou_category_id of this InlineResponse2008Records.  # noqa: E501


        :return: The ou_category_id of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._ou_category_id

    @ou_category_id.setter
    def ou_category_id(self, ou_category_id):
        """Sets the ou_category_id of this InlineResponse2008Records.


        :param ou_category_id: The ou_category_id of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._ou_category_id = ou_category_id

    @property
    def default_dashboard_id(self):
        """Gets the default_dashboard_id of this InlineResponse2008Records.  # noqa: E501


        :return: The default_dashboard_id of this InlineResponse2008Records.  # noqa: E501
        :rtype: int
        """
        return self._default_dashboard_id

    @default_dashboard_id.setter
    def default_dashboard_id(self, default_dashboard_id):
        """Sets the default_dashboard_id of this InlineResponse2008Records.


        :param default_dashboard_id: The default_dashboard_id of this InlineResponse2008Records.  # noqa: E501
        :type: int
        """

        self._default_dashboard_id = default_dashboard_id

    @property
    def workspace_id(self):
        """Gets the workspace_id of this InlineResponse2008Records.  # noqa: E501


        :return: The workspace_id of this InlineResponse2008Records.  # noqa: E501
        :rtype: int
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this InlineResponse2008Records.


        :param workspace_id: The workspace_id of this InlineResponse2008Records.  # noqa: E501
        :type: int
        """

        self._workspace_id = workspace_id

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse2008Records.  # noqa: E501


        :return: The created_at of this InlineResponse2008Records.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse2008Records.


        :param created_at: The created_at of this InlineResponse2008Records.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def parent_ref_id(self):
        """Gets the parent_ref_id of this InlineResponse2008Records.  # noqa: E501


        :return: The parent_ref_id of this InlineResponse2008Records.  # noqa: E501
        :rtype: int
        """
        return self._parent_ref_id

    @parent_ref_id.setter
    def parent_ref_id(self, parent_ref_id):
        """Sets the parent_ref_id of this InlineResponse2008Records.


        :param parent_ref_id: The parent_ref_id of this InlineResponse2008Records.  # noqa: E501
        :type: int
        """

        self._parent_ref_id = parent_ref_id

    @property
    def workflow_profile_id(self):
        """Gets the workflow_profile_id of this InlineResponse2008Records.  # noqa: E501


        :return: The workflow_profile_id of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._workflow_profile_id

    @workflow_profile_id.setter
    def workflow_profile_id(self, workflow_profile_id):
        """Sets the workflow_profile_id of this InlineResponse2008Records.


        :param workflow_profile_id: The workflow_profile_id of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._workflow_profile_id = workflow_profile_id

    @property
    def workflow_profile_name(self):
        """Gets the workflow_profile_name of this InlineResponse2008Records.  # noqa: E501


        :return: The workflow_profile_name of this InlineResponse2008Records.  # noqa: E501
        :rtype: str
        """
        return self._workflow_profile_name

    @workflow_profile_name.setter
    def workflow_profile_name(self, workflow_profile_name):
        """Sets the workflow_profile_name of this InlineResponse2008Records.


        :param workflow_profile_name: The workflow_profile_name of this InlineResponse2008Records.  # noqa: E501
        :type: str
        """

        self._workflow_profile_name = workflow_profile_name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(InlineResponse2008Records, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InlineResponse2008Records):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
