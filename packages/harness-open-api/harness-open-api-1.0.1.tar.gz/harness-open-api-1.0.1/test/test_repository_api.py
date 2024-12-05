# coding: utf-8

"""
    Harness NextGen Software Delivery Platform API Reference

    The Harness Software Delivery Platform uses OpenAPI Specification v3.0. Harness constantly improves these APIs. Please be aware that some improvements could cause breaking changes. # Introduction     The Harness API allows you to integrate and use all the services and modules we provide on the Harness Platform. If you use client-side SDKs, Harness functionality can be integrated with your client-side automation, helping you reduce manual efforts and deploy code faster.    For more information about how Harness works, read our [documentation](https://developer.harness.io/docs/getting-started) or visit the [Harness Developer Hub](https://developer.harness.io/).  ## How it works    The Harness API is a RESTful API that uses standard HTTP verbs. You can send requests in JSON, YAML, or form-data format. The format of the response matches the format of your request. You must send a single request at a time and ensure that you include your authentication key. For more information about this, go to [Authentication](#section/Introduction/Authentication).  ## Get started    Before you start integrating, get to know our API better by reading the following topics:    * [Harness key concepts](https://developer.harness.io/docs/getting-started/learn-harness-key-concepts/)   * [Authentication](#section/Introduction/Authentication)   * [Requests and responses](#section/Introduction/Requests-and-Responses)   * [Common Parameters](#section/Introduction/Common-Parameters-Beta)   * [Status Codes](#section/Introduction/Status-Codes)   * [Errors](#tag/Error-Response)   * [Versioning](#section/Introduction/Versioning-Beta)   * [Pagination](/#section/Introduction/Pagination-Beta)    The methods you need to integrate with depend on the functionality you want to use. Work with  your Harness Solutions Engineer to determine which methods you need.  ## Authentication  To authenticate with the Harness API, you need to:   1. Generate an API token on the Harness Platform.   2. Send the API token you generate in the `x-api-key` header in each request.  ### Generate an API token  To generate an API token, complete the following steps:   1. Go to the [Harness Platform](https://app.harness.io/).   2. On the left-hand navigation, click **My Profile**.   3. Click **+API Key**, enter a name for your key and then click **Save**.   4. Within the API Key tile, click **+Token**.   5. Enter a name for your token and click **Generate Token**. **Important**: Make sure to save your token securely. Harness does not store the API token for future reference, so make sure to save your token securely before you leave the page.  ### Send the API token in your requests  Send the token you created in the Harness Platform in the x-api-key header. For example:   `x-api-key: YOUR_API_KEY_HERE`  ## Requests and Responses    The structure for each request and response is outlined in the API documentation. We have examples in JSON and YAML for every request and response. You can use our online editor to test the examples.  ## Common Parameters [Beta]  | Field Name | Type    | Default | Description    | |------------|---------|---------|----------------| | identifier | string  | none    | URL-friendly version of the name, used to identify a resource within it's scope and so needs to be unique within the scope.                                                                                                            | | name       | string  | none    | Human-friendly name for the resource.                                                                                       | | org        | string  | none    | Limit to provided org identifiers.                                                                                                                     | | project    | string  | none    | Limit to provided project identifiers.                                                                                                                 | | description| string  | none    | More information about the specific resource.                                                                                    | | tags       | map[string]string  | none    | List of labels applied to the resource.                                                                                                                         | | order      | string  | desc    | Order to use when sorting the specified fields. Type: enum(asc,desc).                                                                                                                                     | | sort       | string  | none    | Fields on which to sort. Note: Specify the fields that you want to use for sorting. When doing so, consider the operational overhead of sorting fields. | | limit      | int     | 30      | Pagination: Number of items to return.                                                                                                                 | | page       | int     | 1       | Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page.                  | | created    | int64   | none    | Unix timestamp that shows when the resource was created (in milliseconds).                                                               | | updated    | int64   | none    | Unix timestamp that shows when the resource was last edited (in milliseconds).                                                           |   ## Status Codes    Harness uses conventional HTTP status codes to indicate the status of an API request.    Generally, 2xx responses are reserved for success and 4xx status codes are reserved for failures. A 5xx response code indicates an error on the Harness server.    | Error Code  | Description |   |-------------|-------------|   | 200         |     OK      |   | 201         |   Created   |   | 202         |   Accepted  |   | 204         |  No Content |   | 400         | Bad Request |   | 401         | Unauthorized |   | 403         | Forbidden |   | 412         | Precondition Failed |   | 415         | Unsupported Media Type |   | 500         | Server Error |    To view our error response structures, go [here](#tag/Error-Response).  ## Versioning [Beta]  ### Harness Version   The current version of our Beta APIs is yet to be announced. The version number will use the date-header format and will be valid only for our Beta APIs.  ### Generation   All our beta APIs are versioned as a Generation, and this version is included in the path to every API resource. For example, v1 beta APIs begin with `app.harness.io/v1/`, where v1 is the API Generation.    The version number represents the core API and does not change frequently. The version number changes only if there is a significant departure from the basic underpinnings of the existing API. For example, when Harness performs a system-wide refactoring of core concepts or resources.  ## Pagination [Beta]  We use pagination to place limits on the number of responses associated with list endpoints. Pagination is achieved by the use of limit query parameters. The limit defaults to 30. Its maximum value is 100.  Following are the pagination headers supported in the response bodies of paginated APIs:   1. X-Total-Elements : Indicates the total number of entries in a paginated response.   2. X-Page-Number : Indicates the page number currently returned for a paginated response.   3. X-Page-Size : Indicates the number of entries per page for a paginated response.  For example:    ``` X-Total-Elements : 30 X-Page-Number : 0 X-Page-Size : 10   ```   # noqa: E501

    OpenAPI spec version: 1.0
    Contact: contact@harness.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import harness_open_api
from harness_open_api.api.repository_api import RepositoryApi  # noqa: E501
from harness_open_api.rest import ApiException


class TestRepositoryApi(unittest.TestCase):
    """RepositoryApi unit test stubs"""

    def setUp(self):
        self.api = RepositoryApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_archive(self):
        """Test case for archive

        Download repo in archived format  # noqa: E501
        """
        pass

    def test_calculate_commit_divergence(self):
        """Test case for calculate_commit_divergence

        Get commit divergence  # noqa: E501
        """
        pass

    def test_code_owners_validate(self):
        """Test case for code_owners_validate

        Validate code owners file  # noqa: E501
        """
        pass

    def test_commit_files(self):
        """Test case for commit_files

        Commit files  # noqa: E501
        """
        pass

    def test_create_branch(self):
        """Test case for create_branch

        Create branch  # noqa: E501
        """
        pass

    def test_create_repository(self):
        """Test case for create_repository

        Create repository  # noqa: E501
        """
        pass

    def test_create_tag(self):
        """Test case for create_tag

        Create tag  # noqa: E501
        """
        pass

    def test_delete_branch(self):
        """Test case for delete_branch

        Delete branch  # noqa: E501
        """
        pass

    def test_delete_repository(self):
        """Test case for delete_repository

        Soft delete repository  # noqa: E501
        """
        pass

    def test_delete_tag(self):
        """Test case for delete_tag

        Delete tag  # noqa: E501
        """
        pass

    def test_diff_stats(self):
        """Test case for diff_stats

        Get diff stats  # noqa: E501
        """
        pass

    def test_find_general_settings(self):
        """Test case for find_general_settings

        Get general settings  # noqa: E501
        """
        pass

    def test_find_security_settings(self):
        """Test case for find_security_settings

        Get security settings  # noqa: E501
        """
        pass

    def test_get_blame(self):
        """Test case for get_blame

        Get git blame  # noqa: E501
        """
        pass

    def test_get_branch(self):
        """Test case for get_branch

        Get branch  # noqa: E501
        """
        pass

    def test_get_commit(self):
        """Test case for get_commit

        Get commit  # noqa: E501
        """
        pass

    def test_get_commit_diff(self):
        """Test case for get_commit_diff

        Get raw git diff of a commit  # noqa: E501
        """
        pass

    def test_get_content(self):
        """Test case for get_content

        Get content of a file  # noqa: E501
        """
        pass

    def test_get_raw(self):
        """Test case for get_raw

        Get raw file content  # noqa: E501
        """
        pass

    def test_get_repository(self):
        """Test case for get_repository

        Get repository  # noqa: E501
        """
        pass

    def test_import_repository(self):
        """Test case for import_repository

        Import repository  # noqa: E501
        """
        pass

    def test_list_branches(self):
        """Test case for list_branches

        List branches  # noqa: E501
        """
        pass

    def test_list_commits(self):
        """Test case for list_commits

        List commits  # noqa: E501
        """
        pass

    def test_list_paths(self):
        """Test case for list_paths

        List all paths  # noqa: E501
        """
        pass

    def test_list_repos(self):
        """Test case for list_repos

        List repositories  # noqa: E501
        """
        pass

    def test_list_tags(self):
        """Test case for list_tags

        List tags  # noqa: E501
        """
        pass

    def test_merge_check(self):
        """Test case for merge_check

        Check mergeability  # noqa: E501
        """
        pass

    def test_path_details(self):
        """Test case for path_details

        Get commit details  # noqa: E501
        """
        pass

    def test_purge_repository(self):
        """Test case for purge_repository

        Purge repository  # noqa: E501
        """
        pass

    def test_raw_diff(self):
        """Test case for raw_diff

        Get raw diff  # noqa: E501
        """
        pass

    def test_raw_diff_post(self):
        """Test case for raw_diff_post

        Get raw diff  # noqa: E501
        """
        pass

    def test_rebase_branch(self):
        """Test case for rebase_branch

        Rebase a branch relative to another branch or a commit  # noqa: E501
        """
        pass

    def test_restore_repository(self):
        """Test case for restore_repository

        Restore repository  # noqa: E501
        """
        pass

    def test_rule_add(self):
        """Test case for rule_add

        Add protection rule  # noqa: E501
        """
        pass

    def test_rule_delete(self):
        """Test case for rule_delete

        Delete protection rule  # noqa: E501
        """
        pass

    def test_rule_get(self):
        """Test case for rule_get

        Get protection rule  # noqa: E501
        """
        pass

    def test_rule_list(self):
        """Test case for rule_list

        List protection rules  # noqa: E501
        """
        pass

    def test_rule_update(self):
        """Test case for rule_update

        Update protection rule  # noqa: E501
        """
        pass

    def test_squash_branch(self):
        """Test case for squash_branch

        Squashes commits in a branch relative to another branch or a commit  # noqa: E501
        """
        pass

    def test_summary(self):
        """Test case for summary

        Get repository summary  # noqa: E501
        """
        pass

    def test_update_default_branch(self):
        """Test case for update_default_branch

        Update default branch  # noqa: E501
        """
        pass

    def test_update_general_settings(self):
        """Test case for update_general_settings

        Update general settings  # noqa: E501
        """
        pass

    def test_update_repository(self):
        """Test case for update_repository

        Update repository  # noqa: E501
        """
        pass

    def test_update_security_settings(self):
        """Test case for update_security_settings

        Update security settings  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
