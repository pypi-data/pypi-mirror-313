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

class TriggerPayload(object):
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
        'unknown_fields': 'UnknownFieldSet',
        'type': 'str',
        'version': 'int',
        'image_path': 'str',
        'type_value': 'int',
        'headers_count': 'int',
        'source_type_value': 'int',
        'artifact_data_or_builder': 'ArtifactDataOrBuilder',
        'manifest_data_or_builder': 'ManifestDataOrBuilder',
        'connector_ref_bytes': 'ByteString',
        'image_path_bytes': 'ByteString',
        'build_data_case': 'str',
        'parsed_payload_or_builder': 'ParsedPayloadOrBuilder',
        'connector_ref': 'str',
        'serialized_size': 'int',
        'parser_for_type': 'ParserTriggerPayload',
        'default_instance_for_type': 'TriggerPayload',
        'source_type': 'str',
        'headers_map': 'dict(str, str)',
        'artifact_data': 'ArtifactData',
        'manifest_data': 'ManifestData',
        'parsed_payload': 'ParsedPayload',
        'initialized': 'bool',
        'headers': 'dict(str, str)',
        'all_fields': 'dict(str, object)',
        'descriptor_for_type': 'Descriptor',
        'initialization_error_string': 'str',
        'memoized_serialized_size': 'int'
    }

    attribute_map = {
        'unknown_fields': 'unknownFields',
        'type': 'type',
        'version': 'version',
        'image_path': 'imagePath',
        'type_value': 'typeValue',
        'headers_count': 'headersCount',
        'source_type_value': 'sourceTypeValue',
        'artifact_data_or_builder': 'artifactDataOrBuilder',
        'manifest_data_or_builder': 'manifestDataOrBuilder',
        'connector_ref_bytes': 'connectorRefBytes',
        'image_path_bytes': 'imagePathBytes',
        'build_data_case': 'buildDataCase',
        'parsed_payload_or_builder': 'parsedPayloadOrBuilder',
        'connector_ref': 'connectorRef',
        'serialized_size': 'serializedSize',
        'parser_for_type': 'parserForType',
        'default_instance_for_type': 'defaultInstanceForType',
        'source_type': 'sourceType',
        'headers_map': 'headersMap',
        'artifact_data': 'artifactData',
        'manifest_data': 'manifestData',
        'parsed_payload': 'parsedPayload',
        'initialized': 'initialized',
        'headers': 'headers',
        'all_fields': 'allFields',
        'descriptor_for_type': 'descriptorForType',
        'initialization_error_string': 'initializationErrorString',
        'memoized_serialized_size': 'memoizedSerializedSize'
    }

    def __init__(self, unknown_fields=None, type=None, version=None, image_path=None, type_value=None, headers_count=None, source_type_value=None, artifact_data_or_builder=None, manifest_data_or_builder=None, connector_ref_bytes=None, image_path_bytes=None, build_data_case=None, parsed_payload_or_builder=None, connector_ref=None, serialized_size=None, parser_for_type=None, default_instance_for_type=None, source_type=None, headers_map=None, artifact_data=None, manifest_data=None, parsed_payload=None, initialized=None, headers=None, all_fields=None, descriptor_for_type=None, initialization_error_string=None, memoized_serialized_size=None):  # noqa: E501
        """TriggerPayload - a model defined in Swagger"""  # noqa: E501
        self._unknown_fields = None
        self._type = None
        self._version = None
        self._image_path = None
        self._type_value = None
        self._headers_count = None
        self._source_type_value = None
        self._artifact_data_or_builder = None
        self._manifest_data_or_builder = None
        self._connector_ref_bytes = None
        self._image_path_bytes = None
        self._build_data_case = None
        self._parsed_payload_or_builder = None
        self._connector_ref = None
        self._serialized_size = None
        self._parser_for_type = None
        self._default_instance_for_type = None
        self._source_type = None
        self._headers_map = None
        self._artifact_data = None
        self._manifest_data = None
        self._parsed_payload = None
        self._initialized = None
        self._headers = None
        self._all_fields = None
        self._descriptor_for_type = None
        self._initialization_error_string = None
        self._memoized_serialized_size = None
        self.discriminator = None
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields
        if type is not None:
            self.type = type
        if version is not None:
            self.version = version
        if image_path is not None:
            self.image_path = image_path
        if type_value is not None:
            self.type_value = type_value
        if headers_count is not None:
            self.headers_count = headers_count
        if source_type_value is not None:
            self.source_type_value = source_type_value
        if artifact_data_or_builder is not None:
            self.artifact_data_or_builder = artifact_data_or_builder
        if manifest_data_or_builder is not None:
            self.manifest_data_or_builder = manifest_data_or_builder
        if connector_ref_bytes is not None:
            self.connector_ref_bytes = connector_ref_bytes
        if image_path_bytes is not None:
            self.image_path_bytes = image_path_bytes
        if build_data_case is not None:
            self.build_data_case = build_data_case
        if parsed_payload_or_builder is not None:
            self.parsed_payload_or_builder = parsed_payload_or_builder
        if connector_ref is not None:
            self.connector_ref = connector_ref
        if serialized_size is not None:
            self.serialized_size = serialized_size
        if parser_for_type is not None:
            self.parser_for_type = parser_for_type
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if source_type is not None:
            self.source_type = source_type
        if headers_map is not None:
            self.headers_map = headers_map
        if artifact_data is not None:
            self.artifact_data = artifact_data
        if manifest_data is not None:
            self.manifest_data = manifest_data
        if parsed_payload is not None:
            self.parsed_payload = parsed_payload
        if initialized is not None:
            self.initialized = initialized
        if headers is not None:
            self.headers = headers
        if all_fields is not None:
            self.all_fields = all_fields
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if memoized_serialized_size is not None:
            self.memoized_serialized_size = memoized_serialized_size

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this TriggerPayload.  # noqa: E501


        :return: The unknown_fields of this TriggerPayload.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this TriggerPayload.


        :param unknown_fields: The unknown_fields of this TriggerPayload.  # noqa: E501
        :type: UnknownFieldSet
        """

        self._unknown_fields = unknown_fields

    @property
    def type(self):
        """Gets the type of this TriggerPayload.  # noqa: E501


        :return: The type of this TriggerPayload.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TriggerPayload.


        :param type: The type of this TriggerPayload.  # noqa: E501
        :type: str
        """
        allowed_values = ["CUSTOM", "GIT", "SCHEDULED", "WEBHOOK", "ARTIFACT", "MANIFEST", "UNRECOGNIZED"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def version(self):
        """Gets the version of this TriggerPayload.  # noqa: E501


        :return: The version of this TriggerPayload.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this TriggerPayload.


        :param version: The version of this TriggerPayload.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def image_path(self):
        """Gets the image_path of this TriggerPayload.  # noqa: E501


        :return: The image_path of this TriggerPayload.  # noqa: E501
        :rtype: str
        """
        return self._image_path

    @image_path.setter
    def image_path(self, image_path):
        """Sets the image_path of this TriggerPayload.


        :param image_path: The image_path of this TriggerPayload.  # noqa: E501
        :type: str
        """

        self._image_path = image_path

    @property
    def type_value(self):
        """Gets the type_value of this TriggerPayload.  # noqa: E501


        :return: The type_value of this TriggerPayload.  # noqa: E501
        :rtype: int
        """
        return self._type_value

    @type_value.setter
    def type_value(self, type_value):
        """Sets the type_value of this TriggerPayload.


        :param type_value: The type_value of this TriggerPayload.  # noqa: E501
        :type: int
        """

        self._type_value = type_value

    @property
    def headers_count(self):
        """Gets the headers_count of this TriggerPayload.  # noqa: E501


        :return: The headers_count of this TriggerPayload.  # noqa: E501
        :rtype: int
        """
        return self._headers_count

    @headers_count.setter
    def headers_count(self, headers_count):
        """Sets the headers_count of this TriggerPayload.


        :param headers_count: The headers_count of this TriggerPayload.  # noqa: E501
        :type: int
        """

        self._headers_count = headers_count

    @property
    def source_type_value(self):
        """Gets the source_type_value of this TriggerPayload.  # noqa: E501


        :return: The source_type_value of this TriggerPayload.  # noqa: E501
        :rtype: int
        """
        return self._source_type_value

    @source_type_value.setter
    def source_type_value(self, source_type_value):
        """Sets the source_type_value of this TriggerPayload.


        :param source_type_value: The source_type_value of this TriggerPayload.  # noqa: E501
        :type: int
        """

        self._source_type_value = source_type_value

    @property
    def artifact_data_or_builder(self):
        """Gets the artifact_data_or_builder of this TriggerPayload.  # noqa: E501


        :return: The artifact_data_or_builder of this TriggerPayload.  # noqa: E501
        :rtype: ArtifactDataOrBuilder
        """
        return self._artifact_data_or_builder

    @artifact_data_or_builder.setter
    def artifact_data_or_builder(self, artifact_data_or_builder):
        """Sets the artifact_data_or_builder of this TriggerPayload.


        :param artifact_data_or_builder: The artifact_data_or_builder of this TriggerPayload.  # noqa: E501
        :type: ArtifactDataOrBuilder
        """

        self._artifact_data_or_builder = artifact_data_or_builder

    @property
    def manifest_data_or_builder(self):
        """Gets the manifest_data_or_builder of this TriggerPayload.  # noqa: E501


        :return: The manifest_data_or_builder of this TriggerPayload.  # noqa: E501
        :rtype: ManifestDataOrBuilder
        """
        return self._manifest_data_or_builder

    @manifest_data_or_builder.setter
    def manifest_data_or_builder(self, manifest_data_or_builder):
        """Sets the manifest_data_or_builder of this TriggerPayload.


        :param manifest_data_or_builder: The manifest_data_or_builder of this TriggerPayload.  # noqa: E501
        :type: ManifestDataOrBuilder
        """

        self._manifest_data_or_builder = manifest_data_or_builder

    @property
    def connector_ref_bytes(self):
        """Gets the connector_ref_bytes of this TriggerPayload.  # noqa: E501


        :return: The connector_ref_bytes of this TriggerPayload.  # noqa: E501
        :rtype: ByteString
        """
        return self._connector_ref_bytes

    @connector_ref_bytes.setter
    def connector_ref_bytes(self, connector_ref_bytes):
        """Sets the connector_ref_bytes of this TriggerPayload.


        :param connector_ref_bytes: The connector_ref_bytes of this TriggerPayload.  # noqa: E501
        :type: ByteString
        """

        self._connector_ref_bytes = connector_ref_bytes

    @property
    def image_path_bytes(self):
        """Gets the image_path_bytes of this TriggerPayload.  # noqa: E501


        :return: The image_path_bytes of this TriggerPayload.  # noqa: E501
        :rtype: ByteString
        """
        return self._image_path_bytes

    @image_path_bytes.setter
    def image_path_bytes(self, image_path_bytes):
        """Sets the image_path_bytes of this TriggerPayload.


        :param image_path_bytes: The image_path_bytes of this TriggerPayload.  # noqa: E501
        :type: ByteString
        """

        self._image_path_bytes = image_path_bytes

    @property
    def build_data_case(self):
        """Gets the build_data_case of this TriggerPayload.  # noqa: E501


        :return: The build_data_case of this TriggerPayload.  # noqa: E501
        :rtype: str
        """
        return self._build_data_case

    @build_data_case.setter
    def build_data_case(self, build_data_case):
        """Sets the build_data_case of this TriggerPayload.


        :param build_data_case: The build_data_case of this TriggerPayload.  # noqa: E501
        :type: str
        """
        allowed_values = ["ARTIFACTDATA", "MANIFESTDATA", "BUILDDATA_NOT_SET"]  # noqa: E501
        if build_data_case not in allowed_values:
            raise ValueError(
                "Invalid value for `build_data_case` ({0}), must be one of {1}"  # noqa: E501
                .format(build_data_case, allowed_values)
            )

        self._build_data_case = build_data_case

    @property
    def parsed_payload_or_builder(self):
        """Gets the parsed_payload_or_builder of this TriggerPayload.  # noqa: E501


        :return: The parsed_payload_or_builder of this TriggerPayload.  # noqa: E501
        :rtype: ParsedPayloadOrBuilder
        """
        return self._parsed_payload_or_builder

    @parsed_payload_or_builder.setter
    def parsed_payload_or_builder(self, parsed_payload_or_builder):
        """Sets the parsed_payload_or_builder of this TriggerPayload.


        :param parsed_payload_or_builder: The parsed_payload_or_builder of this TriggerPayload.  # noqa: E501
        :type: ParsedPayloadOrBuilder
        """

        self._parsed_payload_or_builder = parsed_payload_or_builder

    @property
    def connector_ref(self):
        """Gets the connector_ref of this TriggerPayload.  # noqa: E501


        :return: The connector_ref of this TriggerPayload.  # noqa: E501
        :rtype: str
        """
        return self._connector_ref

    @connector_ref.setter
    def connector_ref(self, connector_ref):
        """Sets the connector_ref of this TriggerPayload.


        :param connector_ref: The connector_ref of this TriggerPayload.  # noqa: E501
        :type: str
        """

        self._connector_ref = connector_ref

    @property
    def serialized_size(self):
        """Gets the serialized_size of this TriggerPayload.  # noqa: E501


        :return: The serialized_size of this TriggerPayload.  # noqa: E501
        :rtype: int
        """
        return self._serialized_size

    @serialized_size.setter
    def serialized_size(self, serialized_size):
        """Sets the serialized_size of this TriggerPayload.


        :param serialized_size: The serialized_size of this TriggerPayload.  # noqa: E501
        :type: int
        """

        self._serialized_size = serialized_size

    @property
    def parser_for_type(self):
        """Gets the parser_for_type of this TriggerPayload.  # noqa: E501


        :return: The parser_for_type of this TriggerPayload.  # noqa: E501
        :rtype: ParserTriggerPayload
        """
        return self._parser_for_type

    @parser_for_type.setter
    def parser_for_type(self, parser_for_type):
        """Sets the parser_for_type of this TriggerPayload.


        :param parser_for_type: The parser_for_type of this TriggerPayload.  # noqa: E501
        :type: ParserTriggerPayload
        """

        self._parser_for_type = parser_for_type

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this TriggerPayload.  # noqa: E501


        :return: The default_instance_for_type of this TriggerPayload.  # noqa: E501
        :rtype: TriggerPayload
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this TriggerPayload.


        :param default_instance_for_type: The default_instance_for_type of this TriggerPayload.  # noqa: E501
        :type: TriggerPayload
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def source_type(self):
        """Gets the source_type of this TriggerPayload.  # noqa: E501


        :return: The source_type of this TriggerPayload.  # noqa: E501
        :rtype: str
        """
        return self._source_type

    @source_type.setter
    def source_type(self, source_type):
        """Sets the source_type of this TriggerPayload.


        :param source_type: The source_type of this TriggerPayload.  # noqa: E501
        :type: str
        """
        allowed_values = ["CUSTOM_REPO", "GITHUB_REPO", "GITLAB_REPO", "BITBUCKET_REPO", "AWS_CODECOMMIT_REPO", "AZURE_REPO", "HARNESS_REPO", "UNRECOGNIZED"]  # noqa: E501
        if source_type not in allowed_values:
            raise ValueError(
                "Invalid value for `source_type` ({0}), must be one of {1}"  # noqa: E501
                .format(source_type, allowed_values)
            )

        self._source_type = source_type

    @property
    def headers_map(self):
        """Gets the headers_map of this TriggerPayload.  # noqa: E501


        :return: The headers_map of this TriggerPayload.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._headers_map

    @headers_map.setter
    def headers_map(self, headers_map):
        """Sets the headers_map of this TriggerPayload.


        :param headers_map: The headers_map of this TriggerPayload.  # noqa: E501
        :type: dict(str, str)
        """

        self._headers_map = headers_map

    @property
    def artifact_data(self):
        """Gets the artifact_data of this TriggerPayload.  # noqa: E501


        :return: The artifact_data of this TriggerPayload.  # noqa: E501
        :rtype: ArtifactData
        """
        return self._artifact_data

    @artifact_data.setter
    def artifact_data(self, artifact_data):
        """Sets the artifact_data of this TriggerPayload.


        :param artifact_data: The artifact_data of this TriggerPayload.  # noqa: E501
        :type: ArtifactData
        """

        self._artifact_data = artifact_data

    @property
    def manifest_data(self):
        """Gets the manifest_data of this TriggerPayload.  # noqa: E501


        :return: The manifest_data of this TriggerPayload.  # noqa: E501
        :rtype: ManifestData
        """
        return self._manifest_data

    @manifest_data.setter
    def manifest_data(self, manifest_data):
        """Sets the manifest_data of this TriggerPayload.


        :param manifest_data: The manifest_data of this TriggerPayload.  # noqa: E501
        :type: ManifestData
        """

        self._manifest_data = manifest_data

    @property
    def parsed_payload(self):
        """Gets the parsed_payload of this TriggerPayload.  # noqa: E501


        :return: The parsed_payload of this TriggerPayload.  # noqa: E501
        :rtype: ParsedPayload
        """
        return self._parsed_payload

    @parsed_payload.setter
    def parsed_payload(self, parsed_payload):
        """Sets the parsed_payload of this TriggerPayload.


        :param parsed_payload: The parsed_payload of this TriggerPayload.  # noqa: E501
        :type: ParsedPayload
        """

        self._parsed_payload = parsed_payload

    @property
    def initialized(self):
        """Gets the initialized of this TriggerPayload.  # noqa: E501


        :return: The initialized of this TriggerPayload.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this TriggerPayload.


        :param initialized: The initialized of this TriggerPayload.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def headers(self):
        """Gets the headers of this TriggerPayload.  # noqa: E501


        :return: The headers of this TriggerPayload.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._headers

    @headers.setter
    def headers(self, headers):
        """Sets the headers of this TriggerPayload.


        :param headers: The headers of this TriggerPayload.  # noqa: E501
        :type: dict(str, str)
        """

        self._headers = headers

    @property
    def all_fields(self):
        """Gets the all_fields of this TriggerPayload.  # noqa: E501


        :return: The all_fields of this TriggerPayload.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this TriggerPayload.


        :param all_fields: The all_fields of this TriggerPayload.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this TriggerPayload.  # noqa: E501


        :return: The descriptor_for_type of this TriggerPayload.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this TriggerPayload.


        :param descriptor_for_type: The descriptor_for_type of this TriggerPayload.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this TriggerPayload.  # noqa: E501


        :return: The initialization_error_string of this TriggerPayload.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this TriggerPayload.


        :param initialization_error_string: The initialization_error_string of this TriggerPayload.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def memoized_serialized_size(self):
        """Gets the memoized_serialized_size of this TriggerPayload.  # noqa: E501


        :return: The memoized_serialized_size of this TriggerPayload.  # noqa: E501
        :rtype: int
        """
        return self._memoized_serialized_size

    @memoized_serialized_size.setter
    def memoized_serialized_size(self, memoized_serialized_size):
        """Sets the memoized_serialized_size of this TriggerPayload.


        :param memoized_serialized_size: The memoized_serialized_size of this TriggerPayload.  # noqa: E501
        :type: int
        """

        self._memoized_serialized_size = memoized_serialized_size

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
        if issubclass(TriggerPayload, dict):
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
        if not isinstance(other, TriggerPayload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
