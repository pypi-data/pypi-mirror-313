from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Generator, List, Literal, Optional, Union

import grpc._channel
import pyarrow as pa
import requests

from . import exceptions
from ._common import BAUPLAN_VERSION, Constants
from ._common_getters import (
    _get_branch_name,
    _get_namespace_name,
    _get_optional_branch_name,
    _get_optional_namespace_name,
    _get_optional_ref_name,
    _get_quoted_url,
    _get_ref_name,
    _get_table_name,
)
from ._common_operation import _JobLifeCycleHandler, _lifecycle, _OperationContainer
from ._info import InfoState, _Info
from ._profile import Profile
from ._query import _Query
from ._run import ReRunState, RunState, _Run
from ._table_create_plan import TableCreatePlanApplyState, TableCreatePlanState, _TableCreate
from ._table_data_import import TableDataImportState, _TableImport
from .schema import APIResponse, Branch, Namespace, Ref, Table, TableWithMetadata


class Client(_OperationContainer):
    """
    A consistent interface to access Bauplan operations.

    **Using the client**

    .. code-block:: python

        import bauplan
        client = bauplan.Client()

        # query the table and return result set as an arrow Table
        my_table = client.query('SELECT sum(trips) trips FROM travel_table', branch_name='main')

        # efficiently cast the table to a pandas DataFrame
        df = my_table.to_pandas()

    **Notes on authentication**

    .. code-block:: python

        # by default, authenticate from BAUPLAN_API_KEY >> BAUPLAN_PROFILE >> ~/.bauplan/config.yml
        client = bauplan.Client()
        # client used ~/.bauplan/config.yml profile 'default'

        os.environ['BAUPLAN_PROFILE'] = "someprofile"
        client = bauplan.Client()
        # >> client now uses profile 'someprofile'

        os.environ['BAUPLAN_API_KEY'] = "mykey"
        client = bauplan.Client()
        # >> client now authenticates with api_key value "mykey", because api key > profile

        # specify authentication directly - this supercedes BAUPLAN_API_KEY in the environment
        client = bauplan.Client(api_key='MY_KEY')

        # specify a profile from ~/.bauplan/config.yml - this supercedes BAUPLAN_PROFILE in the environment
        client = bauplan.Client(profile='default')

    **Handling Exceptions**

    Catalog operations (branch/table methods) raise a subclass of ``bauplan.exceptions.BauplanError`` that mirror HTTP status codes.

        * 400: InvalidDataError
        * 401: UnauthorizedError
        * 403: AccessDeniedError
        * 404: ResourceNotFoundError e.g .ID doesn't match any records
        * 404: ApiRouteError e.g. the given route doesn't exist
        * 405: ApiMethodError e.g. POST on a route with only GET defined
        * 409: UpdateConflictError e.g. creating a record with a name that already exists
        * 429: TooManyRequestsError

    Run/Query/Scan/Import operations raise a subclass of ``bauplan.exceptions.BauplanError`` that represents, and also return a ``RunState`` object containing details and logs:

        * ``JobError`` e.g. something went wrong in a run/query/import/scan; includes error details

    Run/import operations also return a state object that includes a ``job_status`` and other details.
    There are two ways to check status for run/import operations:
        1. try/except the JobError exception
        2. check the ``state.job_status`` attribute

    Examples:

    .. code-block:: python

        try:
            state = client.run(...)
            state = client.query(...)
            state = client.scan(...)
            state = client.plan_table_creation(...)
        except bauplan.exceptions.JobError as e:
            ...

        state = client.run(...)
        if state.job_status != "success":
            ...


    :param profile: (optional) The Bauplan config profile name to use to determine api_key.
    :param api_key: (optional) Your unique Bauplan API key; mutually exclusive with ``profile``. If not provided, fetch precedence is 1) environment BAUPLAN_API_KEY 2) .bauplan/config.yml
    :param branch: (optional) The default branch to use for queries and runs. If not provided active_branch from the profile is used.
    :param namespace: (optional) The default namespace to use for queries and runs.
    :param cache: (optional) Whether to enable or disable caching for all the requests.
    :param debug: (optional) Whether to enable or disable debug mode for all the requests.
    :param verbose: (optional) Whether to enable or disable verbose mode for all the requests.
    :param args: (optional) Additional arguments to pass to all the requests.
    :param api_endpoint: (optional) The Bauplan API endpoint to use. If not provided, fetch precedence is 1) environment BAUPLAN_API_ENDPOINT 2) .bauplan/config.yml
    :param catalog_endpoint: (optional) The Bauplan catalog endpoint to use. If not provided, fetch precedence is 1) environment BAUPLAN_CATALOG_ENDPOINT 2) .bauplan/config.yml
    :param client_timeout: (optional) The client timeout in seconds for all the requests.
    :param env: (optional) The environment to use for all the requests. Default: 'prod'.
    :param config_file_path: (optional) The path to the Bauplan config file to use. If not provided, fetch precedence is 1) environment BAUPLAN_CONFIG_PATH 2) ~/.bauplan/config.yml
    :param user_session_token: (optional) Your unique Bauplan user session token.
    """

    def __init__(
        self,
        profile: Optional[str] = None,
        api_key: Optional[str] = None,
        branch: Optional[str] = None,
        namespace: Optional[str] = None,
        cache: Optional[Literal['on', 'off']] = None,
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        api_endpoint: Optional[str] = None,
        catalog_endpoint: Optional[str] = None,
        client_timeout: Optional[int] = None,
        env: Optional[str] = None,
        config_file_path: Optional[Union[str, Path]] = None,
        user_session_token: Optional[str] = None,
        feature_flags: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            profile=Profile.load_profile(
                profile=profile,
                api_key=api_key,
                user_session_token=user_session_token,
                branch=branch,
                namespace=namespace,
                cache=cache,
                debug=debug,
                verbose=verbose,
                args=args,
                api_endpoint=api_endpoint,
                catalog_endpoint=catalog_endpoint,
                client_timeout=client_timeout,
                env=env,
                config_file_path=config_file_path,
                feature_flags=feature_flags,
            ),
        )

        # instantiate interfaces to authenticated modules
        self._query = _Query(self.profile)
        self._run = _Run(self.profile)
        self._table_create = _TableCreate(self.profile)
        self._table_import = _TableImport(self.profile)
        self._info = _Info(self.profile)

    # Run

    def run(
        self,
        project_dir: Optional[str] = None,
        ref: Optional[Union[str, Branch, Ref]] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        parameters: Optional[Dict[str, Optional[Union[str, int, float, bool]]]] = None,
        cache: Optional[Literal['on', 'off']] = None,
        transaction: Optional[Literal['on', 'off']] = None,
        dry_run: Optional[bool] = None,
        strict: Optional[Literal['on', 'off']] = None,
        preview: Optional[Union[Literal['on', 'off', 'head', 'tail'], str]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> RunState:
        """
        Run a Bauplan project and return the state of the run. This is the equivalent of
        running through the CLI the ``bauplan run`` command.

        :param project_dir: The directory of the project (where the ``bauplan_project.yml`` file is located).
        :param ref: The ref or branch name to read.
        :param namespace: The Namespace to run the job in. If not set, the job will be run in the default namespace.
        :param parameters: Parameters for templating into SQL or Python models.
        :param cache: Whether to enable or disable caching for the run.
        :param transaction: Whether to enable or disable transaction mode for the run.
        :param dry_run: Whether to enable or disable dry-run mode for the run; models are not materialized.
        :param strict: Whether to enable or disable strict schema validation.
        :param preview: Whether to enable or disable preview mode for the run.
        :param debug: Whether to enable or disable debug mode for the run.
        :param args: Additional arguments (optional).
        :param verbose: Whether to enable or disable verbose mode for the run.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The state of the run.
        """
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._run.run(
                project_dir=project_dir,
                ref=ref_name,
                namespace=namespace_name,
                parameters=parameters,
                cache=cache,
                transaction=transaction,
                dry_run=dry_run,
                strict=strict,
                preview=preview,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def rerun(
        self,
        job_id: str,
        ref: Optional[Union[str, Branch, Ref]] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        cache: Optional[Literal['on', 'off']] = None,
        transaction: Optional[Literal['on', 'off']] = None,
        dry_run: Optional[bool] = None,
        strict: Optional[Literal['on', 'off']] = None,
        preview: Optional[Union[Literal['on', 'off', 'head', 'tail'], str]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> ReRunState:
        """
        Re run a Bauplan project by its ID and return the state of the run. This is the equivalent of
        running through the CLI the ``bauplan rerun`` command.

        :param job_id: The Job ID of the previous run. This can be used to re-run a previous run, e.g., on a different branch.
        :param ref: The ref or branch name to read.
        :param namespace: The Namespace to run the job in. If not set, the job will be run in the default namespace.
        :param cache: Whether to enable or disable caching for the run.
        :param transaction: Whether to enable or disable transaction mode for the run.
        :param dry_run: Whether to enable or disable dry-run mode for the run; models are not materialized.
        :param strict: Whether to enable or disable strict schema validation.
        :param preview: Whether to enable or disable preview mode for the run.
        :param debug: Whether to enable or disable debug mode for the run.
        :param args: Additional arguments (optional).
        :param verbose: Whether to enable or disable verbose mode for the run.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The state of the run.
        """
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._run.rerun(
                job_id=job_id,
                ref=ref_name,
                namespace=namespace_name,
                cache=cache,
                transaction=transaction,
                dry_run=dry_run,
                strict=strict,
                preview=preview,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    # Query

    def query(
        self,
        query: str,
        ref: Optional[Union[str, Branch, Ref]] = None,
        max_rows: Optional[int] = None,
        cache: Optional[Literal['on', 'off']] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> pa.Table:
        """
        Execute a SQL query and return the results as a pyarrow.Table.
        Note that this function uses Arrow also internally, resulting
        in a fast data transfer.

        If you prefer to return the results as a pandas DataFrame, use
        the ``to_pandas`` function of pyarrow.Table.

        .. code-block:: python

            import bauplan

            client = bauplan.Client()

            # query the table and return result set as an arrow Table
            my_table = client.query(
                query='SELECT c1 FROM my_table',
                ref='my_ref_or_branch_name',
            )

            # efficiently cast the table to a pandas DataFrame
            df = my_table.to_pandas()

        :param query: The Bauplan query to execute.
        :param ref: The ref or branch name to read data from.
        :param max_rows: The maximum number of rows to return; default: ``None`` (no limit).
        :param cache: Whether to enable or disable caching for the query.
        :param connector: The connector type for the model (defaults to Bauplan). Allowed values are 'snowflake' and 'dremio'.
        :param connector_config_key: The key name if the SSM key is custom with the pattern bauplan/connectors/<connector_type>/<key>.
        :param connector_config_uri: Full SSM uri if completely custom path, e.g. ssm://us-west-2/123456789012/baubau/dremio.
        :param namespace: The Namespace to run the query in. If not set, the query will be run in the default namespace for your account.
        :param debug: Whether to enable or disable debug mode for the query.
        :param args: Additional arguments to pass to the query (default: None).
        :param verbose: Whether to enable or disable verbose mode for the query.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The query results as a ``pyarrow.Table``.
        """
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._query.query(
                query=query,
                ref=ref_name,
                max_rows=max_rows,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace_name,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def query_to_generator(
        self,
        query: str,
        ref: Optional[Union[str, Branch, Ref]] = None,
        max_rows: Optional[int] = None,
        cache: Optional[Literal['on', 'off']] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        debug: Optional[bool] = None,
        as_json: Optional[bool] = False,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Execute a SQL query and return the results as a generator, where each row is
        a Python dictionary.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # query the table and iterate through the results one row at a time
            res = client.query_to_generator(
                query='SELECT c1 FROM my_table',
                ref='my_ref_or_branch_name',
            )
            for row in res:
                # do logic

        :param query: The Bauplan query to execute.
        :param ref: The ref or branch name to read data from.
        :param max_rows: The maximum number of rows to return; default: ``None`` (no limit).
        :param cache: Whether to enable or disable caching for the query.
        :param connector: The connector type for the model (defaults to Bauplan). Allowed values are 'snowflake' and 'dremio'.
        :param connector_config_key: The key name if the SSM key is custom with the pattern bauplan/connectors/<connector_type>/<key>.
        :param connector_config_uri: Full SSM uri if completely custom path, e.g. ssm://us-west-2/123456789012/baubau/dremio.
        :param namespace: The Namespace to run the query in. If not set, the query will be run in the default namespace for your account.
        :param debug: Whether to enable or disable debug mode for the query.
        :param as_json: Whether to return the results as a JSON-compatible string (default: ``False``).
        :param args: Additional arguments to pass to the query (default: ``None``).
        :param verbose: Whether to enable or disable verbose mode for the query.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :yield: A dictionary representing a row of query results.
        """
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._query.query_to_generator(
                query=query,
                ref=ref_name,
                max_rows=max_rows,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace_name,
                debug=debug,
                as_json=as_json,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def query_to_parquet_file(
        self,
        path: Union[str, Path],
        query: str,
        ref: Optional[Union[str, Branch, Ref]] = None,
        max_rows: Optional[int] = None,
        cache: Optional[Literal['on', 'off']] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> Path:
        """
        Export the results of a SQL query to a file in Parquet format.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # query the table and iterate through the results one row at a time
            client.query_to_parquet_file(
                path='./my.parquet',
                query='SELECT c1 FROM my_table',
                ref='my_ref_or_branch_name',
            ):

        :param path: The name or path of the file parquet to write the results to.
        :param query: The Bauplan query to execute.
        :param ref: The ref or branch name to read data from.
        :param max_rows: The maximum number of rows to return; default: ``None`` (no limit).
        :param cache: Whether to enable or disable caching for the query.
        :param connector: The connector type for the model (defaults to Bauplan). Allowed values are 'snowflake' and 'dremio'.
        :param connector_config_key: The key name if the SSM key is custom with the pattern bauplan/connectors/<connector_type>/<key>.
        :param connector_config_uri: Full SSM uri if completely custom path, e.g. ssm://us-west-2/123456789012/baubau/dremio.
        :param namespace: The Namespace to run the query in. If not set, the query will be run in the default namespace for your account.
        :param debug: Whether to enable or disable debug mode for the query.
        :param args: Additional arguments to pass to the query (default: None).
        :param verbose: Whether to enable or disable verbose mode for the query.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The path of the file written.
        """
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._query.query_to_parquet_file(
                path=path,
                query=query,
                ref=ref_name,
                max_rows=max_rows,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace_name,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
                **kwargs,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def query_to_csv_file(
        self,
        path: Union[str, Path],
        query: str,
        ref: Optional[Union[str, Branch, Ref]] = None,
        max_rows: Optional[int] = None,
        cache: Optional[Literal['on', 'off']] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> Path:
        """
        Export the results of a SQL query to a file in CSV format.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # query the table and iterate through the results one row at a time
            client.query_to_csv_file(
                path='./my.csv',
                query='SELECT c1 FROM my_table',
                ref='my_ref_or_branch_name',
            ):

        :param path: The name or path of the file csv to write the results to.
        :param query: The Bauplan query to execute.
        :param ref: The ref or branch name to read data from.
        :param max_rows: The maximum number of rows to return; default: ``None`` (no limit).
        :param cache: Whether to enable or disable caching for the query.
        :param connector: The connector type for the model (defaults to Bauplan). Allowed values are 'snowflake' and 'dremio'.
        :param connector_config_key: The key name if the SSM key is custom with the pattern bauplan/connectors/<connector_type>/<key>.
        :param connector_config_uri: Full SSM uri if completely custom path, e.g. ssm://us-west-2/123456789012/baubau/dremio.
        :param namespace: The Namespace to run the query in. If not set, the query will be run in the default namespace for your account.
        :param debug: Whether to enable or disable debug mode for the query.
        :param args: Additional arguments to pass to the query (default: None).
        :param verbose: Whether to enable or disable verbose mode for the query.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The path of the file written.
        """
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._query.query_to_csv_file(
                path=path,
                query=query,
                ref=ref_name,
                max_rows=max_rows,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace_name,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
                **kwargs,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def query_to_json_file(
        self,
        path: Union[str, Path],
        query: str,
        file_format: Optional[Literal['json', 'jsonl']] = 'json',
        ref: Optional[Union[str, Branch, Ref]] = None,
        max_rows: Optional[int] = None,
        cache: Optional[Literal['on', 'off']] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> Path:
        """
        Export the results of a SQL query to a file in JSON format.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # query the table and iterate through the results one row at a time
            client.query_to_json_file(
                path='./my.json',
                query='SELECT c1 FROM my_table',
                ref='my_ref_or_branch_name',
            ):

        :param path: The name or path of the file json to write the results to.
        :param query: The Bauplan query to execute.
        :param file_format: The format to write the results in; default: ``json``. Allowed values are 'json' and 'jsonl'.
        :param ref: The ref or branch name to read data from.
        :param max_rows: The maximum number of rows to return; default: ``None`` (no limit).
        :param cache: Whether to enable or disable caching for the query.
        :param connector: The connector type for the model (defaults to Bauplan). Allowed values are 'snowflake' and 'dremio'.
        :param connector_config_key: The key name if the SSM key is custom with the pattern bauplan/connectors/<connector_type>/<key>.
        :param connector_config_uri: Full SSM uri if completely custom path, e.g. ssm://us-west-2/123456789012/baubau/dremio.
        :param namespace: The Namespace to run the query in. If not set, the query will be run in the default namespace for your account.
        :param debug: Whether to enable or disable debug mode for the query.
        :param args: Additional arguments to pass to the query (default: None).
        :param verbose: Whether to enable or disable verbose mode for the query.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The path of the file written.
        """
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._query.query_to_json_file(
                path=path,
                query=query,
                file_format=file_format,
                ref=ref_name,
                max_rows=max_rows,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace_name,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def create_table(
        self,
        table: Union[str, Table],
        search_uri: str,
        branch: Optional[Union[str, Branch]] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        partitioned_by: Optional[str] = None,
        replace: Optional[bool] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> Table:
        """
        Create a table from an S3 location.

        This operation will attempt to create a table based of schemas of N
        parquet files found by a given search uri.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            plan_state = client.create_table(
                table='my_table_name',
                search_uri='s3://path/to/my/files/*.parquet',
                ref='my_ref_or_branch_name',
            )
            if plan_state.error:
                plan_error_action(...)
            success_action(plan_state.plan)

        :param table: The table which will be created.
        :param search_uri: The location of the files to scan for schema.
        :param branch: The branch name in which to create the table in.
        :param namespace: Optional argument specifying the namespace. If not.
            specified, it will be inferred based on table location or the default.
            namespace.
        :param partitioned_by: Optional argument specifying the table partitioning.
        :param replace: Replace the table if it already exists.
        :param debug: Whether to enable or disable debug mode for the query.
        :param args: dict of arbitrary args to pass to the backend.
        :param verbose: Whether to enable or disable verbose mode.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :raises TableCreatePlanStatusError: if the table creation plan fails.
        :raises TableCreatePlanApplyStatusError: if the table creation plan apply fails.

        :return: The plan state.
        """
        table_create_plan = self.plan_table_creation(
            table=table,
            search_uri=search_uri,
            branch=branch,
            namespace=namespace,
            partitioned_by=partitioned_by,
            replace=replace,
            debug=debug,
            args=args,
            verbose=verbose,
            client_timeout=client_timeout,
        )
        _ = self.apply_table_creation_plan(
            plan=table_create_plan,
            debug=debug,
            args=args,
            verbose=verbose,
            client_timeout=client_timeout,
        )

        # The namespace has been resolved by the commander
        parts = table_create_plan.ctx.table_name.split('.')
        if len(parts) > 1:
            return Table(
                name=parts[-1],
                namespace='.'.join(parts[:-1]),
            )

        return Table(
            name=table_create_plan.ctx.table_name,
            namespace=table_create_plan.ctx.namespace,
        )

    def plan_table_creation(
        self,
        table: Union[str, Table],
        search_uri: str,
        branch: Optional[Union[str, Branch]] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        partitioned_by: Optional[str] = None,
        replace: Optional[bool] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> TableCreatePlanState:
        """
        Create a table import plan from an S3 location.

        This operation will attempt to create a table based of schemas of N
        parquet files found by a given search uri. A YAML file containing the
        schema and plan is returns and if there are no conflicts, it is
        automatically applied.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            plan_state = client.plan_table_creation(
                table='my_table_name',
                search_uri='s3://path/to/my/files/*.parquet',
                ref='my_ref_or_branch_name',
            )
            if plan_state.error:
                plan_error_action(...)
            success_action(plan_state.plan)

        :param table: The table which will be created.
        :param search_uri: The location of the files to scan for schema.
        :param branch: The branch name in which to create the table in.
        :param namespace: Optional argument specifying the namespace. If not.
            specified, it will be inferred based on table location or the default.
            namespace.
        :param partitioned_by: Optional argument specifying the table partitioning.
        :param replace: Replace the table if it already exists.
        :param debug: Whether to enable or disable debug mode.
        :param args: dict of arbitrary args to pass to the backend.
        :param verbose: Whether to enable or disable verbose mode.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :raises TableCreatePlanStatusError: if the table creation plan fails.

        :return: The plan state.
        """
        branch_name = _get_optional_branch_name('branch', branch)
        table_name = _get_table_name('table', table)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._table_create.plan(
                table_name=table_name,
                search_uri=search_uri,
                branch_name=branch_name,
                namespace=namespace_name,
                partitioned_by=partitioned_by,
                replace=replace,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def apply_table_creation_plan(
        self,
        plan: Union[Dict, TableCreatePlanState],
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> TableCreatePlanApplyState:
        """
        Apply a plan for creating a table. It is done automaticaly during th
        table plan creation if no schema conflicts exist. Otherwise, if schema
        conflicts exist, then this function is used to apply them after the
        schema conflicts are resolved. Most common schema conflict is a two
        parquet files with the same column name but different datatype

        :param plan: The plan to apply.
        :param debug: Whether to enable or disable debug mode for the query.
        :param args: dict of arbitrary args to pass to the backend.
        :param verbose: Whether to enable or disable verbose mode.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :raises TableCreatePlanApplyStatusError: if the table creation plan apply fails.

        :return The plan state.
        """
        try:
            return self._table_create.apply(
                plan=plan,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    def import_data(
        self,
        table: Union[str, Table],
        search_uri: str,
        branch: Optional[Union[str, Branch]] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        continue_on_error: bool = False,
        import_duplicate_files: bool = False,
        best_effort: bool = False,
        # transformation_query: Optional[str] = None,
        preview: Optional[Union[Literal['on', 'off', 'head', 'tail'], str]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> TableDataImportState:
        """
        Imports data into an already existing table.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            plan_state = client.import_data(
                table='my_table_name',
                search_uri='s3://path/to/my/files/*.parquet',
                branch='my_branch_name',
            )
            if plan_state.error:
                plan_error_action(...)
            success_action(plan_state.plan)

        :param table: Previously created table in into which data will be imported.
        :param search_uri: Uri which to scan for files to import.
        :param branch: Branch in which to import the table.
        :param namespace: Namespace of the table. If not specified, namespace will be infered from table name or default settings.
        :param continue_on_error: Do not fail the import even if 1 data import fails.
        :param import_duplicate_files: Ignore prevention of importing s3 files that were already imported.
        :param best_effort: Don't fail if schema of table does not match.
        :param transformation_query: Optional duckdb compliant query applied on each parquet file. Use `original_table` as the table in the query.
        :param preview: Whether to enable or disable preview mode for the import.
        :param debug: Whether to enable or disable debug mode for the import.
        :param args: dict of arbitrary args to pass to the backend.
        :param verbose: Whether to enable or disable verbose mode.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The plan state.
        """
        table_name = _get_table_name('table', table)
        branch_name = _get_optional_branch_name('branch', branch)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._table_import.data_import(
                table_name=table_name,
                search_uri=search_uri,
                branch_name=branch_name,
                namespace=namespace_name,
                continue_on_error=continue_on_error,
                import_duplicate_files=import_duplicate_files,
                best_effort=best_effort,
                transformation_query=None,
                preview=preview,
                debug=debug,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    # Scan

    def scan(
        self,
        table: Union[str, Table],
        ref: Optional[Union[str, Branch, Ref]] = None,
        columns: Optional[List[str]] = None,
        filters: Optional[str] = None,
        limit: Optional[int] = None,
        cache: Optional[Literal['on', 'off']] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[Union[str, Namespace]] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        client_timeout: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> pa.Table:
        """
        Execute a table scan (with optional filters) and return the results as an arrow Table.

        Note that this function uses SQLGlot to compose a safe SQL query,
        and then internally defer to the query_to_arrow function for the actual
        scan.

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # run a table scan over the data lake
            # filters are passed as a string
            my_table = client.scan(
                table='my_table_name',
                ref='my_ref_or_branch_name',
                columns=['c1'],
                filters='c2 > 10',
            )

        :param table: The table to scan.
        :param ref: The ref or branch name to read data from.
        :param columns: The columns to return (default: ``None``).
        :param filters: The filters to apply (default: ``None``).
        :param limit: The maximum number of rows to return (default: ``None``).
        :param cache: Whether to enable or disable caching for the query.
        :param connector: The connector type for the model (defaults to Bauplan). Allowed values are 'snowflake' and 'dremio'.
        :param connector_config_key: The key name if the SSM key is custom with the pattern bauplan/connectors/<connector_type>/<key>.
        :param connector_config_uri: Full SSM uri if completely custom path, e.g. ssm://us-west-2/123456789012/baubau/dremio.
        :param namespace: The Namespace to run the scan in. If not set, the scan will be run in the default namespace for your account.
        :param debug: Whether to enable or disable debug mode for the query.
        :param args: dict of arbitrary args to pass to the backend.
        :param client_timeout: seconds to timeout; this also cancels the remote job execution.

        :return: The scan results as a ``pyarrow.Table``.
        """
        table_name = _get_table_name('table', table)
        ref_name = _get_optional_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        try:
            return self._query.scan(
                table_name=table_name,
                ref=ref_name,
                columns=columns,
                filters=filters,
                limit=limit,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace_name,
                debug=debug,
                args=args,
                client_timeout=client_timeout,
                **kwargs,
            )
        except grpc._channel._InactiveRpcError as e:
            if hasattr(e, 'details'):
                raise exceptions.JobError(e.details()) from e
            raise exceptions.JobError(e) from e

    # Catalog

    def get_branches(
        self,
        name: Optional[str] = None,
        user: Optional[str] = None,
        limit: Optional[int] = None,
        itersize: Optional[int] = None,
    ) -> Generator[Branch, None, None]:
        """
        Get the available data branches in the Bauplan catalog.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            for branch in client.get_branches():
                print(branch.name, branch.hash)

        :param name: Filter the branches by name.
        :param user: Filter the branches by user.
        :param itersize: int 1-500.
        :param limit: int > 0.

        :yield: A Branch object.
        """
        path = _get_quoted_url('v0', 'branches')
        params = {}
        if name and name.strip():
            params['name'] = name.strip()
        if user and user.strip():
            params['user'] = user.strip()
        for record in self._paginate_api(path, limit=limit, itersize=itersize, params=params):
            yield Branch.model_validate(record)

    def get_branch(
        self,
        branch: Union[str, Branch],
    ) -> Branch:
        """
        Get the branch.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # retrieve only the tables as tuples of (name, kind)
            branch = client.get_branch('my_branch_name')
            print(branch.hash)

        :param branch: The name of the branch to retrieve.

        :return: A Branch object.
        """
        branch_name = _get_branch_name('branch', branch)
        path = _get_quoted_url('v0', 'refs', branch_name)
        out: APIResponse = self._make_catalog_api_call('get', path)
        return Branch.model_validate(out.data)

    def has_branch(
        self,
        branch: Union[str, Branch],
    ) -> bool:
        """
        Check if a branch exists.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.has_branch('my_branch_name')

        :param branch: The name of the branch to check.

        :return: A boolean for if the branch exists.
        """
        try:
            self.get_branch(branch=branch)
            return True
        except exceptions.ResourceNotFoundError:
            return False

    def create_branch(
        self,
        branch: Union[str, Branch],
        from_ref: Union[str, Branch, Ref],
    ) -> Branch:
        """
        Create a new branch at a given ref.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.create_branch(
                branch='my_branch_name',
                from_ref='my_ref_or_branch_name',
            )

        :param branch: The name of the new branch.
        :param from_ref: The name of the base branch; either a branch like "main" or ref like "main@[sha]".

        :return: The created branch object.
        """
        branch_name = _get_branch_name('branch', branch)
        from_ref_name = _get_ref_name('from_ref', from_ref)
        path = _get_quoted_url('v0', 'branches')
        body = {'branch_name': branch_name, 'from_ref': from_ref_name}
        out: APIResponse = self._make_catalog_api_call('post', path, body=body)
        return Branch.model_validate(out.data)

    def merge_branch(
        self,
        source_ref: Union[str, Branch, Ref],
        into_branch: Union[str, Branch],
    ) -> bool:
        """
        Merge one branch into another.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert merge_branch(
                source_ref='my_ref_or_branch_name',
                into_branch='main',
            )

        :param source_ref: The name of the merge source; either a branch like "main" or ref like "main@[sha]".
        :param into_branch: The name of the merge target.

        :return: a boolean for whether the merge worked.
        """
        into_branch = _get_branch_name('into_branch', into_branch)
        source_ref_name = _get_ref_name('source_ref', source_ref)
        path = _get_quoted_url('v0', 'refs', source_ref_name, 'merge', into_branch)
        self._make_catalog_api_call('post', path)
        return True

    def delete_branch(
        self,
        branch: Union[str, Branch],
    ) -> bool:
        """
        Delete a branch.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.delete_branch('my_branch_name')

        :param branch: The name of the branch to delete.

        :return: A boolean for if the branch was deleted.
        """
        branch_name = _get_branch_name('branch', branch)
        path = _get_quoted_url('v0', 'branches', branch_name)
        self._make_catalog_api_call('delete', path)
        return True

    def get_namespaces(
        self,
        ref: Union[str, Branch, Ref],
        filter_by_name: Optional[str] = None,
        itersize: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Generator[Namespace, None, None]:
        """
        Get the available data namespaces in the Bauplan catalog branch.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            for namespace in client.get_namespaces('my_namespace_name'):
                print(namespace.name)

        :param ref: The ref or branch to retrieve the namespaces from.
        :param filter_by_name: Filter the namespaces by name.
        :param itersize: int 1-500.
        :param limit: int > 0.

        :yield: A Namespace object.
        """
        ref_name = _get_ref_name('ref', ref)
        path = _get_quoted_url('v0', 'refs', ref_name, 'namespaces')
        params = {}
        if filter_by_name and filter_by_name.strip():
            params['namespace'] = filter_by_name.strip()
        for record in self._paginate_api(path, limit=limit, itersize=itersize, params=params):
            yield Namespace.model_validate(record)

    def get_namespace(
        self,
        namespace: Union[str, Namespace],
        ref: Union[str, Branch, Ref],
    ) -> Namespace:
        """
        Get a namespace.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            namespace =  client.get_namespace(
                namespace='my_namespace_name',
                ref='my_ref_or_branch_name',
            )

        :param namespace: The name of the namespace to get.
        :param ref: The ref or branch to check the namespace on.

        :return: A Namespace object.
        """
        namespace_name = _get_namespace_name('namespace', namespace)
        list(self.get_tables(ref=ref, namespace=namespace, limit=1))
        return Namespace(name=namespace_name)

    def create_namespace(
        self,
        namespace: Union[str, Namespace],
        branch: Union[str, Branch],
    ) -> Namespace:
        """
        Create a new namespace at a given branch.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.create_namespace(
                namespace='my_namespace_name'
                branch='my_branch_name',
            )

        :param namespace: The name of the namespace.
        :param branch: The name of the branch to create the namespace on.

        :return: The created namespace.
        """
        namespace_name = _get_namespace_name('namespace', namespace)
        branch_name = _get_branch_name('branch', branch)
        path = _get_quoted_url('v0', 'branches', branch_name, 'namespaces')
        body = {'namespace_name': namespace_name}
        out: APIResponse = self._make_catalog_api_call('post', path, body=body)
        return Namespace.model_validate(out.data)

    def delete_namespace(
        self,
        namespace: Union[str, Namespace],
        branch: Union[str, Branch],
    ) -> bool:
        """
        Delete a namespace.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.delete_namespace(
                namespace='my_namespace_name',
                branch='my_branch_name',
            )

        :param namespace: The name of the namespace to delete.
        :param form_branch: The name of the branch to delete the namespace from.

        :return: A boolean for if the namespace was deleted.
        """
        namespace_name = _get_namespace_name('namespace', namespace)
        branch_name = _get_branch_name('branch', branch)
        path = _get_quoted_url('v0', 'branches', branch_name, 'namespaces', namespace_name)
        self._make_catalog_api_call('delete', path)
        return True

    def has_namespace(
        self,
        namespace: Union[str, Namespace],
        ref: Union[str, Branch, Ref],
    ) -> bool:
        """
        Check if a namespace exists.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.has_namespace(
                namespace='my_namespace_name',
                ref='my_ref_or_branch_name',
            )

        :param namespace: The name of the namespace to check.
        :param ref: The ref or branch to check the namespace on.

        :return: A boolean for if the namespace exists.
        """
        try:
            self.get_namespace(namespace=namespace, ref=ref)
            return True
        except exceptions.ResourceNotFoundError:
            return False

    def get_tables(
        self,
        ref: Union[str, Branch, Ref],
        namespace: Optional[Union[str, Namespace]] = None,
        limit: Optional[int] = None,
        itersize: Optional[int] = None,
    ) -> Generator[Table, None, None]:
        """
        Get the tables and views in the target branch.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # retrieve only the tables as tuples of (name, kind)
            for table in client.get_tables('my_ref_or_branch_name'):
                print(table.name, table.kind)

        :param ref: The ref or branch to get the tables from.
        :param namespace: The namespace to get the tables from.
        :param limit: int > 0.
        :param itersize: int 1-500.

        :yield: A Table object.
        """
        ref_name = _get_ref_name('ref', ref)
        namespace_name = _get_optional_namespace_name('namespace', namespace)
        path = _get_quoted_url('v0', 'refs', ref_name, 'tables')
        params = {}
        if namespace_name:
            params['namespace'] = namespace_name
        for record in self._paginate_api(path, limit=limit, itersize=itersize, params=params):
            yield Table.model_validate(record)

    def get_table(
        self,
        table: Union[str, Table],
        ref: Union[str, Ref, Branch],
        include_raw: bool = False,
    ) -> TableWithMetadata:
        """
        Get the table data and metadata for a table in the target branch.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            # get the fields and metadata for a table
            table = client.get_table(
                table='my_table_name',
                ref='my_ref_or_branch_name',
            )

            # loop through the fields and print their name, required, and type
            for c in table.fields:
                print(c.name, c.required, c.type)

            # show the number of records in the table
            print(table.records)

        :param ref: The ref or branch to get the table from.
        :param table: The table to retrieve.
        :param include_raw: Whether or not to include the raw metadata.json object as a nested dict.

        :return: a TableWithMetadata object, optionally including the raw metadata.json object.
        """
        ref_name = _get_ref_name('ref', ref)
        table_name = _get_table_name('table', table)
        path = _get_quoted_url('v0', 'refs', ref_name, 'tables', table_name)
        params = {'raw': 1 if include_raw else 0}
        out: APIResponse = self._make_catalog_api_call('get', path, params=params)

        return TableWithMetadata.model_validate(out.data)

    def has_table(
        self,
        table: Union[str, Table],
        ref: Union[str, Ref, Branch],
    ) -> bool:
        """
        Check if a table exists.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.has_table(
                table='my_table_name',
                ref='my_ref_or_branch_name',
            )

        :param ref: The ref or branch to get the table from.
        :param table: The table to retrieve.

        :return: A boolean for if the table exists.
        """
        try:
            self.get_table(table=table, ref=ref)
            return True
        except exceptions.ResourceNotFoundError:
            return False

    def delete_table(
        self,
        table: Union[str, Table],
        branch: Union[str, Branch],
    ) -> bool:
        """
        Drop a table.

        Upon failure, raises ``bauplan.exceptions.BauplanError``

        .. code-block:: python

            import bauplan
            client = bauplan.Client()

            assert client.delete_table(
                table='my_table_name',
                branch='my_branch_name',
            )

        :param table: The table to delete.
        :param branch: The branch on which the table is stored.

        :return: A boolean for if the table was deleted.
        """
        branch_name = _get_branch_name('branch', branch)
        table_name = _get_table_name('table', table)
        path = _get_quoted_url('v0', 'branches', branch_name, 'tables', table_name)
        self._make_catalog_api_call('delete', path)
        return True

    def info(
        self,
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> InfoState:
        """
        Fetch organization & account information.
        """
        return self._info.info(
            debug=debug,
            verbose=verbose,
            client_timeout=client_timeout,
            **kwargs,
        )

    # Helpers

    @_lifecycle
    def _make_catalog_api_call(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        pagination_token: Optional[str] = None,
        # shared
        client_timeout: Optional[Union[int, float]] = None,
        lifecycle_handler: Optional[_JobLifeCycleHandler] = None,
    ) -> APIResponse:
        """
        Helper to make a request to the API.

        :meta private:
        """
        url = self.profile.catalog_endpoint + path
        headers = {Constants.METADATA_PYPI_VERSION_KEY: BAUPLAN_VERSION}
        if self.profile.user_session_token:
            headers = {Constants.METADATA_USER_SESSION_TOKEN: self.profile.user_session_token}
        elif self.profile.api_key:
            headers = {Constants.METADATA_API_KEY: self.profile.api_key}
        if self.profile.feature_flags:
            headers[Constants.METADATA_FEATURE_FLAGS] = json.dumps(self.profile.feature_flags)
        params = params or {}
        if pagination_token and pagination_token.strip():
            params['pagination_token'] = pagination_token.strip()
        if body:
            if not isinstance(body, dict):
                raise exceptions.BauplanError(
                    f'SDK INTERNAL ERROR: API request body must be dict, not {type(body)}'
                )
            res = requests.request(
                method,
                url,
                headers=headers,
                timeout=Constants.DEFAULT_API_CALL_TIMEOUT_SECONDS,
                params=params or {},
                json=body,
            )
        else:
            res = requests.request(
                method,
                url,
                headers=headers,
                timeout=Constants.DEFAULT_API_CALL_TIMEOUT_SECONDS,
                params=params or {},
            )
        out = APIResponse.model_validate(res.json())
        if out.metadata.error or res.status_code != 200:
            if res.status_code == 400:
                raise exceptions.InvalidDataError(out.metadata.error)
            if res.status_code == 401:
                raise exceptions.UnauthorizedError(out.metadata.error)
            if res.status_code == 403:
                raise exceptions.AccessDeniedError(out.metadata.error)
            if res.status_code == 404:
                if out.metadata.error == 'path method not found':
                    raise exceptions.ApiMethodError(out.metadata.error)
                raise exceptions.ResourceNotFoundError(out.metadata.error)
            if res.status_code == 409:
                raise exceptions.UpdateConflictError(out.metadata.error)
            if res.status_code == 429:
                raise exceptions.TooManyRequestsError(out.metadata.error)
            raise exceptions.BauplanError(f'unhandled API exception {res.status_code}: {out.metadata.error}')
        return out

    def _paginate_api(
        self,
        path: str,
        limit: Optional[int] = None,
        itersize: Optional[int] = None,
        params: Optional[Dict] = None,
    ) -> Union[Any, Generator[Any, None, None]]:
        """
        Helper to paginate through a Bauplan API or only fetch a limited number of records.

        Works if the route returns lists of records and accepts a pagination token.

        If the route doesn't return a list of records, this just returns the record returned.

        :meta private:
        """
        if itersize is not None:
            if not isinstance(itersize, int) or itersize > 500 or itersize < 1:
                raise ValueError('itersize must be an int between 1 and 500 inclusive')
        if limit is not None:
            if not isinstance(limit, int) or limit < 1:
                raise ValueError('limit must be a positive integer')

        params = {**(params or {}), 'max_records': itersize or 500}
        pagination_token = None
        n = 0
        stop = False
        while not stop:
            if pagination_token:
                params['pagination_token'] = pagination_token
            out: APIResponse = self._make_catalog_api_call(
                method='get',
                path=path,
                pagination_token=pagination_token,
                params=params,
            )
            if not isinstance(out.data, list):
                return out.data  # noqa: B901
            for x in out.data:
                yield x
                n += 1
                if limit and n >= limit:
                    stop = True
                    break
            if out.metadata.pagination_token:
                pagination_token = out.metadata.pagination_token
            else:
                break
