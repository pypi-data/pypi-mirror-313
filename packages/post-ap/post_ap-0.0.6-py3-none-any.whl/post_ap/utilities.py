'''
Module with utility functions
'''

import os

import toml
import yaml
import dmu.generic.utilities as gut

from XRootD              import client
from dmu.logging.log_store import LogStore

log = LogStore.add_logger('post_ap:utilities')
local_config = False

# --------------------------------------
class Data:
    '''
    Data meant to hold shared attributes
    '''
    lx_user   : str
    conf_path : str
# --------------------------------------
def load_config(cfg_nam : str, kind :str ='yaml') -> dict:
    '''
    Parameters
    -----------------
    cfg_nam (str): Name of config file, without extension
    kind    (str): Type of file, e.g. yaml (default), toml, etc

    Returns
    -----------------
    d_config (dict): Dictionary with configuration
    '''
    if not local_config:
        val = _load_grid_config(cfg_nam, kind)
    else:
        val = _load_local_config(cfg_nam, kind)

    return val
# --------------------------------------
def _load_local_config(cfg_nam : str, kind : str) -> dict:
    '''
    Will pick up config file from installed project
    '''
    cfg_path = f'{Data.conf_path}/post_ap/{cfg_nam}.{kind}'
    cfg_path = str(cfg_path)
    if not os.path.isfile(cfg_path):
        raise FileNotFoundError(f'Config path not found: {cfg_path}')

    log.warning(f'Loading local config file: {cfg_path}')

    if   kind == 'toml':
        data = toml.load(cfg_path)
    elif kind == 'yaml':
        with open(cfg_path, encoding='utf-8') as ifile:
            data = yaml.safe_load(ifile)
    else:
        raise ValueError(f'Invalid config type: {kind}')

    return data
# --------------------------------------
@gut.timeit
def _load_grid_config(cfg_nam :str, kind : str) -> dict:
    '''
    Will use XROOTD to pick up file from grid
    '''
    xrd_path = f'root://x509up_u1000@eoslhcb.cern.ch//eos/lhcb/grid/user/lhcb/user/{Data.lx_user[0]}/{Data.lx_user}/run3/ntupling/config/{cfg_nam}.{kind}'
    log.info(f'Loading: {xrd_path}')
    with client.File() as ifile:
        status, _ = ifile.open(xrd_path)
        if not status.ok:
            log.error(status.message)
            raise

        status, file_content = ifile.read()
        if not status.ok:
            log.error(status.message)
            raise FileNotFoundError

        content = file_content.decode('utf-8')

        if   kind == 'toml':
            data = toml.loads(content)
        elif kind == 'yaml':
            data = yaml.safe_load(content)
        else:
            raise ValueError(f'Invalid config type: {kind}')

        return data
# --------------------------------------
def _initialize():
    if 'LXNAME' not in os.environ:
        raise ValueError('Cannot find LXNAME in environment')

    Data.lx_user = os.environ['LXNAME']

    if 'CONFPATH' in os.environ:
        Data.conf_path = os.environ['CONFPATH']
# --------------------------------------
_initialize()
