import ssl
from os import PathLike
from pathlib import Path
from typing import Dict, Generator, List, Literal, Tuple, Type, Union
from urllib.parse import urlparse

import httpx

from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor
from pipelet.processors.file_system import AbstractFileSystemManager

logger = logger_factory()


class HttpDataExtractProcessor(
    BaseProcessor[str | httpx._urls.URL, str | PathLike[str], None, None]
):
    """
    Processor for downloading data from an HTTP endpoint and saving it to the local file system.

    This processor sends an HTTP GET request to the specified URL, retrieves the data,
    and saves it to a file using the provided file system manager.

    Attributes:
        _file_system_manager (AbstractFileSystemManager[Union[str, PathLike[str]], Union[str, bytes]]): Manager for handling file system operations.
        _params (dict): Parameters to include in the HTTP request.
        _headers (dict): Headers to include in the HTTP request.
        _timeout (int): Timeout for the HTTP request in seconds.
        _follow_redirects (bool): Whether to follow redirects for the HTTP request.
        _cookies (dict): Cookies to include in the HTTP request.
        _auth (httpx.Auth): Authentication information for the HTTP request.
        _proxy (httpx.Proxy): Proxy information for the HTTP request.
        _cert (str | Tuple[str, str]): SSL certificate for the HTTP request.
        _verify (bool | str): Whether to verify SSL certificates.
        _trust_env (bool): Whether to trust environment variables for HTTP configuration.
    """

    def __init__(
        self,
        file_system_manager: AbstractFileSystemManager[
            Union[str, PathLike[str]], Union[str, bytes]
        ],
        white_exceptions: List[Type[Exception]] | None = None,
        params: Dict[str, str] | None = None,
        headers: Dict[str, str] | None = None,
        timeout: int | None = 120,
        follow_redirects: bool = False,
        cookies: Dict[str, str] | None = None,
        auth: httpx.Auth | None = None,
        proxy: httpx.Proxy | None = None,
        cert: str | Tuple[str, str] | None = None,
        verify: Union[str, bool, ssl.SSLContext] = True,
        trust_env: bool = True,
    ) -> None:
        """
        Initializes the HttpDataExtractProcessor.

        Args:
            file_system_manager (AbstractFileSystemManager[
                    Union[str, PathLike[str]], Union[str, bytes]
                ]
            ): A file system manager to handle file creation.
            white_exceptions (List[Type[BaseProcessorException]] | None): List of exceptions to allow in processing.
            params (Dict[str, str] | None): URL parameters for the HTTP request.
            headers (Dict[str, str] | None): Headers for the HTTP request.
            timeout (int | None): Timeout for the HTTP request.
            follow_redirects (bool): Whether to follow redirects.
            cookies (Dict[str, str] | None): Cookies for the HTTP request.
            auth (httpx.Auth | None): Authentication details for the HTTP request.
            proxy (httpx.Proxy | None): Proxy settings for the HTTP request.
            cert (str | Tuple[str, str] | None): SSL certificate for the HTTP request.
            verify (bool | str | None): SSL verification flag.
            trust_env (bool | None): Whether to trust environment variables.
        """
        super().__init__(white_exceptions)
        self._file_system_manager = file_system_manager
        self._params = params or {}
        self._headers = headers or {}
        self._timeout = timeout
        self._follow_redirects = follow_redirects
        self._cookies = cookies or {}
        self._auth = auth
        self._proxy = proxy
        self._cert = cert
        self._verify = verify
        self._trust_env = trust_env

    def process(
        self, input_data: str | httpx._urls.URL
    ) -> Generator[PathLike | str, None, None]:
        """
        Downloads data from the provided URL and saves it to the file system.

        The method retrieves the content from the specified URL using HTTP GET, saves it
        to a file using the file system manager, and passes the file name to the next processor
        (if any) in the chain.

        Args:
            input_data (str): The URL to download data from.

        Yields:
            PathLike | str: The file name or path of the downloaded file.
        """
        resp = httpx.get(
            input_data,
            params=self._params,
            headers=self._headers,
            timeout=self._timeout,
            follow_redirects=self._follow_redirects,
            cookies=self._cookies,
            auth=self._auth,
            proxy=self._proxy,
            cert=self._cert,
            verify=self._verify,
            trust_env=self._trust_env,
        )
        resp.raise_for_status()

        parsed_url = urlparse(str(input_data))
        file_name = Path(parsed_url.path).name
        self._file_system_manager.create_file(
            file_name,
            resp.content,
        )

        if self._next is not None:
            yield from self._next.process(file_name)
        else:
            yield file_name

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"headers={self._headers}, "
            f"params={self._params})"
        )


