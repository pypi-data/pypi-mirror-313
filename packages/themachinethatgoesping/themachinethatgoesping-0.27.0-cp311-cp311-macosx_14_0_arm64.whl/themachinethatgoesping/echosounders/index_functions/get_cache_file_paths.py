# This file is authored by Peter Urban, Ghent University, and is subject to the MPL-2.0 license.
# SPDX-License-Identifier: MPL-2.0

import os
from pathlib import Path
import pickle
from collections import defaultdict
from typing import List, Dict, Union

def get_cache_file_path(
    file_path: Union[str, Path], 
    cache_root: Union[str, Path, None] = None, 
    cache_file_ending: str = '.tmtgp.cache', 
    create_dir: bool = True) -> Path:
    """Return the path to the cache file for a given folder path

    Parameters
    ----------
    file_path : str or Path
        The path to the file that is indexed
    cache_root : str or Path, optional
        The path to the root folder containing all cache files. If None, the cache file will be in the same folder as the data files
    cache_name : str, optional
        The name of the cache file
    create_dir : bool, optional
        If true: create a subdirectory, by default True

    Returns
    -------
    Path
        The path to the cache file
    """
    
    if cache_root is None:
        return str(Path(file_path + cache_file_ending))
            
    cache_file = Path(os.path.abspath(cache_root))
    file_path = Path(os.path.abspath(file_path))
    root_path = 'root_' + file_path.parts[0]
    root_path = root_path.replace(':', '')

    cache_file = Path(str(cache_file.joinpath(root_path, *file_path.parts[1:])) + cache_file_ending)
    
    if create_dir:
        os.makedirs(cache_file.parent, exist_ok=True)
    
    return str(cache_file)


def get_cache_file_paths(
    file_paths: List[str], 
    cache_file_ending: str = '.tmtgp.cache', 
    cache_root: str = 'cache', 
    update_cache: Dict[str, str] = None, 
    verbose: bool = False, 
    create_dir: bool = True) -> Dict[str, str]:
    """Load index files for a given list of file paths

    Parameters
    ----------
    file_paths : list of str
        The list of file paths to load index files for
    cache_name : str, optional
        The name of the cache file, by default 'tmtgp.index'
    cache_root : str, optional
        The path to the root folder containing all cache files, by default 'cache'
    update_cache : dict, optional
        A dictionary to update with the loaded cache data, by default None
    verbose : bool, optional
        If true: print verbose output, by default False
    create_dir : bool, optional
        If true: create a subdirectory, by default True

    Returns
    -------
    dict
        A dictionary containing the loaded index cache data
    """
    
    if update_cache is None:
        cache_file_paths = {}
    else:
        cache_file_paths = update_cache
        
    loaded_index_cache_files = set()
    
    # look for existing files in each folder
    for fp in file_paths:
        try:
            folder_path, file = os.path.split(fp)
            
            index_file = get_cache_file_path(fp, cache_root, cache_file_ending, create_dir=create_dir)            
            
            if index_file in loaded_index_cache_files:
                continue
                
            loaded_index_cache_files.add(index_file)
            cache_file_paths[fp] = index_file
        except Exception as e:
            raise e
            pass
            
    return cache_file_paths
