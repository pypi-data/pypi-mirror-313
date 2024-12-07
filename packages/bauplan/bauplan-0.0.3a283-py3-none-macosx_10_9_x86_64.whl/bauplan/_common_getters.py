from __future__ import annotations

import datetime
import re
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

from ._bpln_proto.commander.service.v2.common_pb2 import JobRequestOptionalBool
from .schema import Branch, Namespace, Ref, Table


def _get_quoted_url(*args: str) -> str:
    """
    Helper to build a URL from parts, safely handling slashes.

    :meta private:
    """
    return '/' + '/'.join([urllib.parse.quote(x, safe='') for x in args])


def _get_parameters(
    name: str,
    parameters: Optional[Dict[str, Optional[Union[str, int, float, bool]]]] = None,
) -> Dict[str, Optional[Union[str, int, float, bool]]]:
    """
    Default branch is the local active branch, but can be overridden by passing a ref.
    It's optional because the default ref is managed by the service.

    :meta private:
    """
    if parameters is not None:
        if not isinstance(parameters, dict):
            raise ValueError(f'{name} must be a dict or None')
    return parameters or {}


def _get_feature_flags(
    name: str,
    flags: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    flags = _get_parameters(name, flags)
    ff_normalized: Dict[str, str] = {}
    for key, value in flags.items():
        if isinstance(value, bool):
            ff_normalized[key] = 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            ff_normalized[key] = str(value)
        elif not isinstance(key, str):
            raise ValueError(f'{name} keys must be str | int | float')
        elif not isinstance(value, str):
            raise ValueError(f'{name} values must be str | int | float')
        else:
            ff_normalized[key] = value
    return ff_normalized


def _get_string(name: str, val: Optional[str] = None) -> str:
    if val is None or not isinstance(val, str) or val.strip() == '':
        raise ValueError(f'{name} must be a non-empty string')
    return val


def _get_optional_string(
    name: str,
    value: Optional[str],
    default_value: Optional[str] = None,
) -> Optional[str]:
    value = default_value if value is None else value
    if value is not None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{name} must be a non-empty string or None')
    return value


def _get_optional_ref(
    name: str,
    ref: Optional[str],
    default_ref: Optional[str] = None,
) -> Optional[str]:
    """
    Default branch is the local active branch, but can be overridden by passing a ref.
    It's optional because the default ref is managed by the service.

    :meta private:
    """
    ref = default_ref if ref is None else ref
    if ref is not None:
        if not isinstance(ref, str) or ref.strip() == '':
            raise ValueError(f'{name} must be a non-empty string or None')
    return ref


def _get_ref_name(
    name: str,
    ref: Optional[Union[str, Branch, Ref]],
    default_name: Optional[str] = None,
) -> str:
    """
    Get the ref name from a ref or ref-like object.

    :meta private:
    """
    ref_name = _get_optional_ref_name(name, ref, default_name)
    if ref_name is None:
        raise ValueError(f'{name} must be a non-empty string or a valid Branch object')
    return ref_name


def _get_optional_ref_name(
    name: str,
    ref: Optional[Union[str, Branch, Ref]],
    default_name: Optional[str] = None,
) -> Optional[str]:
    """
    Get the ref name from a ref or ref-like object.

    :meta private:
    """
    if ref is None:
        return default_name
    if isinstance(ref, str) and ref.strip() != '':
        return ref
    if isinstance(ref, (Branch, Ref)) and ref.name.strip() != '':
        return ref.name
    raise ValueError(f'{name} must be a non-empty string or a valid Branch object')


def _get_bool(name: str, val: Optional[bool]) -> bool:
    if val is None or not isinstance(val, bool):
        raise ValueError(f'{name} must be a bool')
    return val


def _get_optional_bool(
    name: str,
    value: Optional[bool] = None,
    default_value: Optional[bool] = None,
) -> Optional[bool]:
    value = default_value if value is None else value
    if value is not None:
        if not isinstance(value, bool):
            raise ValueError(f'{name} must be a bool or None')
    return value


def _get_optional_on_off_flag(
    name: str,
    val: Optional[Union[bool, str]],
    default_flag: Optional[Union[bool, str]] = None,
) -> Optional[str]:
    val = default_flag if val is None else val
    if val is not None:
        if isinstance(val, str) and val.strip() != '':
            return val.strip()
        raise ValueError(f'{name} must be a bool or a non-empty string or None')
    return None


def _get_pb2_optional_bool(
    name: str,
    value: Optional[bool],
    default_value: Optional[bool] = None,
) -> Tuple[Optional[bool], JobRequestOptionalBool]:
    value = _get_optional_bool(name, value, default_value)
    if value is True:
        return value, JobRequestOptionalBool.JOB_REQUEST_OPTIONAL_BOOL_TRUE
    if value is False:
        return value, JobRequestOptionalBool.JOB_REQUEST_OPTIONAL_BOOL_FALSE
    return value, JobRequestOptionalBool.JOB_REQUEST_OPTIONAL_BOOL_UNSPECIFIED


def _get_optional_namespace(
    name: str,
    namespace: Optional[str],
    default_namespace: Optional[str] = None,
) -> Optional[str]:
    """
    Default namespace is read from the local config, but can be overridden by the user.
    It's optional because the default namespace is managed by the service.

    :meta private:
    """
    namespace = default_namespace if namespace is None else namespace
    if namespace is not None:
        if not isinstance(namespace, str) or namespace.strip() == '':
            raise ValueError(f'{name} must be a non-empty string or None')
    return namespace


def _get_namespace_name(
    name: str,
    namespace: Optional[Union[str, Namespace]],
    default_name: Optional[str] = None,
) -> str:
    """
    Get the namespace name from a namespace or namespace-like object.

    :meta private:
    """
    namespace_name = _get_optional_namespace_name(name, namespace, default_name)
    if namespace_name is None:
        raise ValueError(f'{name} must be a non-empty string or a valid Namespace object')
    return namespace_name


def _get_optional_namespace_name(
    name: str,
    namespace: Optional[Union[str, Namespace]],
    default_name: Optional[str] = None,
) -> Optional[str]:
    """
    Get the namespace name from a namespace or namespace-like object.

    :meta private:
    """
    if namespace is None:
        return default_name
    if isinstance(namespace, str) and namespace.strip() != '':
        return namespace
    if isinstance(namespace, Namespace) and namespace.name.strip() != '':
        return namespace.name
    raise ValueError(f'{name} must be a non-empty string or a valid Namespace object')


def _get_table_name(
    name: str,
    table: Optional[Union[str, Table]],
) -> str:
    """
    Get the table name from a table or table-like object.

    :meta private:
    """
    table_name = _get_optional_table_name(name, table)
    if table_name is None:
        raise ValueError(f'{name} must be a non-empty string or a valid Table object')
    return table_name


def _get_optional_table_name(
    name: str,
    table: Optional[Union[str, Table]],
) -> Optional[str]:
    """
    Get the table name from a table or table-like object.

    :meta private:
    """
    if table is None:
        return None
    if isinstance(table, str) and table.strip() != '':
        return table
    if isinstance(table, Table) and table.name.strip() != '':
        return table.fqn
    raise ValueError(f'{name} must be a non-empty string or a valid Table object')


def _get_branch_name(
    name: str,
    branch: Optional[Union[str, Branch]],
    default_name: Optional[str] = None,
) -> str:
    """
    Get the branch name from a branch or branch-like object.

    :meta private:
    """
    branch_name = _get_optional_branch_name(name, branch, default_name)
    if branch_name is None:
        raise ValueError(f'{name} must be a non-empty string or a valid Branch object')
    return branch_name


def _get_optional_branch_name(
    name: str,
    branch: Optional[Union[str, Branch]],
    default_name: Optional[str] = None,
) -> Optional[str]:
    """
    Get the branch name from a branch or branch-like object.

    :meta private:
    """
    if branch is None:
        branch = default_name
    if branch is None:
        return None
    if isinstance(branch, str) and branch.strip() != '':
        if '@' in branch:
            raise ValueError(f'{name} cannot contain references (@), provide branch name only')
        return branch
    if isinstance(branch, (Ref, Branch)) and branch.name.strip() != '':
        if '@' in branch.name:
            raise ValueError(f'{name} cannot contain references (@), provide branch name only')
        return branch.name
    raise ValueError(f'{name} must be a non-empty string or a valid Branch object')


def _get_args(
    name: str,
    args: Optional[Dict[str, str]],
    default_args: Optional[Dict[str, str]],
) -> Dict[str, str]:
    """
    Validate and return the args dict.

    :meta private:
    """
    if args is not None:
        if not isinstance(args, dict):
            raise ValueError(f'{name} must be a dict or None')
    return {
        **(default_args or {}),
        **(args or {}),
    }


def _ensure_parent_dir_exists(name: str, path: Union[str, Path]) -> Path:
    abs_path = Path(path).expanduser().resolve()
    parent_dir = abs_path.parent
    if not parent_dir.exists():
        raise FileNotFoundError(f'{name} is an invalid path, directory {parent_dir} does not exist')
    return abs_path


def _get_log_ts_str(val: int) -> str:
    """
    Output ISO timestamp to the decisecond from a nanosecond integer timestamp input.

    :meta private:
    """
    return str(datetime.datetime.fromtimestamp(round(val / 1000000000, 2)))[:21]


def _get_optional_endpoint(
    name: str,
    endpoint: Optional[str],
) -> Optional[str]:
    if endpoint is None:
        return None
    if not isinstance(endpoint, str) or not endpoint.strip():
        raise ValueError(f'{name} must be a valid string or None')
    endpoint = endpoint.strip()
    proto_match = re.match(r'^([^:]+)://(.*)$', endpoint.lower())
    if not proto_match:
        endpoint = f'https://{endpoint}'
    else:
        if proto_match.group(1) not in ('http', 'https'):
            raise ValueError(f'{name} must be a valid URL: invalid protocol')
        if not proto_match.group(2):
            ValueError(f'{name} must be a valid URL: missing hostname')
    # removing all trailing slashes
    return re.sub(r'/*$', '', endpoint)
