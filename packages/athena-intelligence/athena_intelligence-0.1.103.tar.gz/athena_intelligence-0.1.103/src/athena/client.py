import enum
import io
import os
import typing
import warnings

import httpx
from typing import cast, List, Union
from typing_extensions import TypeVar, ParamSpec

from .base_client import BaseAthena, AsyncBaseAthena
from .environment import AthenaEnvironment
from .tools.client import AsyncToolsClient, ToolsClient
from .query.client import AsyncQueryClient, QueryClient
from .types.data_frame_request_out import DataFrameRequestOut

if typing.TYPE_CHECKING:
    import pandas as pd


P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar('U')


def _inherit_signature_and_doc(
    f: typing.Callable[P, T],
    replace_in_doc: typing.Dict[str, str]
) -> typing.Callable[..., typing.Callable[P, U]]:
    def decorator(decorated):
        for old, new in replace_in_doc.items():
            assert old in f.__doc__
            decorated.__doc__ = f.__doc__.replace(old, new)
        return decorated
    return decorator


class SpecialEnvironments(enum.Enum):
    AUTODETECT_ENVIRONMENT = 'AUTO'


class WrappedToolsClient(ToolsClient):

    def get_file(self, asset_id: str) -> io.BytesIO:
        """
        Parameters
        ----------
        asset_id : str

        Returns
        -------
        io.BytesIO

        Examples
        --------
        import polars as pl
        from athena.client import Athena

        client = Athena(api_key="YOUR_API_KEY")
        file_io = client.tools.get_file(asset_id="asset_id")
        pl.read_csv(file_io)
        """
        file_bytes = b''.join(self.raw_data(asset_id=asset_id))
        bytes_io = io.BytesIO(file_bytes)
        return bytes_io

    @_inherit_signature_and_doc(ToolsClient.data_frame, {'DataFrameRequestOut': 'pd.DataFrame'})
    def data_frame(self, *, asset_id: str, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = super().data_frame(asset_id=asset_id, **kwargs)
        return _read_json_frame(model)

    def read_data_frame(self, asset_id: str, *args, **kwargs) -> 'pd.DataFrame':
        """
        Parameters
        ----------
        asset_id : str

        **kwargs : dict
          keyword arguments passed to pandas `read_csv` or `read_excel` function,
          depending on the file type of the document identified by `asset_id`.

        Returns
        -------
        pd.DataFrame

        Examples
        --------
        from athena.client import Athena

        client = Athena(api_key="YOUR_API_KEY")
        client.tools.read_data_frame(asset_id="asset_id")
        """
        _check_pandas_installed()
        file_bytes = self.get_file(asset_id)
        return _to_pandas_df(file_bytes, *args, **kwargs)


class WrappedQueryClient(QueryClient):

    @_inherit_signature_and_doc(QueryClient.execute, {'DataFrameRequestOut': 'pd.DataFrame'})
    def execute(self, *, sql_command: str, database_asset_ids: Union[str, List[str]], **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = super().execute(
            sql_command=sql_command,
            database_asset_ids=database_asset_ids,
            **kwargs
        )
        return _read_json_frame(model)

    @_inherit_signature_and_doc(QueryClient.execute_snippet, {'DataFrameRequestOut': 'pd.DataFrame'})
    def execute_snippet(self, *, snippet_asset_id: str, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = super().execute_snippet(snippet_asset_id=snippet_asset_id, **kwargs)
        return _read_json_frame(model)


def _add_docs_for_async_variant(obj):
    def decorator(decorated):
        doc = obj.__doc__
        name = obj.__name__
        decorated.__doc__ = (
            doc
            .replace('client = Athena', 'client = AsyncAthena')
            .replace(f'client.tools.{name}', f'await client.tools.{name}')
        )
        return decorated
    return decorator


class WrappedAsyncToolsClient(AsyncToolsClient):

    @_add_docs_for_async_variant(WrappedToolsClient.get_file)
    async def get_file(self, asset_id: str) -> io.BytesIO:
        file_bytes = b''.join([gen async for gen in self.raw_data(asset_id=asset_id)])
        bytes_io = io.BytesIO(file_bytes)
        return bytes_io

    @_inherit_signature_and_doc(AsyncToolsClient.data_frame, {'DataFrameRequestOut': 'pd.DataFrame'})
    async def data_frame(self, *, asset_id: str, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = await super().data_frame(asset_id=asset_id, **kwargs)
        return _read_json_frame(model)

    @_add_docs_for_async_variant(WrappedToolsClient.read_data_frame)
    async def read_data_frame(self, asset_id: str, *args, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        file_bytes = await self.get_file(asset_id)
        return _to_pandas_df(file_bytes, *args, **kwargs)


class WrappedAsyncQueryClient(AsyncQueryClient):

    @_inherit_signature_and_doc(AsyncQueryClient.execute, {'DataFrameRequestOut': 'pd.DataFrame'})
    async def execute(self, *, sql_command: str, database_asset_ids: Union[str, List[str]], **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = await super().execute(
            sql_command=sql_command,
            database_asset_ids=database_asset_ids,
            **kwargs
        )
        return _read_json_frame(model)

    @_inherit_signature_and_doc(AsyncQueryClient.execute_snippet, {'DataFrameRequestOut': 'pd.DataFrame'})
    async def execute_snippet(self, *, snippet_asset_id: str, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = await super().execute_snippet(snippet_asset_id=snippet_asset_id, **kwargs)
        return _read_json_frame(model)


class Athena(BaseAthena):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : AthenaEnvironment
        The environment to use for requests from the client.

        Defaults to `AthenaEnvironment.PRODUCTION` when outside of athena notebook environment.

    api_key: typing.Optional[str].  The API key. Required when used outside of the athena notebook environment.
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from athena.client import Athena

    client = Athena(
        api_key="YOUR_API_KEY",
    )
    """

    tools: WrappedToolsClient

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: Union[AthenaEnvironment, SpecialEnvironments] = SpecialEnvironments.AUTODETECT_ENVIRONMENT,    # type: ignore[arg-type]
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        if api_key is None:
            try:
                api_key = os.environ['ATHENA_API_KEY']
            except KeyError:
                raise TypeError(
                    "Athena() missing 1 required keyword-only argument: 'api_key'"
                    ' (ATHENA_API_KEY environment variable not found)'
                )
        if environment == SpecialEnvironments.AUTODETECT_ENVIRONMENT:
            if 'ATHENA_API_URL' in os.environ:

                class AutodetectedEnvironments(enum.Enum):
                    CURRENT = os.environ['ATHENA_API_URL']

                environment = cast(AthenaEnvironment, AutodetectedEnvironments.CURRENT)
            else:
                environment = AthenaEnvironment.PRODUCTION
        super().__init__(
            base_url=base_url,
            environment=environment,    # type: ignore[arg-type]
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client,
        )
        self.tools = WrappedToolsClient(client_wrapper=self._client_wrapper)
        self.query = WrappedQueryClient(client_wrapper=self._client_wrapper)


class AsyncAthena(AsyncBaseAthena):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.


    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : AthenaEnvironment
        The environment to use for requests from the client.

        Defaults to `AthenaEnvironment.PRODUCTION` when outside of athena notebook environment.

    api_key: typing.Optional[str].  The API key. Required when used outside of the athena notebook environment.
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from athena.client import AsyncAthena

    client = AsyncAthena(
        api_key="YOUR_API_KEY",
    )
    """

    tools: WrappedAsyncToolsClient

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: Union[AthenaEnvironment, SpecialEnvironments] = SpecialEnvironments.AUTODETECT_ENVIRONMENT,    # type: ignore[arg-type]
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        if api_key is None:
            try:
                api_key = os.environ['ATHENA_API_KEY']
            except KeyError:
                raise TypeError(
                    "AsyncAthena() missing 1 required keyword-only argument: 'api_key'"
                    ' (ATHENA_API_KEY environment variable not found)'
                )
        if environment == SpecialEnvironments.AUTODETECT_ENVIRONMENT:
            if 'ATHENA_API_URL' in os.environ:

                class AutodetectedEnvironments(enum.Enum):
                    CURRENT = os.environ['ATHENA_API_URL']

                environment = cast(AthenaEnvironment, AutodetectedEnvironments.CURRENT)
            else:
                environment = AthenaEnvironment.PRODUCTION
        super().__init__(
            base_url=base_url,
            environment=environment,    # type: ignore[arg-type]
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client,
        )
        self.tools = WrappedAsyncToolsClient(client_wrapper=self._client_wrapper)
        self.query = WrappedAsyncQueryClient(client_wrapper=self._client_wrapper)


def _read_json_frame(model: DataFrameRequestOut) -> 'pd.DataFrame':
    import pandas as pd

    string_io = io.StringIO(model.json())

    with warnings.catch_warnings():
        # Filter warnings due to https://github.com/pandas-dev/pandas/issues/59511
        warnings.simplefilter(action='ignore', category=FutureWarning)
        return pd.read_json(string_io, orient='split')


def _check_pandas_installed():
    import pandas
    assert pandas


def _to_pandas_df(bytes_io: io.BytesIO, *args, **kwargs):
    import pandas as pd
    import magic

    # ideally this would be read from response header, but fern SDK for Python hides this info from us
    media_type = magic.from_buffer(bytes_io.read(2048), mime=True)
    bytes_io.seek(0)

    if media_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return pd.read_excel(bytes_io, *args, engine='openpyxl', **kwargs)
    elif media_type == 'application/vnd.ms-excel':
        return pd.read_excel(bytes_io, *args, **kwargs)
    elif media_type == 'text/csv':
        return pd.read_csv(bytes_io, *args, **kwargs)
    else:
        raise Exception("Unknown media type")
