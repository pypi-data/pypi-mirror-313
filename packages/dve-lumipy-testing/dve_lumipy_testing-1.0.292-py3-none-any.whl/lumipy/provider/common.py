import re
import subprocess
from importlib.util import find_spec
from pathlib import Path
from shutil import which
from subprocess import CalledProcessError
from typing import Union

import numpy as np
import pandas as pd
from pandas import CategoricalDtype, Series
from semver import Version

from lumipy.common import indent_str
from lumipy.lumiflex._metadata.dtype import DType
from lumipy.provider.max_version import max_version_str


def infer_datatype(col: Series) -> DType:
    """Map the type of pandas Series to its corresponding SQL column type.

    Args:
        col (Series): the input series to infer the type of.

    Returns:
        DType: the SQL column type.
    """
    pd_dtype = col.dtype

    if pd_dtype == int:
        return DType.Int
    elif pd_dtype == float:
        return DType.Double
    elif pd_dtype == bool:
        return DType.Boolean
    elif isinstance(pd_dtype, CategoricalDtype):
        return DType.Text
    elif isinstance(pd_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        return DType.DateTime
    elif np.issubdtype(pd_dtype, np.datetime64):
        raise ValueError(
            f"The pandas DataFrame column '{col.name}' used to build the provider was not tz-aware. "
            f"Datetime values in pandas providers must be tz-aware.\n"
            "  Consider using the following (e.g. for the UTC timezone)\n"
            "    df['column'] = df['column'].dt.tz_localize(tz='utc')\n"
            "  to convert an existing DataFrame datetime column."
        )
    else:
        return DType.Text


def df_summary_str(d):
    mem_use = pd.DataFrame.memory_usage(d, deep=True)
    max_col_len = max(len(k) for k in mem_use.keys())
    divider = '―' * (max_col_len + 11)

    def format_size(x):

        units = [['TB😱', 1e12], ['GB', 1e9], ['MB', 1e6], ['KB', 1e3], ['B ', 1e0]]

        for upper, lower in zip(units[:-1], units[1:]):
            if upper[1] > x >= lower[1]:
                vstr = f'{x / lower[1]:6.1f}'
                return f'{vstr:6} {lower[0]}'

    strs = [divider]
    for k, v in mem_use.items():
        strs.append(f'{k:{max_col_len}}  {format_size(v)}')

    strs.append(divider)
    strs.append(f'{"Total":{max_col_len}}  {format_size(mem_use.sum())}')
    strs.append(divider)

    table_str = '\n'.join(map(lambda x: f'| {x} |', strs))

    return '\n'.join([
        '\n',
        'DataFrame Stats',
        f'    Number of rows: {d.shape[0]}',
        f'    Number of cols: {d.shape[1]}',
        '    Memory Usage:',
        f'{indent_str(table_str, 6)}',
        '',
    ])


def clean_colname(c_str):
    return str(c_str).replace('.', '_').replace("'", "").strip().strip('_')


def available(*args):
    return all(find_spec(name) is not None for name in args)


min_version = Version.parse('1.16.226')
max_version = Version.parse(max_version_str)


def get_dll_path(sdk_version) -> Path:
    return Path.home() / '.lumipy' / 'python_providers' / sdk_version.replace('.', '_')


def get_certs_path(domain) -> Path:
    return Path.home() / '.lumipy' / 'certs' / domain


def get_latest_local_python_provider_semver() -> Union[None, str]:
    lm_path = Path.home() / '.lumipy' / 'python_providers'
    folders = [f.parts[-1].replace('_', '.') for f in lm_path.glob('*_*_*')]
    sem_vers = sorted([Version.parse(f) for f in folders if Version.is_valid(f)])
    sem_vers = [sv for sv in sem_vers if min_version <= sv <= max_version]
    if len(sem_vers) == 0:
        return None
    return str(sem_vers[-1])


def semver_has_dll(semver) -> bool:
    path = Path.home() / '.lumipy' / 'python_providers' / semver.replace('.', '_') / 'tools' / 'net6.0' / 'any' / 'Finbourne.Honeycomb.Host.dll'
    return path.exists()


def expression_to_table_spec(meta, content):
    _meta = [{'name': a.args[0], 'type': a.args[1]} for a in meta.args]
    _content = content.args[0]
    return _meta, _content


def strtobool(val) -> int:
    val = val.lower()

    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


def find_dotnet_sdks():

    semver_regex_dotnet_6 = r'(6\.\d+\.\d+)'
    instruction = "Please install .NET 6.0."

    if which('dotnet') is None:
        raise ValueError(f".NET runtime not found. {instruction}]")

    try:
        result = subprocess.run(["dotnet", "--list-sdks"], capture_output=True, text=True, check=True)
    except CalledProcessError:
        raise ValueError(f"Error when trying to list .NET SDKs. {instruction}")

    semvers = re.findall(semver_regex_dotnet_6, result.stdout)
    if len(semvers) == 0:
        raise ValueError(f"You must install the .NET 6 SDK (newer versions are not yet supported). {instruction}")
