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

class FrontendExemption(object):
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
        'approver_id': 'str',
        'can_approve_for': 'list[str]',
        'can_reject': 'bool',
        'created': 'int',
        'expiration': 'int',
        'id': 'str',
        'issue_summary': 'IssueSummary',
        'last_modified': 'int',
        'link': 'str',
        'org_id': 'str',
        'pending_changes': 'PendingChanges',
        'pipeline_id': 'str',
        'project_id': 'str',
        'reason': 'str',
        'requester_id': 'str',
        'scope': 'str',
        'status': 'str',
        'target_id': 'str',
        'type': 'str'
    }

    attribute_map = {
        'approver_id': 'approverId',
        'can_approve_for': 'canApproveFor',
        'can_reject': 'canReject',
        'created': 'created',
        'expiration': 'expiration',
        'id': 'id',
        'issue_summary': 'issueSummary',
        'last_modified': 'lastModified',
        'link': 'link',
        'org_id': 'orgId',
        'pending_changes': 'pendingChanges',
        'pipeline_id': 'pipelineId',
        'project_id': 'projectId',
        'reason': 'reason',
        'requester_id': 'requesterId',
        'scope': 'scope',
        'status': 'status',
        'target_id': 'targetId',
        'type': 'type'
    }

    def __init__(self, approver_id=None, can_approve_for=None, can_reject=False, created=None, expiration=None, id=None, issue_summary=None, last_modified=None, link=None, org_id=None, pending_changes=None, pipeline_id=None, project_id=None, reason=None, requester_id=None, scope=None, status=None, target_id=None, type=None):  # noqa: E501
        """FrontendExemption - a model defined in Swagger"""  # noqa: E501
        self._approver_id = None
        self._can_approve_for = None
        self._can_reject = None
        self._created = None
        self._expiration = None
        self._id = None
        self._issue_summary = None
        self._last_modified = None
        self._link = None
        self._org_id = None
        self._pending_changes = None
        self._pipeline_id = None
        self._project_id = None
        self._reason = None
        self._requester_id = None
        self._scope = None
        self._status = None
        self._target_id = None
        self._type = None
        self.discriminator = None
        if approver_id is not None:
            self.approver_id = approver_id
        if can_approve_for is not None:
            self.can_approve_for = can_approve_for
        if can_reject is not None:
            self.can_reject = can_reject
        self.created = created
        if expiration is not None:
            self.expiration = expiration
        self.id = id
        self.issue_summary = issue_summary
        self.last_modified = last_modified
        if link is not None:
            self.link = link
        if org_id is not None:
            self.org_id = org_id
        self.pending_changes = pending_changes
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if project_id is not None:
            self.project_id = project_id
        self.reason = reason
        self.requester_id = requester_id
        if scope is not None:
            self.scope = scope
        self.status = status
        if target_id is not None:
            self.target_id = target_id
        self.type = type

    @property
    def approver_id(self):
        """Gets the approver_id of this FrontendExemption.  # noqa: E501

        User ID of the user who approved this Exemption  # noqa: E501

        :return: The approver_id of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._approver_id

    @approver_id.setter
    def approver_id(self, approver_id):
        """Sets the approver_id of this FrontendExemption.

        User ID of the user who approved this Exemption  # noqa: E501

        :param approver_id: The approver_id of this FrontendExemption.  # noqa: E501
        :type: str
        """

        self._approver_id = approver_id

    @property
    def can_approve_for(self):
        """Gets the can_approve_for of this FrontendExemption.  # noqa: E501

        Scopes that the user has permission to approve for this Exemption  # noqa: E501

        :return: The can_approve_for of this FrontendExemption.  # noqa: E501
        :rtype: list[str]
        """
        return self._can_approve_for

    @can_approve_for.setter
    def can_approve_for(self, can_approve_for):
        """Sets the can_approve_for of this FrontendExemption.

        Scopes that the user has permission to approve for this Exemption  # noqa: E501

        :param can_approve_for: The can_approve_for of this FrontendExemption.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["ACCOUNT", "ORG", "PROJECT", "PIPELINE"]  # noqa: E501
        if not set(can_approve_for).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `can_approve_for` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(can_approve_for) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._can_approve_for = can_approve_for

    @property
    def can_reject(self):
        """Gets the can_reject of this FrontendExemption.  # noqa: E501

        States if the user can reject the exemption  # noqa: E501

        :return: The can_reject of this FrontendExemption.  # noqa: E501
        :rtype: bool
        """
        return self._can_reject

    @can_reject.setter
    def can_reject(self, can_reject):
        """Sets the can_reject of this FrontendExemption.

        States if the user can reject the exemption  # noqa: E501

        :param can_reject: The can_reject of this FrontendExemption.  # noqa: E501
        :type: bool
        """

        self._can_reject = can_reject

    @property
    def created(self):
        """Gets the created of this FrontendExemption.  # noqa: E501

        Unix timestamp at which the resource was created  # noqa: E501

        :return: The created of this FrontendExemption.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this FrontendExemption.

        Unix timestamp at which the resource was created  # noqa: E501

        :param created: The created of this FrontendExemption.  # noqa: E501
        :type: int
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def expiration(self):
        """Gets the expiration of this FrontendExemption.  # noqa: E501

        Unix timestamp at which this Exemption will expire  # noqa: E501

        :return: The expiration of this FrontendExemption.  # noqa: E501
        :rtype: int
        """
        return self._expiration

    @expiration.setter
    def expiration(self, expiration):
        """Sets the expiration of this FrontendExemption.

        Unix timestamp at which this Exemption will expire  # noqa: E501

        :param expiration: The expiration of this FrontendExemption.  # noqa: E501
        :type: int
        """

        self._expiration = expiration

    @property
    def id(self):
        """Gets the id of this FrontendExemption.  # noqa: E501

        Resource identifier  # noqa: E501

        :return: The id of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FrontendExemption.

        Resource identifier  # noqa: E501

        :param id: The id of this FrontendExemption.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def issue_summary(self):
        """Gets the issue_summary of this FrontendExemption.  # noqa: E501


        :return: The issue_summary of this FrontendExemption.  # noqa: E501
        :rtype: IssueSummary
        """
        return self._issue_summary

    @issue_summary.setter
    def issue_summary(self, issue_summary):
        """Sets the issue_summary of this FrontendExemption.


        :param issue_summary: The issue_summary of this FrontendExemption.  # noqa: E501
        :type: IssueSummary
        """
        if issue_summary is None:
            raise ValueError("Invalid value for `issue_summary`, must not be `None`")  # noqa: E501

        self._issue_summary = issue_summary

    @property
    def last_modified(self):
        """Gets the last_modified of this FrontendExemption.  # noqa: E501

        Unix timestamp at which the resource was most recently modified  # noqa: E501

        :return: The last_modified of this FrontendExemption.  # noqa: E501
        :rtype: int
        """
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified):
        """Sets the last_modified of this FrontendExemption.

        Unix timestamp at which the resource was most recently modified  # noqa: E501

        :param last_modified: The last_modified of this FrontendExemption.  # noqa: E501
        :type: int
        """
        if last_modified is None:
            raise ValueError("Invalid value for `last_modified`, must not be `None`")  # noqa: E501

        self._last_modified = last_modified

    @property
    def link(self):
        """Gets the link of this FrontendExemption.  # noqa: E501

        Link related to this Exemption  # noqa: E501

        :return: The link of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this FrontendExemption.

        Link related to this Exemption  # noqa: E501

        :param link: The link of this FrontendExemption.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def org_id(self):
        """Gets the org_id of this FrontendExemption.  # noqa: E501

        ID of the Harness Org to which this Exemption applies  # noqa: E501

        :return: The org_id of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this FrontendExemption.

        ID of the Harness Org to which this Exemption applies  # noqa: E501

        :param org_id: The org_id of this FrontendExemption.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def pending_changes(self):
        """Gets the pending_changes of this FrontendExemption.  # noqa: E501


        :return: The pending_changes of this FrontendExemption.  # noqa: E501
        :rtype: PendingChanges
        """
        return self._pending_changes

    @pending_changes.setter
    def pending_changes(self, pending_changes):
        """Sets the pending_changes of this FrontendExemption.


        :param pending_changes: The pending_changes of this FrontendExemption.  # noqa: E501
        :type: PendingChanges
        """
        if pending_changes is None:
            raise ValueError("Invalid value for `pending_changes`, must not be `None`")  # noqa: E501

        self._pending_changes = pending_changes

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this FrontendExemption.  # noqa: E501

        ID of the Harness pipeline to which this Exemption applies  # noqa: E501

        :return: The pipeline_id of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this FrontendExemption.

        ID of the Harness pipeline to which this Exemption applies  # noqa: E501

        :param pipeline_id: The pipeline_id of this FrontendExemption.  # noqa: E501
        :type: str
        """

        self._pipeline_id = pipeline_id

    @property
    def project_id(self):
        """Gets the project_id of this FrontendExemption.  # noqa: E501

        ID of the Harness project to which this Exemption applies  # noqa: E501

        :return: The project_id of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this FrontendExemption.

        ID of the Harness project to which this Exemption applies  # noqa: E501

        :param project_id: The project_id of this FrontendExemption.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def reason(self):
        """Gets the reason of this FrontendExemption.  # noqa: E501

        Reason for Exemption  # noqa: E501

        :return: The reason of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this FrontendExemption.

        Reason for Exemption  # noqa: E501

        :param reason: The reason of this FrontendExemption.  # noqa: E501
        :type: str
        """
        if reason is None:
            raise ValueError("Invalid value for `reason`, must not be `None`")  # noqa: E501

        self._reason = reason

    @property
    def requester_id(self):
        """Gets the requester_id of this FrontendExemption.  # noqa: E501

        User ID of the user who requested this Exemption  # noqa: E501

        :return: The requester_id of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._requester_id

    @requester_id.setter
    def requester_id(self, requester_id):
        """Sets the requester_id of this FrontendExemption.

        User ID of the user who requested this Exemption  # noqa: E501

        :param requester_id: The requester_id of this FrontendExemption.  # noqa: E501
        :type: str
        """
        if requester_id is None:
            raise ValueError("Invalid value for `requester_id`, must not be `None`")  # noqa: E501

        self._requester_id = requester_id

    @property
    def scope(self):
        """Gets the scope of this FrontendExemption.  # noqa: E501

        The scope of the exemption  # noqa: E501

        :return: The scope of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this FrontendExemption.

        The scope of the exemption  # noqa: E501

        :param scope: The scope of this FrontendExemption.  # noqa: E501
        :type: str
        """
        allowed_values = ["ACCOUNT", "ORG", "PROJECT", "PIPELINE"]  # noqa: E501
        if scope not in allowed_values:
            raise ValueError(
                "Invalid value for `scope` ({0}), must be one of {1}"  # noqa: E501
                .format(scope, allowed_values)
            )

        self._scope = scope

    @property
    def status(self):
        """Gets the status of this FrontendExemption.  # noqa: E501

        Status of this Exemption  # noqa: E501

        :return: The status of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this FrontendExemption.

        Status of this Exemption  # noqa: E501

        :param status: The status of this FrontendExemption.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def target_id(self):
        """Gets the target_id of this FrontendExemption.  # noqa: E501

        ID of Target to which this Exemption applies  # noqa: E501

        :return: The target_id of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """Sets the target_id of this FrontendExemption.

        ID of Target to which this Exemption applies  # noqa: E501

        :param target_id: The target_id of this FrontendExemption.  # noqa: E501
        :type: str
        """

        self._target_id = target_id

    @property
    def type(self):
        """Gets the type of this FrontendExemption.  # noqa: E501

        Type of Exemption  # noqa: E501

        :return: The type of this FrontendExemption.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this FrontendExemption.

        Type of Exemption  # noqa: E501

        :param type: The type of this FrontendExemption.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

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
        if issubclass(FrontendExemption, dict):
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
        if not isinstance(other, FrontendExemption):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
