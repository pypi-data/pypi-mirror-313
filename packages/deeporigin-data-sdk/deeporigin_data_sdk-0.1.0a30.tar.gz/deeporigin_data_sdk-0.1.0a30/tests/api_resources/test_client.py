# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from deeporigin_data import DeeporiginData, AsyncDeeporiginData
from deeporigin_data.types import (
    ListRowsResponse,
    ListFilesResponse,
    DeleteRowsResponse,
    EnsureRowsResponse,
    ImportRowsResponse,
    DescribeFileResponse,
    ListMentionsResponse,
    LockDatabaseResponse,
    CreateDatabaseResponse,
    DeleteDatabaseResponse,
    UnlockDatabaseResponse,
    UpdateDatabaseResponse,
    ConvertIDFormatResponse,
    CreateWorkspaceResponse,
    DeleteWorkspaceResponse,
    ExecuteCodeSyncResponse,
    UpdateWorkspaceResponse,
    ChatCreateThreadResponse,
    ChatListMessagesResponse,
    CreateFileUploadResponse,
    DescribeDatabaseResponse,
    ExecuteCodeAsyncResponse,
    ListDatabaseRowsResponse,
    AddDatabaseColumnResponse,
    DescribeWorkspaceResponse,
    DeleteDatabaseColumnResponse,
    UpdateDatabaseColumnResponse,
    CreateFileDownloadURLResponse,
    DescribeCodeExecutionResponse,
    DescribeDatabaseStatsResponse,
    ListRowBackReferencesResponse,
    ParseBaseSequenceDataResponse,
    ConfigureColumnSelectOptionsResponse,
    ListDatabaseColumnUniqueValuesV2Response,
)
from deeporigin_data.types.shared import DescribeRowResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_add_database_column(self, client: DeeporiginData) -> None:
        client_ = client.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
            },
            database_id="databaseId",
        )
        assert_matches_type(AddDatabaseColumnResponse, client_, path=["response"])

    @parametrize
    def test_method_add_database_column_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
                "cell_json_schema": {},
                "enabled_viewers": ["code"],
                "inline_viewer": "molecule2d",
                "is_required": True,
                "system_type": "name",
            },
            database_id="databaseId",
        )
        assert_matches_type(AddDatabaseColumnResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_add_database_column(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
            },
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(AddDatabaseColumnResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_add_database_column(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
            },
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(AddDatabaseColumnResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive_files(self, client: DeeporiginData) -> None:
        client_ = client.archive_files(
            file_ids=["string"],
        )
        assert_matches_type(object, client_, path=["response"])

    @parametrize
    def test_raw_response_archive_files(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.archive_files(
            file_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(object, client_, path=["response"])

    @parametrize
    def test_streaming_response_archive_files(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.archive_files(
            file_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(object, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_chat_create_thread(self, client: DeeporiginData) -> None:
        client_ = client.chat_create_thread(
            body={},
        )
        assert_matches_type(ChatCreateThreadResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_chat_create_thread(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.chat_create_thread(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ChatCreateThreadResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_chat_create_thread(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.chat_create_thread(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ChatCreateThreadResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_chat_list_messages(self, client: DeeporiginData) -> None:
        client_ = client.chat_list_messages(
            thread_id="threadId",
        )
        assert_matches_type(ChatListMessagesResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_chat_list_messages(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.chat_list_messages(
            thread_id="threadId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ChatListMessagesResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_chat_list_messages(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.chat_list_messages(
            thread_id="threadId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ChatListMessagesResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_chat_send_message(self, client: DeeporiginData) -> None:
        client_ = client.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
        )
        assert client_ is None

    @parametrize
    def test_method_chat_send_message_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
            context={
                "databases": [
                    {
                        "database": {
                            "hid": "hid",
                            "hid_prefix": "hidPrefix",
                            "name": "name",
                        },
                        "columns": [{"name": "name"}],
                        "rows": [
                            {
                                "hid": "hid",
                                "name": "name",
                            }
                        ],
                    }
                ]
            },
        )
        assert client_ is None

    @parametrize
    def test_raw_response_chat_send_message(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert client_ is None

    @parametrize
    def test_streaming_response_chat_send_message(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert client_ is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_configure_column_select_options(self, client: DeeporiginData) -> None:
        client_ = client.configure_column_select_options(
            column_id="columnId",
            database_id="databaseId",
            option_configuration=[
                {
                    "op": "add",
                    "option": "option",
                }
            ],
        )
        assert_matches_type(ConfigureColumnSelectOptionsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_configure_column_select_options(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.configure_column_select_options(
            column_id="columnId",
            database_id="databaseId",
            option_configuration=[
                {
                    "op": "add",
                    "option": "option",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ConfigureColumnSelectOptionsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_configure_column_select_options(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.configure_column_select_options(
            column_id="columnId",
            database_id="databaseId",
            option_configuration=[
                {
                    "op": "add",
                    "option": "option",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ConfigureColumnSelectOptionsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_convert_id_format(self, client: DeeporiginData) -> None:
        client_ = client.convert_id_format(
            conversions=[{"id": "id"}],
        )
        assert_matches_type(ConvertIDFormatResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_convert_id_format(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.convert_id_format(
            conversions=[{"id": "id"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ConvertIDFormatResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_convert_id_format(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.convert_id_format(
            conversions=[{"id": "id"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ConvertIDFormatResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_database(self, client: DeeporiginData) -> None:
        client_ = client.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
            },
        )
        assert_matches_type(CreateDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_method_create_database_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
                "cols": [{}],
                "is_inline_database": True,
                "parent_id": "parentId",
            },
        )
        assert_matches_type(CreateDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_create_database(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CreateDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_create_database(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CreateDatabaseResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_file_download_url(self, client: DeeporiginData) -> None:
        client_ = client.create_file_download_url(
            file_id="fileId",
        )
        assert_matches_type(CreateFileDownloadURLResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_create_file_download_url(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.create_file_download_url(
            file_id="fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CreateFileDownloadURLResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_create_file_download_url(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.create_file_download_url(
            file_id="fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CreateFileDownloadURLResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_file_upload(self, client: DeeporiginData) -> None:
        client_ = client.create_file_upload(
            content_length="contentLength",
            name="name",
        )
        assert_matches_type(CreateFileUploadResponse, client_, path=["response"])

    @parametrize
    def test_method_create_file_upload_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.create_file_upload(
            content_length="contentLength",
            name="name",
            checksum_sha256="checksumSha256",
            content_type="contentType",
        )
        assert_matches_type(CreateFileUploadResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_create_file_upload(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.create_file_upload(
            content_length="contentLength",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CreateFileUploadResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_create_file_upload(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.create_file_upload(
            content_length="contentLength",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CreateFileUploadResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_workspace(self, client: DeeporiginData) -> None:
        client_ = client.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
            },
        )
        assert_matches_type(CreateWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_method_create_workspace_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
                "parent_id": "parentId",
            },
        )
        assert_matches_type(CreateWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_create_workspace(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CreateWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_create_workspace(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CreateWorkspaceResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete_database(self, client: DeeporiginData) -> None:
        client_ = client.delete_database(
            database_id="databaseId",
        )
        assert_matches_type(DeleteDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_delete_database(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.delete_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DeleteDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_delete_database(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.delete_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DeleteDatabaseResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete_database_column(self, client: DeeporiginData) -> None:
        client_ = client.delete_database_column(
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(DeleteDatabaseColumnResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_delete_database_column(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.delete_database_column(
            column_id="columnId",
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DeleteDatabaseColumnResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_delete_database_column(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.delete_database_column(
            column_id="columnId",
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DeleteDatabaseColumnResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete_rows(self, client: DeeporiginData) -> None:
        client_ = client.delete_rows(
            database_id="databaseId",
        )
        assert_matches_type(DeleteRowsResponse, client_, path=["response"])

    @parametrize
    def test_method_delete_rows_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.delete_rows(
            database_id="databaseId",
            delete_all=True,
            row_ids=["string"],
        )
        assert_matches_type(DeleteRowsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_delete_rows(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.delete_rows(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DeleteRowsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_delete_rows(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.delete_rows(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DeleteRowsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete_workspace(self, client: DeeporiginData) -> None:
        client_ = client.delete_workspace(
            workspace_id="workspaceId",
        )
        assert_matches_type(DeleteWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_delete_workspace(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.delete_workspace(
            workspace_id="workspaceId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DeleteWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_delete_workspace(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.delete_workspace(
            workspace_id="workspaceId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DeleteWorkspaceResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_describe_code_execution(self, client: DeeporiginData) -> None:
        client_ = client.describe_code_execution(
            id="id",
        )
        assert_matches_type(DescribeCodeExecutionResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_describe_code_execution(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.describe_code_execution(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DescribeCodeExecutionResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_describe_code_execution(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.describe_code_execution(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DescribeCodeExecutionResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_describe_database(self, client: DeeporiginData) -> None:
        client_ = client.describe_database(
            database_id="databaseId",
        )
        assert_matches_type(DescribeDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_describe_database(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.describe_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DescribeDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_describe_database(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.describe_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DescribeDatabaseResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_describe_database_stats(self, client: DeeporiginData) -> None:
        client_ = client.describe_database_stats(
            database_id="databaseId",
        )
        assert_matches_type(DescribeDatabaseStatsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_describe_database_stats(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.describe_database_stats(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DescribeDatabaseStatsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_describe_database_stats(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.describe_database_stats(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DescribeDatabaseStatsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_describe_file(self, client: DeeporiginData) -> None:
        client_ = client.describe_file(
            file_id="fileId",
        )
        assert_matches_type(DescribeFileResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_describe_file(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.describe_file(
            file_id="fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DescribeFileResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_describe_file(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.describe_file(
            file_id="fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DescribeFileResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_describe_row(self, client: DeeporiginData) -> None:
        client_ = client.describe_row(
            row_id="rowId",
        )
        assert_matches_type(DescribeRowResponse, client_, path=["response"])

    @parametrize
    def test_method_describe_row_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.describe_row(
            row_id="rowId",
            column_selection={
                "exclude": ["string"],
                "include": ["string"],
            },
            fields=True,
        )
        assert_matches_type(DescribeRowResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_describe_row(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.describe_row(
            row_id="rowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DescribeRowResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_describe_row(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.describe_row(
            row_id="rowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DescribeRowResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_describe_workspace(self, client: DeeporiginData) -> None:
        client_ = client.describe_workspace(
            workspace_id="workspaceId",
        )
        assert_matches_type(DescribeWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_describe_workspace(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.describe_workspace(
            workspace_id="workspaceId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(DescribeWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_describe_workspace(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.describe_workspace(
            workspace_id="workspaceId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(DescribeWorkspaceResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_download_file(self, client: DeeporiginData) -> None:
        client_ = client.download_file()
        assert client_ is None

    @parametrize
    def test_raw_response_download_file(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.download_file()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert client_ is None

    @parametrize
    def test_streaming_response_download_file(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.download_file() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert client_ is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_ensure_rows(self, client: DeeporiginData) -> None:
        client_ = client.ensure_rows(
            database_id="databaseId",
            rows=[{}],
        )
        assert_matches_type(EnsureRowsResponse, client_, path=["response"])

    @parametrize
    def test_method_ensure_rows_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.ensure_rows(
            database_id="databaseId",
            rows=[
                {
                    "cells": [
                        {
                            "column_id": "columnId",
                            "value": {},
                            "previous_version": 0,
                        }
                    ],
                    "row": {
                        "creation_block_id": "creationBlockId",
                        "creation_parent_id": "creationParentId",
                        "is_template": True,
                    },
                    "row_id": "rowId",
                }
            ],
            check_previous_value=True,
        )
        assert_matches_type(EnsureRowsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_ensure_rows(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.ensure_rows(
            database_id="databaseId",
            rows=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(EnsureRowsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_ensure_rows(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.ensure_rows(
            database_id="databaseId",
            rows=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(EnsureRowsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_execute_code_async(self, client: DeeporiginData) -> None:
        client_ = client.execute_code_async(
            code="code",
            code_language="python",
        )
        assert_matches_type(ExecuteCodeAsyncResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_execute_code_async(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.execute_code_async(
            code="code",
            code_language="python",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ExecuteCodeAsyncResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_execute_code_async(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.execute_code_async(
            code="code",
            code_language="python",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ExecuteCodeAsyncResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_execute_code_sync(self, client: DeeporiginData) -> None:
        client_ = client.execute_code_sync(
            code="code",
            code_language="python",
        )
        assert_matches_type(ExecuteCodeSyncResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_execute_code_sync(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.execute_code_sync(
            code="code",
            code_language="python",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ExecuteCodeSyncResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_execute_code_sync(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.execute_code_sync(
            code="code",
            code_language="python",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ExecuteCodeSyncResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get_code_execution_result(self, client: DeeporiginData) -> None:
        client_ = client.get_code_execution_result(
            id="id",
        )
        assert_matches_type(object, client_, path=["response"])

    @parametrize
    def test_raw_response_get_code_execution_result(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.get_code_execution_result(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(object, client_, path=["response"])

    @parametrize
    def test_streaming_response_get_code_execution_result(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.get_code_execution_result(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(object, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_import_rows(self, client: DeeporiginData) -> None:
        client_ = client.import_rows(
            database_id="databaseId",
        )
        assert_matches_type(ImportRowsResponse, client_, path=["response"])

    @parametrize
    def test_method_import_rows_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.import_rows(
            database_id="databaseId",
            add_columns=[
                {
                    "cardinality": "one",
                    "lookup_external_column_id": "lookupExternalColumnId",
                    "lookup_source_column_id": "lookupSourceColumnId",
                    "name": "name",
                    "type": "lookup",
                    "cell_json_schema": {},
                    "enabled_viewers": ["code"],
                    "inline_viewer": "molecule2d",
                    "is_required": True,
                    "system_type": "name",
                }
            ],
            creation_block_id="creationBlockId",
            creation_parent_id="creationParentId",
        )
        assert_matches_type(ImportRowsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_import_rows(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.import_rows(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ImportRowsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_import_rows(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.import_rows(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ImportRowsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_database_column_unique_values_v2(self, client: DeeporiginData) -> None:
        client_ = client.list_database_column_unique_values_v2(
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(ListDatabaseColumnUniqueValuesV2Response, client_, path=["response"])

    @parametrize
    def test_raw_response_list_database_column_unique_values_v2(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.list_database_column_unique_values_v2(
            column_id="columnId",
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ListDatabaseColumnUniqueValuesV2Response, client_, path=["response"])

    @parametrize
    def test_streaming_response_list_database_column_unique_values_v2(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.list_database_column_unique_values_v2(
            column_id="columnId",
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ListDatabaseColumnUniqueValuesV2Response, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_database_rows(self, client: DeeporiginData) -> None:
        client_ = client.list_database_rows(
            database_row_id="databaseRowId",
        )
        assert_matches_type(ListDatabaseRowsResponse, client_, path=["response"])

    @parametrize
    def test_method_list_database_rows_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.list_database_rows(
            database_row_id="databaseRowId",
            column_selection={
                "exclude": ["string"],
                "include": ["string"],
            },
            filter={
                "column_id": "columnId",
                "filter_type": "text",
                "filter_value": "filterValue",
                "operator": "equals",
            },
            limit=1,
            offset=0,
            row_sort=[
                {
                    "column_id": "columnId",
                    "sort": "asc",
                }
            ],
        )
        assert_matches_type(ListDatabaseRowsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_list_database_rows(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.list_database_rows(
            database_row_id="databaseRowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ListDatabaseRowsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_list_database_rows(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.list_database_rows(
            database_row_id="databaseRowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ListDatabaseRowsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_files(self, client: DeeporiginData) -> None:
        client_ = client.list_files()
        assert_matches_type(ListFilesResponse, client_, path=["response"])

    @parametrize
    def test_method_list_files_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.list_files(
            filters=[
                {
                    "assigned_row_ids": ["string"],
                    "file_ids": ["string"],
                    "is_unassigned": True,
                    "status": ["ready"],
                }
            ],
        )
        assert_matches_type(ListFilesResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_list_files(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.list_files()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ListFilesResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_list_files(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.list_files() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ListFilesResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_mentions(self, client: DeeporiginData) -> None:
        client_ = client.list_mentions(
            query="query",
        )
        assert_matches_type(ListMentionsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_list_mentions(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.list_mentions(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ListMentionsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_list_mentions(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.list_mentions(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ListMentionsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_row_back_references(self, client: DeeporiginData) -> None:
        client_ = client.list_row_back_references(
            database_id="databaseId",
            row_id="rowId",
        )
        assert_matches_type(ListRowBackReferencesResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_list_row_back_references(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.list_row_back_references(
            database_id="databaseId",
            row_id="rowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ListRowBackReferencesResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_list_row_back_references(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.list_row_back_references(
            database_id="databaseId",
            row_id="rowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ListRowBackReferencesResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_rows(self, client: DeeporiginData) -> None:
        client_ = client.list_rows(
            filters=[{"parent": {"id": "id"}}],
        )
        assert_matches_type(ListRowsResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_list_rows(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.list_rows(
            filters=[{"parent": {"id": "id"}}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ListRowsResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_list_rows(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.list_rows(
            filters=[{"parent": {"id": "id"}}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ListRowsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_lock_database(self, client: DeeporiginData) -> None:
        client_ = client.lock_database(
            database_id="databaseId",
        )
        assert_matches_type(LockDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_lock_database(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.lock_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(LockDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_lock_database(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.lock_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(LockDatabaseResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_parse_base_sequence_data(self, client: DeeporiginData) -> None:
        client_ = client.parse_base_sequence_data(
            file_id="fileId",
        )
        assert_matches_type(ParseBaseSequenceDataResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_parse_base_sequence_data(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.parse_base_sequence_data(
            file_id="fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ParseBaseSequenceDataResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_parse_base_sequence_data(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.parse_base_sequence_data(
            file_id="fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ParseBaseSequenceDataResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_unlock_database(self, client: DeeporiginData) -> None:
        client_ = client.unlock_database(
            database_id="databaseId",
        )
        assert_matches_type(UnlockDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_unlock_database(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.unlock_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(UnlockDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_unlock_database(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.unlock_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(UnlockDatabaseResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update_database(self, client: DeeporiginData) -> None:
        client_ = client.update_database(
            id="id",
            database={},
        )
        assert_matches_type(UpdateDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_method_update_database_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.update_database(
            id="id",
            database={
                "editor": {},
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
                "parent_id": "parentId",
            },
        )
        assert_matches_type(UpdateDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_update_database(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.update_database(
            id="id",
            database={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(UpdateDatabaseResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_update_database(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.update_database(
            id="id",
            database={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(UpdateDatabaseResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    def test_method_update_database_column(self, client: DeeporiginData) -> None:
        client_ = client.update_database_column(
            column={"type": "boolean"},
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(UpdateDatabaseColumnResponse, client_, path=["response"])

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    def test_method_update_database_column_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.update_database_column(
            column={
                "type": "boolean",
                "cardinality": "one",
                "cellJsonSchema": {},
                "enabledViewers": ["code"],
                "inlineViewer": "molecule2d",
                "isRequired": True,
                "name": "name",
                "systemType": "name",
            },
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(UpdateDatabaseColumnResponse, client_, path=["response"])

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    def test_raw_response_update_database_column(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.update_database_column(
            column={"type": "boolean"},
            column_id="columnId",
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(UpdateDatabaseColumnResponse, client_, path=["response"])

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    def test_streaming_response_update_database_column(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.update_database_column(
            column={"type": "boolean"},
            column_id="columnId",
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(UpdateDatabaseColumnResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update_workspace(self, client: DeeporiginData) -> None:
        client_ = client.update_workspace(
            id="id",
            workspace={},
        )
        assert_matches_type(UpdateWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_method_update_workspace_with_all_params(self, client: DeeporiginData) -> None:
        client_ = client.update_workspace(
            id="id",
            workspace={
                "editor": {},
                "hid": "hid",
                "name": "name",
                "parent_id": "parentId",
            },
        )
        assert_matches_type(UpdateWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_update_workspace(self, client: DeeporiginData) -> None:
        response = client.with_raw_response.update_workspace(
            id="id",
            workspace={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(UpdateWorkspaceResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_update_workspace(self, client: DeeporiginData) -> None:
        with client.with_streaming_response.update_workspace(
            id="id",
            workspace={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(UpdateWorkspaceResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClient:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_add_database_column(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
            },
            database_id="databaseId",
        )
        assert_matches_type(AddDatabaseColumnResponse, client, path=["response"])

    @parametrize
    async def test_method_add_database_column_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
                "cell_json_schema": {},
                "enabled_viewers": ["code"],
                "inline_viewer": "molecule2d",
                "is_required": True,
                "system_type": "name",
            },
            database_id="databaseId",
        )
        assert_matches_type(AddDatabaseColumnResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_add_database_column(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
            },
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(AddDatabaseColumnResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_add_database_column(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.add_database_column(
            column={
                "cardinality": "one",
                "lookup_external_column_id": "lookupExternalColumnId",
                "lookup_source_column_id": "lookupSourceColumnId",
                "name": "name",
                "type": "lookup",
            },
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(AddDatabaseColumnResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive_files(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.archive_files(
            file_ids=["string"],
        )
        assert_matches_type(object, client, path=["response"])

    @parametrize
    async def test_raw_response_archive_files(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.archive_files(
            file_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(object, client, path=["response"])

    @parametrize
    async def test_streaming_response_archive_files(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.archive_files(
            file_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(object, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_chat_create_thread(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.chat_create_thread(
            body={},
        )
        assert_matches_type(ChatCreateThreadResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_chat_create_thread(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.chat_create_thread(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ChatCreateThreadResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_chat_create_thread(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.chat_create_thread(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ChatCreateThreadResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_chat_list_messages(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.chat_list_messages(
            thread_id="threadId",
        )
        assert_matches_type(ChatListMessagesResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_chat_list_messages(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.chat_list_messages(
            thread_id="threadId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ChatListMessagesResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_chat_list_messages(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.chat_list_messages(
            thread_id="threadId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ChatListMessagesResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_chat_send_message(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
        )
        assert client is None

    @parametrize
    async def test_method_chat_send_message_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
            context={
                "databases": [
                    {
                        "database": {
                            "hid": "hid",
                            "hid_prefix": "hidPrefix",
                            "name": "name",
                        },
                        "columns": [{"name": "name"}],
                        "rows": [
                            {
                                "hid": "hid",
                                "name": "name",
                            }
                        ],
                    }
                ]
            },
        )
        assert client is None

    @parametrize
    async def test_raw_response_chat_send_message(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert client is None

    @parametrize
    async def test_streaming_response_chat_send_message(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.chat_send_message(
            messages=[
                {
                    "content": "x",
                    "role": "user",
                }
            ],
            thread_id="threadId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert client is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_configure_column_select_options(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.configure_column_select_options(
            column_id="columnId",
            database_id="databaseId",
            option_configuration=[
                {
                    "op": "add",
                    "option": "option",
                }
            ],
        )
        assert_matches_type(ConfigureColumnSelectOptionsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_configure_column_select_options(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.configure_column_select_options(
            column_id="columnId",
            database_id="databaseId",
            option_configuration=[
                {
                    "op": "add",
                    "option": "option",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ConfigureColumnSelectOptionsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_configure_column_select_options(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.configure_column_select_options(
            column_id="columnId",
            database_id="databaseId",
            option_configuration=[
                {
                    "op": "add",
                    "option": "option",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ConfigureColumnSelectOptionsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_convert_id_format(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.convert_id_format(
            conversions=[{"id": "id"}],
        )
        assert_matches_type(ConvertIDFormatResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_convert_id_format(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.convert_id_format(
            conversions=[{"id": "id"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ConvertIDFormatResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_convert_id_format(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.convert_id_format(
            conversions=[{"id": "id"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ConvertIDFormatResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_database(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
            },
        )
        assert_matches_type(CreateDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_method_create_database_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
                "cols": [{}],
                "is_inline_database": True,
                "parent_id": "parentId",
            },
        )
        assert_matches_type(CreateDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_create_database(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CreateDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_create_database(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.create_database(
            database={
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CreateDatabaseResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_file_download_url(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.create_file_download_url(
            file_id="fileId",
        )
        assert_matches_type(CreateFileDownloadURLResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_create_file_download_url(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.create_file_download_url(
            file_id="fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CreateFileDownloadURLResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_create_file_download_url(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.create_file_download_url(
            file_id="fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CreateFileDownloadURLResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_file_upload(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.create_file_upload(
            content_length="contentLength",
            name="name",
        )
        assert_matches_type(CreateFileUploadResponse, client, path=["response"])

    @parametrize
    async def test_method_create_file_upload_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.create_file_upload(
            content_length="contentLength",
            name="name",
            checksum_sha256="checksumSha256",
            content_type="contentType",
        )
        assert_matches_type(CreateFileUploadResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_create_file_upload(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.create_file_upload(
            content_length="contentLength",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CreateFileUploadResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_create_file_upload(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.create_file_upload(
            content_length="contentLength",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CreateFileUploadResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_workspace(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
            },
        )
        assert_matches_type(CreateWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_method_create_workspace_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
                "parent_id": "parentId",
            },
        )
        assert_matches_type(CreateWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_create_workspace(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CreateWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_create_workspace(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.create_workspace(
            workspace={
                "hid": "hid",
                "name": "name",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CreateWorkspaceResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete_database(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.delete_database(
            database_id="databaseId",
        )
        assert_matches_type(DeleteDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_delete_database(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.delete_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DeleteDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_delete_database(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.delete_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DeleteDatabaseResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete_database_column(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.delete_database_column(
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(DeleteDatabaseColumnResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_delete_database_column(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.delete_database_column(
            column_id="columnId",
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DeleteDatabaseColumnResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_delete_database_column(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.delete_database_column(
            column_id="columnId",
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DeleteDatabaseColumnResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete_rows(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.delete_rows(
            database_id="databaseId",
        )
        assert_matches_type(DeleteRowsResponse, client, path=["response"])

    @parametrize
    async def test_method_delete_rows_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.delete_rows(
            database_id="databaseId",
            delete_all=True,
            row_ids=["string"],
        )
        assert_matches_type(DeleteRowsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_delete_rows(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.delete_rows(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DeleteRowsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_delete_rows(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.delete_rows(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DeleteRowsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete_workspace(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.delete_workspace(
            workspace_id="workspaceId",
        )
        assert_matches_type(DeleteWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_delete_workspace(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.delete_workspace(
            workspace_id="workspaceId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DeleteWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_delete_workspace(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.delete_workspace(
            workspace_id="workspaceId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DeleteWorkspaceResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_describe_code_execution(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.describe_code_execution(
            id="id",
        )
        assert_matches_type(DescribeCodeExecutionResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_describe_code_execution(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.describe_code_execution(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DescribeCodeExecutionResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_describe_code_execution(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.describe_code_execution(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DescribeCodeExecutionResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_describe_database(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.describe_database(
            database_id="databaseId",
        )
        assert_matches_type(DescribeDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_describe_database(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.describe_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DescribeDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_describe_database(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.describe_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DescribeDatabaseResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_describe_database_stats(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.describe_database_stats(
            database_id="databaseId",
        )
        assert_matches_type(DescribeDatabaseStatsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_describe_database_stats(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.describe_database_stats(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DescribeDatabaseStatsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_describe_database_stats(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.describe_database_stats(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DescribeDatabaseStatsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_describe_file(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.describe_file(
            file_id="fileId",
        )
        assert_matches_type(DescribeFileResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_describe_file(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.describe_file(
            file_id="fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DescribeFileResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_describe_file(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.describe_file(
            file_id="fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DescribeFileResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_describe_row(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.describe_row(
            row_id="rowId",
        )
        assert_matches_type(DescribeRowResponse, client, path=["response"])

    @parametrize
    async def test_method_describe_row_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.describe_row(
            row_id="rowId",
            column_selection={
                "exclude": ["string"],
                "include": ["string"],
            },
            fields=True,
        )
        assert_matches_type(DescribeRowResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_describe_row(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.describe_row(
            row_id="rowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DescribeRowResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_describe_row(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.describe_row(
            row_id="rowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DescribeRowResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_describe_workspace(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.describe_workspace(
            workspace_id="workspaceId",
        )
        assert_matches_type(DescribeWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_describe_workspace(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.describe_workspace(
            workspace_id="workspaceId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(DescribeWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_describe_workspace(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.describe_workspace(
            workspace_id="workspaceId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(DescribeWorkspaceResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_download_file(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.download_file()
        assert client is None

    @parametrize
    async def test_raw_response_download_file(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.download_file()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert client is None

    @parametrize
    async def test_streaming_response_download_file(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.download_file() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert client is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_ensure_rows(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.ensure_rows(
            database_id="databaseId",
            rows=[{}],
        )
        assert_matches_type(EnsureRowsResponse, client, path=["response"])

    @parametrize
    async def test_method_ensure_rows_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.ensure_rows(
            database_id="databaseId",
            rows=[
                {
                    "cells": [
                        {
                            "column_id": "columnId",
                            "value": {},
                            "previous_version": 0,
                        }
                    ],
                    "row": {
                        "creation_block_id": "creationBlockId",
                        "creation_parent_id": "creationParentId",
                        "is_template": True,
                    },
                    "row_id": "rowId",
                }
            ],
            check_previous_value=True,
        )
        assert_matches_type(EnsureRowsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_ensure_rows(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.ensure_rows(
            database_id="databaseId",
            rows=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(EnsureRowsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_ensure_rows(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.ensure_rows(
            database_id="databaseId",
            rows=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(EnsureRowsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_execute_code_async(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.execute_code_async(
            code="code",
            code_language="python",
        )
        assert_matches_type(ExecuteCodeAsyncResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_execute_code_async(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.execute_code_async(
            code="code",
            code_language="python",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ExecuteCodeAsyncResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_execute_code_async(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.execute_code_async(
            code="code",
            code_language="python",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ExecuteCodeAsyncResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_execute_code_sync(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.execute_code_sync(
            code="code",
            code_language="python",
        )
        assert_matches_type(ExecuteCodeSyncResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_execute_code_sync(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.execute_code_sync(
            code="code",
            code_language="python",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ExecuteCodeSyncResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_execute_code_sync(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.execute_code_sync(
            code="code",
            code_language="python",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ExecuteCodeSyncResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get_code_execution_result(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.get_code_execution_result(
            id="id",
        )
        assert_matches_type(object, client, path=["response"])

    @parametrize
    async def test_raw_response_get_code_execution_result(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.get_code_execution_result(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(object, client, path=["response"])

    @parametrize
    async def test_streaming_response_get_code_execution_result(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.get_code_execution_result(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(object, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_import_rows(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.import_rows(
            database_id="databaseId",
        )
        assert_matches_type(ImportRowsResponse, client, path=["response"])

    @parametrize
    async def test_method_import_rows_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.import_rows(
            database_id="databaseId",
            add_columns=[
                {
                    "cardinality": "one",
                    "lookup_external_column_id": "lookupExternalColumnId",
                    "lookup_source_column_id": "lookupSourceColumnId",
                    "name": "name",
                    "type": "lookup",
                    "cell_json_schema": {},
                    "enabled_viewers": ["code"],
                    "inline_viewer": "molecule2d",
                    "is_required": True,
                    "system_type": "name",
                }
            ],
            creation_block_id="creationBlockId",
            creation_parent_id="creationParentId",
        )
        assert_matches_type(ImportRowsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_import_rows(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.import_rows(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ImportRowsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_import_rows(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.import_rows(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ImportRowsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_database_column_unique_values_v2(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_database_column_unique_values_v2(
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(ListDatabaseColumnUniqueValuesV2Response, client, path=["response"])

    @parametrize
    async def test_raw_response_list_database_column_unique_values_v2(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.list_database_column_unique_values_v2(
            column_id="columnId",
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ListDatabaseColumnUniqueValuesV2Response, client, path=["response"])

    @parametrize
    async def test_streaming_response_list_database_column_unique_values_v2(
        self, async_client: AsyncDeeporiginData
    ) -> None:
        async with async_client.with_streaming_response.list_database_column_unique_values_v2(
            column_id="columnId",
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ListDatabaseColumnUniqueValuesV2Response, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_database_rows(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_database_rows(
            database_row_id="databaseRowId",
        )
        assert_matches_type(ListDatabaseRowsResponse, client, path=["response"])

    @parametrize
    async def test_method_list_database_rows_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_database_rows(
            database_row_id="databaseRowId",
            column_selection={
                "exclude": ["string"],
                "include": ["string"],
            },
            filter={
                "column_id": "columnId",
                "filter_type": "text",
                "filter_value": "filterValue",
                "operator": "equals",
            },
            limit=1,
            offset=0,
            row_sort=[
                {
                    "column_id": "columnId",
                    "sort": "asc",
                }
            ],
        )
        assert_matches_type(ListDatabaseRowsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_list_database_rows(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.list_database_rows(
            database_row_id="databaseRowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ListDatabaseRowsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_list_database_rows(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.list_database_rows(
            database_row_id="databaseRowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ListDatabaseRowsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_files(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_files()
        assert_matches_type(ListFilesResponse, client, path=["response"])

    @parametrize
    async def test_method_list_files_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_files(
            filters=[
                {
                    "assigned_row_ids": ["string"],
                    "file_ids": ["string"],
                    "is_unassigned": True,
                    "status": ["ready"],
                }
            ],
        )
        assert_matches_type(ListFilesResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_list_files(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.list_files()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ListFilesResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_list_files(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.list_files() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ListFilesResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_mentions(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_mentions(
            query="query",
        )
        assert_matches_type(ListMentionsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_list_mentions(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.list_mentions(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ListMentionsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_list_mentions(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.list_mentions(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ListMentionsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_row_back_references(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_row_back_references(
            database_id="databaseId",
            row_id="rowId",
        )
        assert_matches_type(ListRowBackReferencesResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_list_row_back_references(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.list_row_back_references(
            database_id="databaseId",
            row_id="rowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ListRowBackReferencesResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_list_row_back_references(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.list_row_back_references(
            database_id="databaseId",
            row_id="rowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ListRowBackReferencesResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_rows(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.list_rows(
            filters=[{"parent": {"id": "id"}}],
        )
        assert_matches_type(ListRowsResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_list_rows(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.list_rows(
            filters=[{"parent": {"id": "id"}}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ListRowsResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_list_rows(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.list_rows(
            filters=[{"parent": {"id": "id"}}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ListRowsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_lock_database(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.lock_database(
            database_id="databaseId",
        )
        assert_matches_type(LockDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_lock_database(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.lock_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(LockDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_lock_database(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.lock_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(LockDatabaseResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_parse_base_sequence_data(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.parse_base_sequence_data(
            file_id="fileId",
        )
        assert_matches_type(ParseBaseSequenceDataResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_parse_base_sequence_data(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.parse_base_sequence_data(
            file_id="fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ParseBaseSequenceDataResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_parse_base_sequence_data(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.parse_base_sequence_data(
            file_id="fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ParseBaseSequenceDataResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_unlock_database(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.unlock_database(
            database_id="databaseId",
        )
        assert_matches_type(UnlockDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_unlock_database(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.unlock_database(
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(UnlockDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_unlock_database(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.unlock_database(
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(UnlockDatabaseResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update_database(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.update_database(
            id="id",
            database={},
        )
        assert_matches_type(UpdateDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_method_update_database_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.update_database(
            id="id",
            database={
                "editor": {},
                "hid": "hid",
                "hid_prefix": "hidPrefix",
                "name": "name",
                "parent_id": "parentId",
            },
        )
        assert_matches_type(UpdateDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_update_database(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.update_database(
            id="id",
            database={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(UpdateDatabaseResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_update_database(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.update_database(
            id="id",
            database={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(UpdateDatabaseResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    async def test_method_update_database_column(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.update_database_column(
            column={"type": "boolean"},
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(UpdateDatabaseColumnResponse, client, path=["response"])

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    async def test_method_update_database_column_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.update_database_column(
            column={
                "type": "boolean",
                "cardinality": "one",
                "cellJsonSchema": {},
                "enabledViewers": ["code"],
                "inlineViewer": "molecule2d",
                "isRequired": True,
                "name": "name",
                "systemType": "name",
            },
            column_id="columnId",
            database_id="databaseId",
        )
        assert_matches_type(UpdateDatabaseColumnResponse, client, path=["response"])

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    async def test_raw_response_update_database_column(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.update_database_column(
            column={"type": "boolean"},
            column_id="columnId",
            database_id="databaseId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(UpdateDatabaseColumnResponse, client, path=["response"])

    @pytest.mark.skip(reason="prism doesnt support discriminator")
    @parametrize
    async def test_streaming_response_update_database_column(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.update_database_column(
            column={"type": "boolean"},
            column_id="columnId",
            database_id="databaseId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(UpdateDatabaseColumnResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update_workspace(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.update_workspace(
            id="id",
            workspace={},
        )
        assert_matches_type(UpdateWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_method_update_workspace_with_all_params(self, async_client: AsyncDeeporiginData) -> None:
        client = await async_client.update_workspace(
            id="id",
            workspace={
                "editor": {},
                "hid": "hid",
                "name": "name",
                "parent_id": "parentId",
            },
        )
        assert_matches_type(UpdateWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_update_workspace(self, async_client: AsyncDeeporiginData) -> None:
        response = await async_client.with_raw_response.update_workspace(
            id="id",
            workspace={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(UpdateWorkspaceResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_update_workspace(self, async_client: AsyncDeeporiginData) -> None:
        async with async_client.with_streaming_response.update_workspace(
            id="id",
            workspace={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(UpdateWorkspaceResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True