class HttpxStreamDownloadProcessor(
    BaseProcessor[str | httpx._urls.URL, str | PathLike[str], None, None]
):
    """
    Processor for downloading large files from an HTTP endpoint using streaming.

    This processor downloads data from a specified URL using streaming (i.e., chunked
    transfer encoding). This is useful for downloading large files that may not fit into
    memory entirely. The file is saved using the provided file system manager.

    Attributes:
        _file_system_manager (AbstractFileSystemManager[Union[str, PathLike[str]], Union[str, bytes]]): Manager for handling file system operations.
        _chunk_size (int): The size of each chunk of data to download.
        _method (str): The HTTP method to use (GET, POST, etc.).
        _headers (dict): Headers to include in the HTTP request.
        _params (dict): Parameters to include in the HTTP request.
        _cookies (dict): Cookies to include in the HTTP request.
        _timeout (float): Timeout for the HTTP request.
        _proxies (str | dict): Proxy settings for the HTTP request.
        _verify (bool | str): Whether to verify SSL certificates.
    """

    def __init__(
        self,
        file_system_manager: AbstractFileSystemManager[
            Union[str, PathLike[str]], Union[str, bytes]
        ],
        white_exceptions: List[Type[Exception]] | None = None,
        chunk_size: int | None = 8192,
        method: Literal["GET", "POST", "PUT", "PATCH"] = "GET",
        headers: dict | None = None,
        params: dict | None = None,
        cookies: dict | None = None,
        timeout: float | None = None,
        proxies: str | dict | None = None,
        verify: bool | str = True,
    ) -> None:
        """
        Initializes the HttpxStreamDownloadProcessor.

        Args:
            file_system_manager (AbstractFileSystemManager[Union[str, PathLike[str]], Union[str, bytes]]): A file system manager to handle file creation.
            white_exceptions (List[Type[BaseProcessorException]] | None): List of exceptions to allow in processing.
            chunk_size (int | None): The size of each chunk to download.
            method (Literal): The HTTP method to use (GET, POST, etc.).
            headers (dict | None): Headers for the HTTP request.
            params (dict | None): Parameters for the HTTP request.
            cookies (dict | None): Cookies for the HTTP request.
            timeout (float | None): Timeout for the HTTP request.
            proxies (str | dict | None): Proxy settings for the HTTP request.
            verify (bool | str): Whether to verify SSL certificates.
        """
        super().__init__(white_exceptions)
        self._file_system_manager = file_system_manager
        self._chunk_size = chunk_size
        self._method = method
        self._headers = headers or {}
        self._params = params or {}
        self._cookies = cookies or {}
        self._timeout = timeout
        self._proxies = proxies
        self._verify = verify

    def process(
        self, input_data: str | httpx._urls.URL
    ) -> Generator[PathLike[str] | str, None, None]:
        """
        Downloads data from the provided URL using streaming and saves it to the file system.

        This method downloads the content of a URL in chunks, which is useful for large
        files. It saves the content to a file and passes the file path to the next processor
        (if any) in the chain.

        Args:
            input_data (str): The URL to download data from.

        Yields:
            PathLike[str] | str: The file path of the downloaded file.
        """
        with httpx.stream(
            method=self._method,
            url=input_data,
            headers=self._headers,
            params=self._params,
            cookies=self._cookies,
            timeout=self._timeout,
            proxies=self._proxies,
            verify=self._verify,
        ) as resp:
            resp.raise_for_status()
            parsed_url = urlparse(str(input_data))
            file_name = Path(parsed_url.path).name
            file_path = self._file_system_manager.get_path(file_name)
            self._file_system_manager.create_file(file_path)
            for chunk in resp.iter_bytes(chunk_size=self._chunk_size):
                if chunk:
                    self._file_system_manager.append_to_file(file_path, chunk)

            if self._next is not None:
                yield from self._next.process(file_path)
            else:
                yield file_path

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(chunk_size={self._chunk_size}, "
            f"method={self._method}, "
            f"headers={self._headers}, "
            f"params={self._params})"
        )
