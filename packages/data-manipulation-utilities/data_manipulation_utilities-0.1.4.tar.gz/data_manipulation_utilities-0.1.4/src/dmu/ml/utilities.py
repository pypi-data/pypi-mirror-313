'''
Module containing utility functions for ML tools
'''

import hashlib
from typing import Union

import numpy
import pandas as pnd

from dmu.logging.log_store import LogStore

log = LogStore.add_logger('dmu:ml:utilities')
# ---------------------------------------------
# Patch dataframe with features
# ---------------------------------------------
def patch_and_tag(df : pnd.DataFrame, value : float = 0) -> pnd.DataFrame:
    '''
    Takes panda dataframe, replaces NaNs with value introduced, by default 0
    Returns array of indices where the replacement happened
    '''
    l_nan = df.index[df.isna().any(axis=1)].tolist()
    nnan  = len(l_nan)
    if nnan == 0:
        log.debug('No NaNs found')
        return df

    log.warning(f'Found {nnan} NaNs, patching them with {value}')

    df_pa = df.fillna(value)

    df_pa.attrs['patched_indices'] = numpy.array(l_nan)

    return df_pa
# ---------------------------------------------
# Cleanup of dataframe with features
# ---------------------------------------------
def cleanup(df : pnd.DataFrame) -> pnd.DataFrame:
    '''
    Takes pandas dataframe with features for classification
    Removes repeated entries and entries with nans
    Returns dataframe
    '''
    df = _remove_repeated(df)
    df = _remove_nans(df)

    return df
# ---------------------------------------------
def _remove_nans(df : pnd.DataFrame) -> pnd.DataFrame:
    if not df.isna().any().any():
        log.debug('No NaNs found in dataframe')
        return df

    ninit = len(df)
    df    = df.dropna()
    nfinl = len(df)

    log.warning(f'NaNs found, cleaning dataset: {ninit} -> {nfinl}')

    return df
# ---------------------------------------------
def _remove_repeated(df : pnd.DataFrame) -> pnd.DataFrame:
    l_hash = get_hashes(df, rvalue='list')
    s_hash = set(l_hash)

    ninit = len(l_hash)
    nfinl = len(s_hash)

    if ninit == nfinl:
        log.debug('No cleaning needed for dataframe')
        return df

    log.warning(f'Repeated entries found, cleaning up: {ninit} -> {nfinl}')

    df['hash_index'] = l_hash
    df               = df.set_index('hash_index', drop=True)
    df_clean         = df[~df.index.duplicated(keep='first')]

    if not isinstance(df_clean, pnd.DataFrame):
        raise ValueError('Cleaning did not return pandas dataframe')

    return df_clean
# ----------------------------------
# ---------------------------------------------
def get_hashes(df_ft : pnd.DataFrame, rvalue : str ='set') -> Union[set, list]:
    '''
    Will return hashes for each row in the feature dataframe

    rvalue (str): Return value, can be a set or a list
    '''

    if   rvalue == 'set':
        res = { hash_from_row(row) for _, row in df_ft.iterrows() }
    elif rvalue == 'list':
        res = [ hash_from_row(row) for _, row in df_ft.iterrows() ]
    else:
        log.error(f'Invalid return value: {rvalue}')
        raise ValueError

    return res
# ----------------------------------
def hash_from_row(row):
    '''
    Will return a hash from a pandas dataframe row
    corresponding to an event
    '''
    l_val   = [ str(val) for val in row ]
    row_str = ','.join(l_val)
    row_str = row_str.encode('utf-8')

    hsh = hashlib.sha256()
    hsh.update(row_str)

    hsh_val = hsh.hexdigest()

    return hsh_val
# ----------------------------------
def index_with_hashes(df):
    '''
    Will:
    - take dataframe with features
    - calculate hashes and add them as the index column
    - drop old index column
    '''

    l_hash = get_hashes(df, rvalue='list')
    ind_hsh= pnd.Index(l_hash)

    df = df.set_index(ind_hsh, drop=True)

    return df
# ----------------------------------
