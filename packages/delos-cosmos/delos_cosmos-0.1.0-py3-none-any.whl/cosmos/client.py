"""Client for interacting with the Cosmos API."""

from pathlib import Path
from typing import Any

import requests

from cosmos.exceptions import APIKeyMissingError

from .endpoints import Endpoints, RequestMethod
from .models import FileTranslationReturnType, ParserExtractType
from .releases import AllReleases
from .setup import logger

COSMOS_PLATFORM_BACKEND_URL = "https://platform.cosmos-suite.ai"


class CosmosClient:
    """Client for interacting with the Cosmos API.

    Attributes:
        server_url: The URL of the server.
        apikey: The API key to be used for requests.

    """

    def __init__(
        self: "CosmosClient",
        apikey: str | None = None,
        server_url: str | None = COSMOS_PLATFORM_BACKEND_URL,
        debug_mode: bool = False,
    ) -> None:
        """Initialize the client with the server URL and API key.

        Args:
            apikey: The API key to be used for requests.
            server_url: The URL of the server.
            debug_mode: Whether to enable debug mode.
        """
        if apikey is None:
            raise APIKeyMissingError

        self.apikey = apikey
        self.server_url = server_url

        self.session = requests.Session()
        self.session.headers.update({"apikey": self.apikey})

        self._client_version = AllReleases[0]
        self._debug_mode = debug_mode

    def _make_request(
        self,
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to the specified endpoint with the given data and files.

        Args:
            apikey: The Cosmos key to be used for the request.
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            _print_this_request: Whether to print the request (default is False).

        Returns:
            The response from the request as a dictionary, or None if an error occurred.

        """
        url = f"{self.server_url}{self._client_version.suffix}{endpoint[0]}"
        request_method = endpoint[1].value
        request_func = {
            RequestMethod.GET: self.session.get,
            RequestMethod.POST: self.session.post,
            RequestMethod.PUT: self.session.put,
            RequestMethod.DELETE: self.session.delete,
        }.get(request_method)

        if not request_func:
            unsupported_method_error = f"Unsupported HTTP method: {request_method}"
            raise ValueError(unsupported_method_error)

        if self._debug_mode or _print_this_request:
            logger.debug(f"Request URL: {url}")
            logger.debug(f"Request Method: {request_method}")
            logger.debug(f"Request Data: {data}")
            logger.debug(f"Request Files: {files}")
            logger.debug(f"Request Params: {params}")
        try:
            response = request_func(url, files=files, data=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
            logger.error(f"Response Content: {response.text}")
            raise

    def status_health_request(
        self: "CosmosClient",
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to check the health of the server."""
        return self._make_request(
            Endpoints.STATUS.HEALTH.value,
            _print_this_request=_print_this_request,
        )

    def translate_text_request(
        self: "CosmosClient",
        text: str,
        output_language: str,
        input_language: str | None = None,
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to translate text.

        Args:
            text: The text to be translated.
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).

        Returns:
            The server response.
        """
        data = {
            "text": text,
            "output_language": output_language,
        }
        if input_language:
            data["input_language"] = input_language
        return self._make_request(
            endpoint=Endpoints.TRANSLATE.TRANSLATE_TEXT.value,
            data=data,
            _print_this_request=_print_this_request,
        )

    def translate_file_request(
        self: "CosmosClient",
        filepath: Path,
        output_language: str,
        input_language: str | None = None,
        return_type: FileTranslationReturnType = FileTranslationReturnType.RAW_TEXT.value,
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to translate a file.

        Args:
            filepath: The file path to be translated.
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).
            return_type: The type of return for the translation (Optional). Default is "raw_text".

        Returns:
            The server response.
        """
        data = {
            "output_language": output_language,
            "return_type": return_type,
        }
        if input_language:
            data["input_language"] = input_language

        files = {"file": (filepath.name, filepath.open("rb"))}
        return self._make_request(
            Endpoints.TRANSLATE.TRANSLATE_FILE.value,
            data=data,
            files=files,
            _print_this_request=_print_this_request,
        )

    def web_search_request(
        self: "CosmosClient",
        text: str,
        output_language: str | None = None,
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to perform a search.

        Args:
            text: The text to be searched.
            output_language: The output language for the search (Optional).

        Returns:
            The server response.
        """
        data = {
            "text": text,
        }
        if output_language:
            data["output_language"] = output_language
        return self._make_request(Endpoints.WEB.SEARCH.value, data, _print_this_request=_print_this_request)

    def llm_chat_request(
        self: "CosmosClient",
        text: str,
        model: str | None = None,
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to chat with the LLM.

        Args:
            text: The text to be chatted.
            model: The model to be used for chatting (Optional).

        Returns:
            The server response.
        """
        data = {"text": text}
        if model:
            data["model"] = model
        return self._make_request(endpoint=Endpoints.LLM.CHAT.value, data=data, _print_this_request=_print_this_request)

    def llm_embed_request(
        self: "CosmosClient",
        text: str,
        model: str | None = None,
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to embed data using the LLM.

        Args:
            text: The text to be embedded.
            model: The model to be used for embedding (Optional).

        Returns:
            The server response.
        """
        data = {"text": text}
        if model:
            data["model"] = model
        return self._make_request(Endpoints.LLM.EMBED.value, data, _print_this_request=_print_this_request)

    def files_parse_request(
        self: "CosmosClient",
        filepath: Path,
        extract_type: ParserExtractType = ParserExtractType.CHUNKS,
        k_min: int | None = None,
        k_max: int | None = None,
        overlap: int | None = None,
        filter_pages: str | None = None,
        _print_this_request: bool = False,
    ) -> dict[str, Any] | None:
        """Make a request to chunk a file.

        Args:
            filepath: The file path to be chunked.
            extract_type: The type of extraction to be performed (Optional). Default is "subchunks".
            k_min: The minimum number of chunks to be extracted (Optional). Default is 500 tokens.
            k_max: The maximum number of chunks to be extracted (Optional). Default is 1000 tokens.
            overlap: The overlap between chunks (Optional). Default is 10 tokens.
            filter_pages: The filter for pages (Optional). Default is all pages.

        Returns:
            The server response.
        """
        files = {"file": (filepath.name, filepath.open("rb"))}
        data = {
            "extract_type": extract_type.value,
            "k_min": k_min,
            "k_max": k_max,
            "overlap": overlap,
            "filter_pages": filter_pages,
        }
        return self._make_request(
            Endpoints.FILES.PARSER.value,
            data=data,
            files=files,
            _print_this_request=_print_this_request,
        )

    def files_index_create_request(
        self: "CosmosClient",
        filepaths: list[Path],
        name: str,
        _print_this_request: bool = False,
    ) -> str:
        """Make a request to create an index.

        Args:
            filepaths: A list of file paths to be indexed.
            name: The name of the index.

        Returns:
            The server response.
        """
        files_upfiles = {(filepath.name, filepath.open("rb")) for filepath in filepaths}
        return self._make_request(
            Endpoints.FILES.INDEX_CREATE.value,
            files={"files": files_upfiles},
            data={"name": name},
            _print_this_request=_print_this_request,
        )

    def files_index_add_files_request(
        self: "CosmosClient",
        index_uuid: str,
        filepaths: list[Path],
        _print_this_request: bool = False,
    ) -> str:
        """Make a request to add files to an index.

        Args:
            index_uuid: The index UUID.
            filepaths: A list of file paths to be added to the index.

        Returns:
            The server response.
        """
        files_upfiles = {(filepath.name, filepath.open("rb")) for filepath in filepaths}
        return self._make_request(
            Endpoints.FILES.INDEX_ADD_FILES.value,
            files={"files": files_upfiles},
            data={"index_uuid": index_uuid},
            _print_this_request=_print_this_request,
        )

    def files_index_delete_files_request(
        self: "CosmosClient",
        index_uuid: str,
        files_hashes: list[str],
        _print_this_request: bool = False,
    ) -> str:
        """Make a request to delete files from an index.

        Args:
            index_uuid: The index UUID.
            files_hashes: A list of file hashes to be deleted from the index.

        Returns:
            The server response.
        """
        data = {"index_uuid": index_uuid, "files_hashes": files_hashes}
        return self._make_request(
            Endpoints.FILES.INDEX_DELETE_FILES.value,
            data=data,
            _print_this_request=_print_this_request,
        )

    def files_index_delete_request(self: "CosmosClient", index_uuid: str, _print_this_request: bool = False) -> str:
        """Make a request to delete an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.
        """
        data = {"index_uuid": index_uuid}
        return self._make_request(
            Endpoints.FILES.INDEX_DELETE.value,
            data=data,
            _print_this_request=_print_this_request,
        )

    def files_index_restore_request(self: "CosmosClient", index_uuid: str, _print_this_request: bool = False) -> str:
        """Make a request to restore an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.
        """
        data = {"index_uuid": index_uuid}
        return self._make_request(
            Endpoints.FILES.INDEX_RESTORE.value,
            data=data,
            _print_this_request=_print_this_request,
        )

    def files_index_rename_request(
        self: "CosmosClient",
        index_uuid: str,
        name: str,
        _print_this_request: bool = False,
    ) -> str:
        """Make a request to rename an index.

        Args:
            index_uuid: The index UUID.
            name: The new name for the index.

        Returns:
            The server response.
        """
        data = {"index_uuid": index_uuid, "name": name}
        return self._make_request(
            Endpoints.FILES.INDEX_RENAME.value,
            data=data,
            _print_this_request=_print_this_request,
        )

    def files_index_ask_request(
        self: "CosmosClient",
        index_uuid: str,
        question: str,
        output_language: str | None = None,
        active_files_hashes: list[str] | None = None,
        _print_this_request: bool = False,
    ) -> str:
        """Make a request to ask a question about the index contents.

        Args:
            index_uuid: The index UUID.
            question: The question to be asked.
            output_language: The output language for the question.
            active_files_hashes: The hashes of the files to be used for the question.

        Returns:
            The server response.
        """
        data = {"index_uuid": index_uuid, "question": question}
        if output_language:
            data["output_language"] = output_language
        if active_files_hashes:
            data["active_files_hashes"] = active_files_hashes
        return self._make_request(Endpoints.FILES.INDEX_ASK.value, data=data, _print_this_request=_print_this_request)

    def files_index_embed_request(self: "CosmosClient", index_uuid: str, _print_this_request: bool = False) -> str:
        """Make a request to embed an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.
        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_EMBED.value, data=data, _print_this_request=_print_this_request)

    def files_index_details_request(self: "CosmosClient", index_uuid: str, _print_this_request: bool = False) -> str:
        """Make a request to get details of an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.
        """
        params = {"index_uuid": index_uuid}
        return self._make_request(
            Endpoints.FILES.INDEX_DETAILS.value,
            params=params,
            _print_this_request=_print_this_request,
        )

    def files_index_list_request(self: "CosmosClient", _print_this_request: bool = False) -> str:
        """Make a request to list all indexes."""
        return self._make_request(Endpoints.FILES.INDEX_LIST.value, _print_this_request=_print_this_request)
