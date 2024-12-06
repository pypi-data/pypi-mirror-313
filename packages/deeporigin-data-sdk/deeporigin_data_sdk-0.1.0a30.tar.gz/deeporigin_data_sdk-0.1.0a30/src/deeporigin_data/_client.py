# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, List, Union, Mapping, Iterable
from typing_extensions import Self, Literal, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from .types import (
    client_list_rows_params,
    client_list_files_params,
    client_delete_rows_params,
    client_ensure_rows_params,
    client_import_rows_params,
    client_describe_row_params,
    client_archive_files_params,
    client_describe_file_params,
    client_list_mentions_params,
    client_lock_database_params,
    client_create_database_params,
    client_delete_database_params,
    client_unlock_database_params,
    client_update_database_params,
    client_create_workspace_params,
    client_delete_workspace_params,
    client_update_workspace_params,
    client_chat_send_message_params,
    client_convert_id_format_params,
    client_describe_database_params,
    client_execute_code_sync_params,
    client_chat_create_thread_params,
    client_chat_list_messages_params,
    client_create_file_upload_params,
    client_describe_workspace_params,
    client_execute_code_async_params,
    client_list_database_rows_params,
    client_add_database_column_params,
    client_delete_database_column_params,
    client_update_database_column_params,
    client_describe_code_execution_params,
    client_describe_database_stats_params,
    client_create_file_download_url_params,
    client_list_row_back_references_params,
    client_parse_base_sequence_data_params,
    client_get_code_execution_result_params,
    client_configure_column_select_options_params,
    client_list_database_column_unique_values_v2_params,
)
from ._types import (
    NOT_GIVEN,
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NoneType,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    maybe_transform,
    get_async_library,
    async_maybe_transform,
)
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, DeeporiginDataError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)
from .types.list_rows_response import ListRowsResponse
from .types.list_files_response import ListFilesResponse
from .types.delete_rows_response import DeleteRowsResponse
from .types.ensure_rows_response import EnsureRowsResponse
from .types.import_rows_response import ImportRowsResponse
from .types.describe_file_response import DescribeFileResponse
from .types.list_mentions_response import ListMentionsResponse
from .types.lock_database_response import LockDatabaseResponse
from .types.create_database_response import CreateDatabaseResponse
from .types.delete_database_response import DeleteDatabaseResponse
from .types.unlock_database_response import UnlockDatabaseResponse
from .types.update_database_response import UpdateDatabaseResponse
from .types.create_workspace_response import CreateWorkspaceResponse
from .types.delete_workspace_response import DeleteWorkspaceResponse
from .types.update_workspace_response import UpdateWorkspaceResponse
from .types.convert_id_format_response import ConvertIDFormatResponse
from .types.describe_database_response import DescribeDatabaseResponse
from .types.execute_code_sync_response import ExecuteCodeSyncResponse
from .types.chat_create_thread_response import ChatCreateThreadResponse
from .types.chat_list_messages_response import ChatListMessagesResponse
from .types.create_file_upload_response import CreateFileUploadResponse
from .types.describe_workspace_response import DescribeWorkspaceResponse
from .types.execute_code_async_response import ExecuteCodeAsyncResponse
from .types.list_database_rows_response import ListDatabaseRowsResponse
from .types.add_database_column_response import AddDatabaseColumnResponse
from .types.shared.describe_row_response import DescribeRowResponse
from .types.delete_database_column_response import DeleteDatabaseColumnResponse
from .types.update_database_column_response import UpdateDatabaseColumnResponse
from .types.describe_code_execution_response import DescribeCodeExecutionResponse
from .types.describe_database_stats_response import DescribeDatabaseStatsResponse
from .types.create_file_download_url_response import CreateFileDownloadURLResponse
from .types.list_row_back_references_response import ListRowBackReferencesResponse
from .types.parse_base_sequence_data_response import ParseBaseSequenceDataResponse
from .types.configure_column_select_options_response import ConfigureColumnSelectOptionsResponse
from .types.list_database_column_unique_values_v2_response import ListDatabaseColumnUniqueValuesV2Response

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "DeeporiginData",
    "AsyncDeeporiginData",
    "Client",
    "AsyncClient",
]


