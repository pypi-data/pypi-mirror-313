# This file is authored by Peter Urban, Ghent University, and is subject to the MPL-2.0 license.
# SPDX-License-Identifier: MPL-2.0

import os
from pathlib import Path
import pickle
from collections import defaultdict
from typing import List, Dict, Union
from tqdm.auto import tqdm
from themachinethatgoesping.echosounders import filetemplates      # This is the filereader module for .all/.wcd files

def print_cache_file_statistics(
    file_cache_paths: List[str]) :

    Buffers = defaultdict(int)

    for fcp in tqdm(file_cache_paths.values(), delay=1):
        if not os.path.exists(fcp):
            continue
        
        # load the cache file
        cache = filetemplates.FileCache.from_file(fcp)
        
        for k,p1,p2 in cache.get_cache_buffer_header():
            Buffers[k] += p2-p1
            
        for k,p1,p2 in cache.get_cache_buffer_header():
            Buffers["- Combined -"] += p2-p1

        Buffers["- Source files -"] += cache.get_file_size()
        #cache.print()

    for k,v in Buffers.items():
        if not k.startswith('-'):
            print(f"{k}: {round(v/1024/1024,2)} 'MB' / {round(100*v/Buffers['- Source files -'],2)} %" )
            
    for k,v in Buffers.items():
        if k.startswith('-'):
            print(f"{k}: {round(v/1024/1024,2)} 'MB' / {round(100*v/Buffers['- Source files -'],2)} %" )

def remove_name_from_cache(
    file_cache_paths: List[str],
    name: str) -> None:

    for fcp in tqdm(file_cache_paths.values(), delay=1):
        if not os.path.exists(fcp):
            continue
            
        # load the cache file
        cache = filetemplates.FileCache.from_file(fcp)
        cache.remove_from_cache(name)
        cache.update_file(fcp)