class DeeporiginData(SyncAPIClient):
    with_raw_response: DeeporiginDataWithRawResponse
    with_streaming_response: DeeporiginDataWithStreamedResponse

    # client options
    token: str
    org_id: str

    def __init__(
        self,
        *,
        token: str | None = None,
        org_id: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous deeporigin_data client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `token` from `ORG_BEARER_TOKEN`
        - `org_id` from `ORG_ID`
        """
        if token is None:
            token = os.environ.get("ORG_BEARER_TOKEN")
        if token is None:
            raise DeeporiginDataError(
                "The token client option must be set either by passing token to the client or by setting the ORG_BEARER_TOKEN environment variable"
            )
        self.token = token

        if org_id is None:
            org_id = os.environ.get("ORG_ID")
        if org_id is None:
            raise DeeporiginDataError(
                "The org_id client option must be set either by passing org_id to the client or by setting the ORG_ID environment variable"
            )
        self.org_id = org_id

        if base_url is None:
            base_url = os.environ.get("DEEPORIGIN_DATA_BASE_URL")
        if base_url is None:
            base_url = f"https://os.edge.deeporigin.io/nucleus-api/api"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.with_raw_response = DeeporiginDataWithRawResponse(self)
        self.with_streaming_response = DeeporiginDataWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        token = self.token
        return {"Authorization": f"Bearer {token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "x-org-id": self.org_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        token: str | None = None,
        org_id: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            token=token or self.token,
            org_id=org_id or self.org_id,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def add_database_column(
        self,
        *,
        column: client_add_database_column_params.Column,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddDatabaseColumnResponse:
        """
        Add a column to a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/AddDatabaseColumn",
            body=maybe_transform(
                {
                    "column": column,
                    "database_id": database_id,
                },
                client_add_database_column_params.ClientAddDatabaseColumnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AddDatabaseColumnResponse,
        )

    def archive_files(
        self,
        *,
        file_ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Archive files by their ids.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ArchiveFiles",
            body=maybe_transform({"file_ids": file_ids}, client_archive_files_params.ClientArchiveFilesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def chat_create_thread(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCreateThreadResponse:
        """
        Create a new chat thread.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/CreateChatThread",
            body=maybe_transform(body, client_chat_create_thread_params.ClientChatCreateThreadParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCreateThreadResponse,
        )

    def chat_list_messages(
        self,
        *,
        thread_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatListMessagesResponse:
        """
        List messages in a chat thread.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ListChatThreadMessages",
            body=maybe_transform(
                {"thread_id": thread_id}, client_chat_list_messages_params.ClientChatListMessagesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatListMessagesResponse,
        )

    def chat_send_message(
        self,
        *,
        messages: Iterable[client_chat_send_message_params.Message],
        thread_id: str,
        context: client_chat_send_message_params.Context | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Send a chat message to the Deep Origin assistant and streams results via SSE.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self.post(
            "/SendChatMessage",
            body=maybe_transform(
                {
                    "messages": messages,
                    "thread_id": thread_id,
                    "context": context,
                },
                client_chat_send_message_params.ClientChatSendMessageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def configure_column_select_options(
        self,
        *,
        column_id: str,
        database_id: str,
        option_configuration: Iterable[client_configure_column_select_options_params.OptionConfiguration],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigureColumnSelectOptionsResponse:
        """Configure column select options.

        Supports both adding and removing options.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ConfigureColumnSelectOptions",
            body=maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                    "option_configuration": option_configuration,
                },
                client_configure_column_select_options_params.ClientConfigureColumnSelectOptionsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigureColumnSelectOptionsResponse,
        )

    def convert_id_format(
        self,
        *,
        conversions: Iterable[client_convert_id_format_params.Conversion],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConvertIDFormatResponse:
        """
        Converts between system IDs and human IDs (HIDs).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ConvertIdFormat",
            body=maybe_transform(
                {"conversions": conversions}, client_convert_id_format_params.ClientConvertIDFormatParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConvertIDFormatResponse,
        )

    def create_database(
        self,
        *,
        database: client_create_database_params.Database,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateDatabaseResponse:
        """
        Create a new database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/CreateDatabase",
            body=maybe_transform({"database": database}, client_create_database_params.ClientCreateDatabaseParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateDatabaseResponse,
        )

    def create_file_download_url(
        self,
        *,
        file_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateFileDownloadURLResponse:
        """
        Returns a pre-signed S3 URL.

        Args:
          file_id: Deep Origin system ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/CreateFileDownloadUrl",
            body=maybe_transform(
                {"file_id": file_id}, client_create_file_download_url_params.ClientCreateFileDownloadURLParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateFileDownloadURLResponse,
        )

    def create_file_upload(
        self,
        *,
        content_length: str,
        name: str,
        checksum_sha256: str | NotGiven = NOT_GIVEN,
        content_type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateFileUploadResponse:
        """Create a file upload URL.

        Typically this is creating a pre-signed S3 URL.

        Args:
          checksum_sha256: Base64 encoded SHA256 checksum of the file.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/CreateFileUpload",
            body=maybe_transform(
                {
                    "content_length": content_length,
                    "name": name,
                    "checksum_sha256": checksum_sha256,
                    "content_type": content_type,
                },
                client_create_file_upload_params.ClientCreateFileUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateFileUploadResponse,
        )

    def create_workspace(
        self,
        *,
        workspace: client_create_workspace_params.Workspace,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateWorkspaceResponse:
        """
        Create a new workspace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/CreateWorkspace",
            body=maybe_transform({"workspace": workspace}, client_create_workspace_params.ClientCreateWorkspaceParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateWorkspaceResponse,
        )

    def delete_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteDatabaseResponse:
        """
        Permanently deletes a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DeleteDatabase",
            body=maybe_transform(
                {"database_id": database_id}, client_delete_database_params.ClientDeleteDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteDatabaseResponse,
        )

    def delete_database_column(
        self,
        *,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteDatabaseColumnResponse:
        """
        Delete a column from a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DeleteDatabaseColumn",
            body=maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_delete_database_column_params.ClientDeleteDatabaseColumnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteDatabaseColumnResponse,
        )

    def delete_rows(
        self,
        *,
        database_id: str,
        delete_all: bool | NotGiven = NOT_GIVEN,
        row_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteRowsResponse:
        """
        Delete rows by their ids.

        Args:
          delete_all: When true, deletes all rows in the table except rows with the specified
              `rowIds`.

          row_ids: List of row IDs to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DeleteRows",
            body=maybe_transform(
                {
                    "database_id": database_id,
                    "delete_all": delete_all,
                    "row_ids": row_ids,
                },
                client_delete_rows_params.ClientDeleteRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteRowsResponse,
        )

    def delete_workspace(
        self,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteWorkspaceResponse:
        """
        Permanently deletes a workspace and all its children.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DeleteWorkspace",
            body=maybe_transform(
                {"workspace_id": workspace_id}, client_delete_workspace_params.ClientDeleteWorkspaceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteWorkspaceResponse,
        )

    def describe_code_execution(
        self,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeCodeExecutionResponse:
        """
        Returns information about a particular code execution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DescribeCodeExecution",
            body=maybe_transform({"id": id}, client_describe_code_execution_params.ClientDescribeCodeExecutionParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeCodeExecutionResponse,
        )

    def describe_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeDatabaseResponse:
        """
        Describe a database

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DescribeDatabase",
            body=maybe_transform(
                {"database_id": database_id}, client_describe_database_params.ClientDescribeDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeDatabaseResponse,
        )

    def describe_database_stats(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeDatabaseStatsResponse:
        """
        Returns aggregation information about a particular database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DescribeDatabaseStats",
            body=maybe_transform(
                {"database_id": database_id}, client_describe_database_stats_params.ClientDescribeDatabaseStatsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeDatabaseStatsResponse,
        )

    def describe_file(
        self,
        *,
        file_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeFileResponse:
        """
        Describe a file by its ID.

        Args:
          file_id: Deep Origin system ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DescribeFile",
            body=maybe_transform({"file_id": file_id}, client_describe_file_params.ClientDescribeFileParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeFileResponse,
        )

    def describe_row(
        self,
        *,
        row_id: str,
        column_selection: client_describe_row_params.ColumnSelection | NotGiven = NOT_GIVEN,
        fields: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeRowResponse:
        """Deprecated.

        Use DescribeDatabaseRow, DescribeDatabase, or DescribeWorkspace
        instead.

        Args:
          column_selection: Select columns for inclusion/exclusion.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DescribeRow",
            body=maybe_transform(
                {
                    "row_id": row_id,
                    "column_selection": column_selection,
                    "fields": fields,
                },
                client_describe_row_params.ClientDescribeRowParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeRowResponse,
        )

    def describe_workspace(
        self,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeWorkspaceResponse:
        """
        Describe a workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/DescribeWorkspace",
            body=maybe_transform(
                {"workspace_id": workspace_id}, client_describe_workspace_params.ClientDescribeWorkspaceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeWorkspaceResponse,
        )

    def download_file(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Returns a 303 redirect to a pre-signed S3 URL."""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self.get(
            "/DownloadFile",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def ensure_rows(
        self,
        *,
        database_id: str,
        rows: Iterable[client_ensure_rows_params.Row],
        check_previous_value: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnsureRowsResponse:
        """Either creates or updates an existing row.

        Supports updates to both system and
        user defined columns.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/EnsureRows",
            body=maybe_transform(
                {
                    "database_id": database_id,
                    "rows": rows,
                    "check_previous_value": check_previous_value,
                },
                client_ensure_rows_params.ClientEnsureRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnsureRowsResponse,
        )

    def execute_code_async(
        self,
        *,
        code: str,
        code_language: Literal["python"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExecuteCodeAsyncResponse:
        """
        Execute code asynchronously.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ExecuteCode",
            body=maybe_transform(
                {
                    "code": code,
                    "code_language": code_language,
                },
                client_execute_code_async_params.ClientExecuteCodeAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecuteCodeAsyncResponse,
        )

    def execute_code_sync(
        self,
        *,
        code: str,
        code_language: Literal["python"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExecuteCodeSyncResponse:
        """
        Execute code synchronously.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ExecuteCodeSync",
            body=maybe_transform(
                {
                    "code": code,
                    "code_language": code_language,
                },
                client_execute_code_sync_params.ClientExecuteCodeSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecuteCodeSyncResponse,
        )

    def get_code_execution_result(
        self,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Returns the result of a code execution.

        Args:
          id: Deep Origin system ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/GetCodeExecutionResult",
            body=maybe_transform(
                {"id": id}, client_get_code_execution_result_params.ClientGetCodeExecutionResultParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def import_rows(
        self,
        *,
        database_id: str,
        add_columns: Iterable[client_import_rows_params.AddColumn] | NotGiven = NOT_GIVEN,
        creation_block_id: str | NotGiven = NOT_GIVEN,
        creation_parent_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ImportRowsResponse:
        """
        Creates new rows from CSV data.

        Args:
          add_columns: Optionally add additional columns to the database during import.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ImportRows",
            body=maybe_transform(
                {
                    "database_id": database_id,
                    "add_columns": add_columns,
                    "creation_block_id": creation_block_id,
                    "creation_parent_id": creation_parent_id,
                },
                client_import_rows_params.ClientImportRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImportRowsResponse,
        )

    def list_database_column_unique_values_v2(
        self,
        *,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListDatabaseColumnUniqueValuesV2Response:
        """
        Returns the unique values for every cell within the column.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ListDatabaseColumnUniqueValuesV2",
            body=maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_list_database_column_unique_values_v2_params.ClientListDatabaseColumnUniqueValuesV2Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListDatabaseColumnUniqueValuesV2Response,
        )

    def list_database_rows(
        self,
        *,
        database_row_id: str,
        column_selection: client_list_database_rows_params.ColumnSelection | NotGiven = NOT_GIVEN,
        filter: client_list_database_rows_params.Filter | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        row_sort: Iterable[client_list_database_rows_params.RowSort] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListDatabaseRowsResponse:
        """
        List database rows with full row data.

        Args:
          column_selection: Select columns for inclusion/exclusion.

          row_sort: Sort rows by column.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ListDatabaseRows",
            body=maybe_transform(
                {
                    "database_row_id": database_row_id,
                    "column_selection": column_selection,
                    "filter": filter,
                    "limit": limit,
                    "offset": offset,
                    "row_sort": row_sort,
                },
                client_list_database_rows_params.ClientListDatabaseRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListDatabaseRowsResponse,
        )

    def list_files(
        self,
        *,
        filters: Iterable[client_list_files_params.Filter] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListFilesResponse:
        """
        Returns a list of files using the filters.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ListFiles",
            body=maybe_transform({"filters": filters}, client_list_files_params.ClientListFilesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListFilesResponse,
        )

    def list_mentions(
        self,
        *,
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListMentionsResponse:
        """
        Returns entities that can be mentioned in a notebook.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ListMentions",
            body=maybe_transform({"query": query}, client_list_mentions_params.ClientListMentionsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListMentionsResponse,
        )

    def list_row_back_references(
        self,
        *,
        database_id: str,
        row_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListRowBackReferencesResponse:
        """
        Finds all the places a row is referenced.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ListRowBackReferences",
            body=maybe_transform(
                {
                    "database_id": database_id,
                    "row_id": row_id,
                },
                client_list_row_back_references_params.ClientListRowBackReferencesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListRowBackReferencesResponse,
        )

    def list_rows(
        self,
        *,
        filters: Iterable[client_list_rows_params.Filter],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListRowsResponse:
        """
        Lists rows at a given depth in the hierarchy.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ListRows",
            body=maybe_transform({"filters": filters}, client_list_rows_params.ClientListRowsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListRowsResponse,
        )

    def lock_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LockDatabaseResponse:
        """
        A locked database cannot be edited.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/LockDatabase",
            body=maybe_transform({"database_id": database_id}, client_lock_database_params.ClientLockDatabaseParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LockDatabaseResponse,
        )

    def parse_base_sequence_data(
        self,
        *,
        file_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParseBaseSequenceDataResponse:
        """
        Parses a base sequence file and returns the parsed result.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/ParseBaseSequenceData",
            body=maybe_transform(
                {"file_id": file_id}, client_parse_base_sequence_data_params.ClientParseBaseSequenceDataParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseBaseSequenceDataResponse,
        )

    def unlock_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnlockDatabaseResponse:
        """
        An unlocked database can be edited.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/UnlockDatabase",
            body=maybe_transform(
                {"database_id": database_id}, client_unlock_database_params.ClientUnlockDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UnlockDatabaseResponse,
        )

    def update_database(
        self,
        *,
        id: str,
        database: client_update_database_params.Database,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateDatabaseResponse:
        """
        Update a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/UpdateDatabase",
            body=maybe_transform(
                {
                    "id": id,
                    "database": database,
                },
                client_update_database_params.ClientUpdateDatabaseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UpdateDatabaseResponse,
        )

    def update_database_column(
        self,
        *,
        column: client_update_database_column_params.Column,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateDatabaseColumnResponse:
        """
        Update a column in a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/UpdateDatabaseColumn",
            body=maybe_transform(
                {
                    "column": column,
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_update_database_column_params.ClientUpdateDatabaseColumnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UpdateDatabaseColumnResponse,
        )

    def update_workspace(
        self,
        *,
        id: str,
        workspace: client_update_workspace_params.Workspace,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateWorkspaceResponse:
        """
        Update a workspace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.post(
            "/UpdateWorkspace",
            body=maybe_transform(
                {
                    "id": id,
                    "workspace": workspace,
                },
                client_update_workspace_params.ClientUpdateWorkspaceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UpdateWorkspaceResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncDeeporiginData(AsyncAPIClient):
    with_raw_response: AsyncDeeporiginDataWithRawResponse
    with_streaming_response: AsyncDeeporiginDataWithStreamedResponse

    # client options
    token: str
    org_id: str

    def __init__(
        self,
        *,
        token: str | None = None,
        org_id: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async deeporigin_data client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `token` from `ORG_BEARER_TOKEN`
        - `org_id` from `ORG_ID`
        """
        if token is None:
            token = os.environ.get("ORG_BEARER_TOKEN")
        if token is None:
            raise DeeporiginDataError(
                "The token client option must be set either by passing token to the client or by setting the ORG_BEARER_TOKEN environment variable"
            )
        self.token = token

        if org_id is None:
            org_id = os.environ.get("ORG_ID")
        if org_id is None:
            raise DeeporiginDataError(
                "The org_id client option must be set either by passing org_id to the client or by setting the ORG_ID environment variable"
            )
        self.org_id = org_id

        if base_url is None:
            base_url = os.environ.get("DEEPORIGIN_DATA_BASE_URL")
        if base_url is None:
            base_url = f"https://os.edge.deeporigin.io/nucleus-api/api"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.with_raw_response = AsyncDeeporiginDataWithRawResponse(self)
        self.with_streaming_response = AsyncDeeporiginDataWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        token = self.token
        return {"Authorization": f"Bearer {token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "x-org-id": self.org_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        token: str | None = None,
        org_id: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            token=token or self.token,
            org_id=org_id or self.org_id,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def add_database_column(
        self,
        *,
        column: client_add_database_column_params.Column,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddDatabaseColumnResponse:
        """
        Add a column to a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/AddDatabaseColumn",
            body=await async_maybe_transform(
                {
                    "column": column,
                    "database_id": database_id,
                },
                client_add_database_column_params.ClientAddDatabaseColumnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AddDatabaseColumnResponse,
        )

    async def archive_files(
        self,
        *,
        file_ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Archive files by their ids.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ArchiveFiles",
            body=await async_maybe_transform(
                {"file_ids": file_ids}, client_archive_files_params.ClientArchiveFilesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def chat_create_thread(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCreateThreadResponse:
        """
        Create a new chat thread.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/CreateChatThread",
            body=await async_maybe_transform(body, client_chat_create_thread_params.ClientChatCreateThreadParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCreateThreadResponse,
        )

    async def chat_list_messages(
        self,
        *,
        thread_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatListMessagesResponse:
        """
        List messages in a chat thread.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ListChatThreadMessages",
            body=await async_maybe_transform(
                {"thread_id": thread_id}, client_chat_list_messages_params.ClientChatListMessagesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatListMessagesResponse,
        )

    async def chat_send_message(
        self,
        *,
        messages: Iterable[client_chat_send_message_params.Message],
        thread_id: str,
        context: client_chat_send_message_params.Context | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Send a chat message to the Deep Origin assistant and streams results via SSE.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self.post(
            "/SendChatMessage",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "thread_id": thread_id,
                    "context": context,
                },
                client_chat_send_message_params.ClientChatSendMessageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def configure_column_select_options(
        self,
        *,
        column_id: str,
        database_id: str,
        option_configuration: Iterable[client_configure_column_select_options_params.OptionConfiguration],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigureColumnSelectOptionsResponse:
        """Configure column select options.

        Supports both adding and removing options.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ConfigureColumnSelectOptions",
            body=await async_maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                    "option_configuration": option_configuration,
                },
                client_configure_column_select_options_params.ClientConfigureColumnSelectOptionsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigureColumnSelectOptionsResponse,
        )

    async def convert_id_format(
        self,
        *,
        conversions: Iterable[client_convert_id_format_params.Conversion],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConvertIDFormatResponse:
        """
        Converts between system IDs and human IDs (HIDs).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ConvertIdFormat",
            body=await async_maybe_transform(
                {"conversions": conversions}, client_convert_id_format_params.ClientConvertIDFormatParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConvertIDFormatResponse,
        )

    async def create_database(
        self,
        *,
        database: client_create_database_params.Database,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateDatabaseResponse:
        """
        Create a new database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/CreateDatabase",
            body=await async_maybe_transform(
                {"database": database}, client_create_database_params.ClientCreateDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateDatabaseResponse,
        )

    async def create_file_download_url(
        self,
        *,
        file_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateFileDownloadURLResponse:
        """
        Returns a pre-signed S3 URL.

        Args:
          file_id: Deep Origin system ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/CreateFileDownloadUrl",
            body=await async_maybe_transform(
                {"file_id": file_id}, client_create_file_download_url_params.ClientCreateFileDownloadURLParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateFileDownloadURLResponse,
        )

    async def create_file_upload(
        self,
        *,
        content_length: str,
        name: str,
        checksum_sha256: str | NotGiven = NOT_GIVEN,
        content_type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateFileUploadResponse:
        """Create a file upload URL.

        Typically this is creating a pre-signed S3 URL.

        Args:
          checksum_sha256: Base64 encoded SHA256 checksum of the file.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/CreateFileUpload",
            body=await async_maybe_transform(
                {
                    "content_length": content_length,
                    "name": name,
                    "checksum_sha256": checksum_sha256,
                    "content_type": content_type,
                },
                client_create_file_upload_params.ClientCreateFileUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateFileUploadResponse,
        )

    async def create_workspace(
        self,
        *,
        workspace: client_create_workspace_params.Workspace,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateWorkspaceResponse:
        """
        Create a new workspace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/CreateWorkspace",
            body=await async_maybe_transform(
                {"workspace": workspace}, client_create_workspace_params.ClientCreateWorkspaceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateWorkspaceResponse,
        )

    async def delete_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteDatabaseResponse:
        """
        Permanently deletes a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DeleteDatabase",
            body=await async_maybe_transform(
                {"database_id": database_id}, client_delete_database_params.ClientDeleteDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteDatabaseResponse,
        )

    async def delete_database_column(
        self,
        *,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteDatabaseColumnResponse:
        """
        Delete a column from a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DeleteDatabaseColumn",
            body=await async_maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_delete_database_column_params.ClientDeleteDatabaseColumnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteDatabaseColumnResponse,
        )

    async def delete_rows(
        self,
        *,
        database_id: str,
        delete_all: bool | NotGiven = NOT_GIVEN,
        row_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteRowsResponse:
        """
        Delete rows by their ids.

        Args:
          delete_all: When true, deletes all rows in the table except rows with the specified
              `rowIds`.

          row_ids: List of row IDs to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DeleteRows",
            body=await async_maybe_transform(
                {
                    "database_id": database_id,
                    "delete_all": delete_all,
                    "row_ids": row_ids,
                },
                client_delete_rows_params.ClientDeleteRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteRowsResponse,
        )

    async def delete_workspace(
        self,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteWorkspaceResponse:
        """
        Permanently deletes a workspace and all its children.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DeleteWorkspace",
            body=await async_maybe_transform(
                {"workspace_id": workspace_id}, client_delete_workspace_params.ClientDeleteWorkspaceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteWorkspaceResponse,
        )

    async def describe_code_execution(
        self,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeCodeExecutionResponse:
        """
        Returns information about a particular code execution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DescribeCodeExecution",
            body=await async_maybe_transform(
                {"id": id}, client_describe_code_execution_params.ClientDescribeCodeExecutionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeCodeExecutionResponse,
        )

    async def describe_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeDatabaseResponse:
        """
        Describe a database

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DescribeDatabase",
            body=await async_maybe_transform(
                {"database_id": database_id}, client_describe_database_params.ClientDescribeDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeDatabaseResponse,
        )

    async def describe_database_stats(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeDatabaseStatsResponse:
        """
        Returns aggregation information about a particular database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DescribeDatabaseStats",
            body=await async_maybe_transform(
                {"database_id": database_id}, client_describe_database_stats_params.ClientDescribeDatabaseStatsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeDatabaseStatsResponse,
        )

    async def describe_file(
        self,
        *,
        file_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeFileResponse:
        """
        Describe a file by its ID.

        Args:
          file_id: Deep Origin system ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DescribeFile",
            body=await async_maybe_transform(
                {"file_id": file_id}, client_describe_file_params.ClientDescribeFileParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeFileResponse,
        )

    async def describe_row(
        self,
        *,
        row_id: str,
        column_selection: client_describe_row_params.ColumnSelection | NotGiven = NOT_GIVEN,
        fields: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeRowResponse:
        """Deprecated.

        Use DescribeDatabaseRow, DescribeDatabase, or DescribeWorkspace
        instead.

        Args:
          column_selection: Select columns for inclusion/exclusion.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DescribeRow",
            body=await async_maybe_transform(
                {
                    "row_id": row_id,
                    "column_selection": column_selection,
                    "fields": fields,
                },
                client_describe_row_params.ClientDescribeRowParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeRowResponse,
        )

    async def describe_workspace(
        self,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescribeWorkspaceResponse:
        """
        Describe a workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/DescribeWorkspace",
            body=await async_maybe_transform(
                {"workspace_id": workspace_id}, client_describe_workspace_params.ClientDescribeWorkspaceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescribeWorkspaceResponse,
        )

    async def download_file(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Returns a 303 redirect to a pre-signed S3 URL."""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self.get(
            "/DownloadFile",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def ensure_rows(
        self,
        *,
        database_id: str,
        rows: Iterable[client_ensure_rows_params.Row],
        check_previous_value: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnsureRowsResponse:
        """Either creates or updates an existing row.

        Supports updates to both system and
        user defined columns.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/EnsureRows",
            body=await async_maybe_transform(
                {
                    "database_id": database_id,
                    "rows": rows,
                    "check_previous_value": check_previous_value,
                },
                client_ensure_rows_params.ClientEnsureRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnsureRowsResponse,
        )

    async def execute_code_async(
        self,
        *,
        code: str,
        code_language: Literal["python"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExecuteCodeAsyncResponse:
        """
        Execute code asynchronously.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ExecuteCode",
            body=await async_maybe_transform(
                {
                    "code": code,
                    "code_language": code_language,
                },
                client_execute_code_async_params.ClientExecuteCodeAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecuteCodeAsyncResponse,
        )

    async def execute_code_sync(
        self,
        *,
        code: str,
        code_language: Literal["python"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExecuteCodeSyncResponse:
        """
        Execute code synchronously.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ExecuteCodeSync",
            body=await async_maybe_transform(
                {
                    "code": code,
                    "code_language": code_language,
                },
                client_execute_code_sync_params.ClientExecuteCodeSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecuteCodeSyncResponse,
        )

    async def get_code_execution_result(
        self,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Returns the result of a code execution.

        Args:
          id: Deep Origin system ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/GetCodeExecutionResult",
            body=await async_maybe_transform(
                {"id": id}, client_get_code_execution_result_params.ClientGetCodeExecutionResultParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def import_rows(
        self,
        *,
        database_id: str,
        add_columns: Iterable[client_import_rows_params.AddColumn] | NotGiven = NOT_GIVEN,
        creation_block_id: str | NotGiven = NOT_GIVEN,
        creation_parent_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ImportRowsResponse:
        """
        Creates new rows from CSV data.

        Args:
          add_columns: Optionally add additional columns to the database during import.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ImportRows",
            body=await async_maybe_transform(
                {
                    "database_id": database_id,
                    "add_columns": add_columns,
                    "creation_block_id": creation_block_id,
                    "creation_parent_id": creation_parent_id,
                },
                client_import_rows_params.ClientImportRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImportRowsResponse,
        )

    async def list_database_column_unique_values_v2(
        self,
        *,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListDatabaseColumnUniqueValuesV2Response:
        """
        Returns the unique values for every cell within the column.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ListDatabaseColumnUniqueValuesV2",
            body=await async_maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_list_database_column_unique_values_v2_params.ClientListDatabaseColumnUniqueValuesV2Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListDatabaseColumnUniqueValuesV2Response,
        )

    async def list_database_rows(
        self,
        *,
        database_row_id: str,
        column_selection: client_list_database_rows_params.ColumnSelection | NotGiven = NOT_GIVEN,
        filter: client_list_database_rows_params.Filter | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        row_sort: Iterable[client_list_database_rows_params.RowSort] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListDatabaseRowsResponse:
        """
        List database rows with full row data.

        Args:
          column_selection: Select columns for inclusion/exclusion.

          row_sort: Sort rows by column.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ListDatabaseRows",
            body=await async_maybe_transform(
                {
                    "database_row_id": database_row_id,
                    "column_selection": column_selection,
                    "filter": filter,
                    "limit": limit,
                    "offset": offset,
                    "row_sort": row_sort,
                },
                client_list_database_rows_params.ClientListDatabaseRowsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListDatabaseRowsResponse,
        )

    async def list_files(
        self,
        *,
        filters: Iterable[client_list_files_params.Filter] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListFilesResponse:
        """
        Returns a list of files using the filters.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ListFiles",
            body=await async_maybe_transform({"filters": filters}, client_list_files_params.ClientListFilesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListFilesResponse,
        )

    async def list_mentions(
        self,
        *,
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListMentionsResponse:
        """
        Returns entities that can be mentioned in a notebook.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ListMentions",
            body=await async_maybe_transform({"query": query}, client_list_mentions_params.ClientListMentionsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListMentionsResponse,
        )

    async def list_row_back_references(
        self,
        *,
        database_id: str,
        row_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListRowBackReferencesResponse:
        """
        Finds all the places a row is referenced.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ListRowBackReferences",
            body=await async_maybe_transform(
                {
                    "database_id": database_id,
                    "row_id": row_id,
                },
                client_list_row_back_references_params.ClientListRowBackReferencesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListRowBackReferencesResponse,
        )

    async def list_rows(
        self,
        *,
        filters: Iterable[client_list_rows_params.Filter],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListRowsResponse:
        """
        Lists rows at a given depth in the hierarchy.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ListRows",
            body=await async_maybe_transform({"filters": filters}, client_list_rows_params.ClientListRowsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListRowsResponse,
        )

    async def lock_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LockDatabaseResponse:
        """
        A locked database cannot be edited.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/LockDatabase",
            body=await async_maybe_transform(
                {"database_id": database_id}, client_lock_database_params.ClientLockDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LockDatabaseResponse,
        )

    async def parse_base_sequence_data(
        self,
        *,
        file_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParseBaseSequenceDataResponse:
        """
        Parses a base sequence file and returns the parsed result.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/ParseBaseSequenceData",
            body=await async_maybe_transform(
                {"file_id": file_id}, client_parse_base_sequence_data_params.ClientParseBaseSequenceDataParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseBaseSequenceDataResponse,
        )

    async def unlock_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnlockDatabaseResponse:
        """
        An unlocked database can be edited.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/UnlockDatabase",
            body=await async_maybe_transform(
                {"database_id": database_id}, client_unlock_database_params.ClientUnlockDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UnlockDatabaseResponse,
        )

    async def update_database(
        self,
        *,
        id: str,
        database: client_update_database_params.Database,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateDatabaseResponse:
        """
        Update a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/UpdateDatabase",
            body=await async_maybe_transform(
                {
                    "id": id,
                    "database": database,
                },
                client_update_database_params.ClientUpdateDatabaseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UpdateDatabaseResponse,
        )

    async def update_database_column(
        self,
        *,
        column: client_update_database_column_params.Column,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateDatabaseColumnResponse:
        """
        Update a column in a database.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/UpdateDatabaseColumn",
            body=await async_maybe_transform(
                {
                    "column": column,
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_update_database_column_params.ClientUpdateDatabaseColumnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UpdateDatabaseColumnResponse,
        )

    async def update_workspace(
        self,
        *,
        id: str,
        workspace: client_update_workspace_params.Workspace,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateWorkspaceResponse:
        """
        Update a workspace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.post(
            "/UpdateWorkspace",
            body=await async_maybe_transform(
                {
                    "id": id,
                    "workspace": workspace,
                },
                client_update_workspace_params.ClientUpdateWorkspaceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UpdateWorkspaceResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class DeeporiginDataWithRawResponse:
    def __init__(self, client: DeeporiginData) -> None:
        self.add_database_column = to_raw_response_wrapper(
            client.add_database_column,
        )
        self.archive_files = to_raw_response_wrapper(
            client.archive_files,
        )
        self.chat_create_thread = to_raw_response_wrapper(
            client.chat_create_thread,
        )
        self.chat_list_messages = to_raw_response_wrapper(
            client.chat_list_messages,
        )
        self.chat_send_message = to_raw_response_wrapper(
            client.chat_send_message,
        )
        self.configure_column_select_options = to_raw_response_wrapper(
            client.configure_column_select_options,
        )
        self.convert_id_format = to_raw_response_wrapper(
            client.convert_id_format,
        )
        self.create_database = to_raw_response_wrapper(
            client.create_database,
        )
        self.create_file_download_url = to_raw_response_wrapper(
            client.create_file_download_url,
        )
        self.create_file_upload = to_raw_response_wrapper(
            client.create_file_upload,
        )
        self.create_workspace = to_raw_response_wrapper(
            client.create_workspace,
        )
        self.delete_database = to_raw_response_wrapper(
            client.delete_database,
        )
        self.delete_database_column = to_raw_response_wrapper(
            client.delete_database_column,
        )
        self.delete_rows = to_raw_response_wrapper(
            client.delete_rows,
        )
        self.delete_workspace = to_raw_response_wrapper(
            client.delete_workspace,
        )
        self.describe_code_execution = to_raw_response_wrapper(
            client.describe_code_execution,
        )
        self.describe_database = to_raw_response_wrapper(
            client.describe_database,
        )
        self.describe_database_stats = to_raw_response_wrapper(
            client.describe_database_stats,
        )
        self.describe_file = to_raw_response_wrapper(
            client.describe_file,
        )
        self.describe_row = to_raw_response_wrapper(
            client.describe_row,
        )
        self.describe_workspace = to_raw_response_wrapper(
            client.describe_workspace,
        )
        self.download_file = to_raw_response_wrapper(
            client.download_file,
        )
        self.ensure_rows = to_raw_response_wrapper(
            client.ensure_rows,
        )
        self.execute_code_async = to_raw_response_wrapper(
            client.execute_code_async,
        )
        self.execute_code_sync = to_raw_response_wrapper(
            client.execute_code_sync,
        )
        self.get_code_execution_result = to_raw_response_wrapper(
            client.get_code_execution_result,
        )
        self.import_rows = to_raw_response_wrapper(
            client.import_rows,
        )
        self.list_database_column_unique_values_v2 = to_raw_response_wrapper(
            client.list_database_column_unique_values_v2,
        )
        self.list_database_rows = to_raw_response_wrapper(
            client.list_database_rows,
        )
        self.list_files = to_raw_response_wrapper(
            client.list_files,
        )
        self.list_mentions = to_raw_response_wrapper(
            client.list_mentions,
        )
        self.list_row_back_references = to_raw_response_wrapper(
            client.list_row_back_references,
        )
        self.list_rows = to_raw_response_wrapper(
            client.list_rows,
        )
        self.lock_database = to_raw_response_wrapper(
            client.lock_database,
        )
        self.parse_base_sequence_data = to_raw_response_wrapper(
            client.parse_base_sequence_data,
        )
        self.unlock_database = to_raw_response_wrapper(
            client.unlock_database,
        )
        self.update_database = to_raw_response_wrapper(
            client.update_database,
        )
        self.update_database_column = to_raw_response_wrapper(
            client.update_database_column,
        )
        self.update_workspace = to_raw_response_wrapper(
            client.update_workspace,
        )


class AsyncDeeporiginDataWithRawResponse:
    def __init__(self, client: AsyncDeeporiginData) -> None:
        self.add_database_column = async_to_raw_response_wrapper(
            client.add_database_column,
        )
        self.archive_files = async_to_raw_response_wrapper(
            client.archive_files,
        )
        self.chat_create_thread = async_to_raw_response_wrapper(
            client.chat_create_thread,
        )
        self.chat_list_messages = async_to_raw_response_wrapper(
            client.chat_list_messages,
        )
        self.chat_send_message = async_to_raw_response_wrapper(
            client.chat_send_message,
        )
        self.configure_column_select_options = async_to_raw_response_wrapper(
            client.configure_column_select_options,
        )
        self.convert_id_format = async_to_raw_response_wrapper(
            client.convert_id_format,
        )
        self.create_database = async_to_raw_response_wrapper(
            client.create_database,
        )
        self.create_file_download_url = async_to_raw_response_wrapper(
            client.create_file_download_url,
        )
        self.create_file_upload = async_to_raw_response_wrapper(
            client.create_file_upload,
        )
        self.create_workspace = async_to_raw_response_wrapper(
            client.create_workspace,
        )
        self.delete_database = async_to_raw_response_wrapper(
            client.delete_database,
        )
        self.delete_database_column = async_to_raw_response_wrapper(
            client.delete_database_column,
        )
        self.delete_rows = async_to_raw_response_wrapper(
            client.delete_rows,
        )
        self.delete_workspace = async_to_raw_response_wrapper(
            client.delete_workspace,
        )
        self.describe_code_execution = async_to_raw_response_wrapper(
            client.describe_code_execution,
        )
        self.describe_database = async_to_raw_response_wrapper(
            client.describe_database,
        )
        self.describe_database_stats = async_to_raw_response_wrapper(
            client.describe_database_stats,
        )
        self.describe_file = async_to_raw_response_wrapper(
            client.describe_file,
        )
        self.describe_row = async_to_raw_response_wrapper(
            client.describe_row,
        )
        self.describe_workspace = async_to_raw_response_wrapper(
            client.describe_workspace,
        )
        self.download_file = async_to_raw_response_wrapper(
            client.download_file,
        )
        self.ensure_rows = async_to_raw_response_wrapper(
            client.ensure_rows,
        )
        self.execute_code_async = async_to_raw_response_wrapper(
            client.execute_code_async,
        )
        self.execute_code_sync = async_to_raw_response_wrapper(
            client.execute_code_sync,
        )
        self.get_code_execution_result = async_to_raw_response_wrapper(
            client.get_code_execution_result,
        )
        self.import_rows = async_to_raw_response_wrapper(
            client.import_rows,
        )
        self.list_database_column_unique_values_v2 = async_to_raw_response_wrapper(
            client.list_database_column_unique_values_v2,
        )
        self.list_database_rows = async_to_raw_response_wrapper(
            client.list_database_rows,
        )
        self.list_files = async_to_raw_response_wrapper(
            client.list_files,
        )
        self.list_mentions = async_to_raw_response_wrapper(
            client.list_mentions,
        )
        self.list_row_back_references = async_to_raw_response_wrapper(
            client.list_row_back_references,
        )
        self.list_rows = async_to_raw_response_wrapper(
            client.list_rows,
        )
        self.lock_database = async_to_raw_response_wrapper(
            client.lock_database,
        )
        self.parse_base_sequence_data = async_to_raw_response_wrapper(
            client.parse_base_sequence_data,
        )
        self.unlock_database = async_to_raw_response_wrapper(
            client.unlock_database,
        )
        self.update_database = async_to_raw_response_wrapper(
            client.update_database,
        )
        self.update_database_column = async_to_raw_response_wrapper(
            client.update_database_column,
        )
        self.update_workspace = async_to_raw_response_wrapper(
            client.update_workspace,
        )


class DeeporiginDataWithStreamedResponse:
    def __init__(self, client: DeeporiginData) -> None:
        self.add_database_column = to_streamed_response_wrapper(
            client.add_database_column,
        )
        self.archive_files = to_streamed_response_wrapper(
            client.archive_files,
        )
        self.chat_create_thread = to_streamed_response_wrapper(
            client.chat_create_thread,
        )
        self.chat_list_messages = to_streamed_response_wrapper(
            client.chat_list_messages,
        )
        self.chat_send_message = to_streamed_response_wrapper(
            client.chat_send_message,
        )
        self.configure_column_select_options = to_streamed_response_wrapper(
            client.configure_column_select_options,
        )
        self.convert_id_format = to_streamed_response_wrapper(
            client.convert_id_format,
        )
        self.create_database = to_streamed_response_wrapper(
            client.create_database,
        )
        self.create_file_download_url = to_streamed_response_wrapper(
            client.create_file_download_url,
        )
        self.create_file_upload = to_streamed_response_wrapper(
            client.create_file_upload,
        )
        self.create_workspace = to_streamed_response_wrapper(
            client.create_workspace,
        )
        self.delete_database = to_streamed_response_wrapper(
            client.delete_database,
        )
        self.delete_database_column = to_streamed_response_wrapper(
            client.delete_database_column,
        )
        self.delete_rows = to_streamed_response_wrapper(
            client.delete_rows,
        )
        self.delete_workspace = to_streamed_response_wrapper(
            client.delete_workspace,
        )
        self.describe_code_execution = to_streamed_response_wrapper(
            client.describe_code_execution,
        )
        self.describe_database = to_streamed_response_wrapper(
            client.describe_database,
        )
        self.describe_database_stats = to_streamed_response_wrapper(
            client.describe_database_stats,
        )
        self.describe_file = to_streamed_response_wrapper(
            client.describe_file,
        )
        self.describe_row = to_streamed_response_wrapper(
            client.describe_row,
        )
        self.describe_workspace = to_streamed_response_wrapper(
            client.describe_workspace,
        )
        self.download_file = to_streamed_response_wrapper(
            client.download_file,
        )
        self.ensure_rows = to_streamed_response_wrapper(
            client.ensure_rows,
        )
        self.execute_code_async = to_streamed_response_wrapper(
            client.execute_code_async,
        )
        self.execute_code_sync = to_streamed_response_wrapper(
            client.execute_code_sync,
        )
        self.get_code_execution_result = to_streamed_response_wrapper(
            client.get_code_execution_result,
        )
        self.import_rows = to_streamed_response_wrapper(
            client.import_rows,
        )
        self.list_database_column_unique_values_v2 = to_streamed_response_wrapper(
            client.list_database_column_unique_values_v2,
        )
        self.list_database_rows = to_streamed_response_wrapper(
            client.list_database_rows,
        )
        self.list_files = to_streamed_response_wrapper(
            client.list_files,
        )
        self.list_mentions = to_streamed_response_wrapper(
            client.list_mentions,
        )
        self.list_row_back_references = to_streamed_response_wrapper(
            client.list_row_back_references,
        )
        self.list_rows = to_streamed_response_wrapper(
            client.list_rows,
        )
        self.lock_database = to_streamed_response_wrapper(
            client.lock_database,
        )
        self.parse_base_sequence_data = to_streamed_response_wrapper(
            client.parse_base_sequence_data,
        )
        self.unlock_database = to_streamed_response_wrapper(
            client.unlock_database,
        )
        self.update_database = to_streamed_response_wrapper(
            client.update_database,
        )
        self.update_database_column = to_streamed_response_wrapper(
            client.update_database_column,
        )
        self.update_workspace = to_streamed_response_wrapper(
            client.update_workspace,
        )


class AsyncDeeporiginDataWithStreamedResponse:
    def __init__(self, client: AsyncDeeporiginData) -> None:
        self.add_database_column = async_to_streamed_response_wrapper(
            client.add_database_column,
        )
        self.archive_files = async_to_streamed_response_wrapper(
            client.archive_files,
        )
        self.chat_create_thread = async_to_streamed_response_wrapper(
            client.chat_create_thread,
        )
        self.chat_list_messages = async_to_streamed_response_wrapper(
            client.chat_list_messages,
        )
        self.chat_send_message = async_to_streamed_response_wrapper(
            client.chat_send_message,
        )
        self.configure_column_select_options = async_to_streamed_response_wrapper(
            client.configure_column_select_options,
        )
        self.convert_id_format = async_to_streamed_response_wrapper(
            client.convert_id_format,
        )
        self.create_database = async_to_streamed_response_wrapper(
            client.create_database,
        )
        self.create_file_download_url = async_to_streamed_response_wrapper(
            client.create_file_download_url,
        )
        self.create_file_upload = async_to_streamed_response_wrapper(
            client.create_file_upload,
        )
        self.create_workspace = async_to_streamed_response_wrapper(
            client.create_workspace,
        )
        self.delete_database = async_to_streamed_response_wrapper(
            client.delete_database,
        )
        self.delete_database_column = async_to_streamed_response_wrapper(
            client.delete_database_column,
        )
        self.delete_rows = async_to_streamed_response_wrapper(
            client.delete_rows,
        )
        self.delete_workspace = async_to_streamed_response_wrapper(
            client.delete_workspace,
        )
        self.describe_code_execution = async_to_streamed_response_wrapper(
            client.describe_code_execution,
        )
        self.describe_database = async_to_streamed_response_wrapper(
            client.describe_database,
        )
        self.describe_database_stats = async_to_streamed_response_wrapper(
            client.describe_database_stats,
        )
        self.describe_file = async_to_streamed_response_wrapper(
            client.describe_file,
        )
        self.describe_row = async_to_streamed_response_wrapper(
            client.describe_row,
        )
        self.describe_workspace = async_to_streamed_response_wrapper(
            client.describe_workspace,
        )
        self.download_file = async_to_streamed_response_wrapper(
            client.download_file,
        )
        self.ensure_rows = async_to_streamed_response_wrapper(
            client.ensure_rows,
        )
        self.execute_code_async = async_to_streamed_response_wrapper(
            client.execute_code_async,
        )
        self.execute_code_sync = async_to_streamed_response_wrapper(
            client.execute_code_sync,
        )
        self.get_code_execution_result = async_to_streamed_response_wrapper(
            client.get_code_execution_result,
        )
        self.import_rows = async_to_streamed_response_wrapper(
            client.import_rows,
        )
        self.list_database_column_unique_values_v2 = async_to_streamed_response_wrapper(
            client.list_database_column_unique_values_v2,
        )
        self.list_database_rows = async_to_streamed_response_wrapper(
            client.list_database_rows,
        )
        self.list_files = async_to_streamed_response_wrapper(
            client.list_files,
        )
        self.list_mentions = async_to_streamed_response_wrapper(
            client.list_mentions,
        )
        self.list_row_back_references = async_to_streamed_response_wrapper(
            client.list_row_back_references,
        )
        self.list_rows = async_to_streamed_response_wrapper(
            client.list_rows,
        )
        self.lock_database = async_to_streamed_response_wrapper(
            client.lock_database,
        )
        self.parse_base_sequence_data = async_to_streamed_response_wrapper(
            client.parse_base_sequence_data,
        )
        self.unlock_database = async_to_streamed_response_wrapper(
            client.unlock_database,
        )
        self.update_database = async_to_streamed_response_wrapper(
            client.update_database,
        )
        self.update_database_column = async_to_streamed_response_wrapper(
            client.update_database_column,
        )
        self.update_workspace = async_to_streamed_response_wrapper(
            client.update_workspace,
        )


Client = DeeporiginData

AsyncClient = AsyncDeeporiginData
