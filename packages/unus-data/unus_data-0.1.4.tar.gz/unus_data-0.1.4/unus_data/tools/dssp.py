import concurrent.futures
import os
import subprocess
import sys
import shutil
import pandas as pd
import re
import json
import time
import matplotlib.pyplot as plt
import concurrent
import pickle
import uuid

from utils import PlotMixin
from tqdm import tqdm
from data.parsers import parse_dssp
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Union, Sequence, Set



@dataclass
class DSSPOutput(PlotMixin):
  DSSPOutput_df_columns: Set[str] = ('ID', 'SS_STRING')
  pdb_dirpath: Sequence[str]=''
  output_dirpath: Sequence[str]=''
  time_used: float=-1
  num_files: int=0
  data: Dict[str, Dict]=None
  
  def __post_init__(self):
    self.pdb_dirpath = Path(self.pdb_dirpath)
    self.output_dirpath = Path(self.output_dirpath) 
    if isinstance(self.data, list):   
      self.data = self._statisfy_data()
    
    assert set(self.DSSPOutput_df_columns).issubset(set(self.data_as_df.columns)), 'Data columns do not match DSSPOutput_df_columns'


  @property
  def data_as_df(self) -> pd.DataFrame:
    """Convert DSSP data to DataFrame"""
    return pd.DataFrame(self.data).T
  
  @classmethod
  def satisfy_ss_string(cls, ss_string: Sequence[str], missing_value_holder: str='X') -> Dict:
    """Parse secondary structure string"""
    ss_dict = {
      'H': 'H',
      'G': 'H',
      'I': 'H',
      'E': 'E',
      'B': 'E',
      'T': 'C',
      'S': 'C',
      'C': 'C',
      missing_value_holder: missing_value_holder
    }
    ss_string = ''.join([ss_dict.get(ss_token, missing_value_holder) for ss_token in ss_string])
  
    return ss_string.count('H'), ss_string.count('E'), ss_string.count('C'), ss_string.count(missing_value_holder)

  @classmethod
  def from_local(cls, filepath: Sequence[str]):
    """Load DSSPOutput from file"""
    with open(filepath, 'rb') as f:
      return pickle.load(f) 
  
  @classmethod
  def from_data_df(cls, data_df: pd.DataFrame):
    """Load DSSPOutput from DataFrame"""
    assert set(cls.DSSPOutput_df_columns).issubset(set(data_df.columns)), 'Data columns do not match DSSPOutput_df_columns'
    return cls(
      data=data_df[list(cls.DSSPOutput_df_columns)].T.to_dict(),
      num_files=len(data_df), 
      ) 
  

  def _statisfy_data(self):
    data = {}
    for i, (pdb_id, ss_string) in enumerate(self.data):
      H_count, E_count, C_count, missing_count = self.satisfy_ss_string(ss_string)
      data[pdb_id] = {
        'ID': pdb_id,
        'SS_STRING': ss_string,
        'H_COUNT': H_count,
        'E_COUNT': E_count,
        'C_COUNT': C_count,
        'MISSING_COUNT': missing_count,
      }
    return data

  def save_self(self, save_filepath: Sequence[str]):
    """Save DSSPOutput to file"""
    with open(save_filepath, 'wb') as f:
      pickle.dump(self, f)
      
  # def plot_sse_proportion_analysis(self) -> plt.Figure:
  #   """Plot proportion of secondary structure elements (SSE) among overall dataframe, in style of PVQD.
  #   reference: https://www.biorxiv.org/content/10.1101/2023.11.18.567666v1.full.pdf, Fig 3.D
  #   """
  #   df = self.data_as_df
  #   length = df['length'].astype(float)
  #   df['H_freq'] = (df['H_count'].astype(float) / length).replace(float('inf'), float('nan'))
  #   df['E_freq'] = (df['E_count'].astype(float) / length).replace(float('inf'), float('nan'))
  #   df['C_freq'] = (df['C_count'].astype(float) / length).replace(float('inf'), float('nan'))
    
  #   # fig
  #   fig, axes = plt.subplots(1, 3, figsize=(25, 5))
  #   H_ax = self.plot_histogram_map(df, title='alpha helix', x='H_freq', stat='probability', bins=20, shrink=.5, ax=axes[0])
  #   H_ax.set_ylim(0, .25)
  #   E_ax = self.plot_histogram_map(df, title='beta strand', x='E_freq', stat='probability', bins=20, shrink=.5, ax=axes[1])
  #   E_ax.set_ylim(0, .8)
  #   C_ax = self.plot_histogram_map(df, title='coil', x='C_freq', stat='probability', bins=20,shrink=.5, ax=axes[2])
  #   C_ax.set_ylim(0, .45)
  #   return fig, axes
  

class DSSP:
  """Python wrapper of DSSP. 
  *Install command: `sudo apt-get install dssp`
  """
  def __init__(
    self,
    *,
    binary_path: Sequence[str],
    log_filepath: str='dssp.log',
  ):
    self.binary_path = binary_path
    self.log_filepath = log_filepath # TODO: implement logging logger
  
  @property
  def version(self) -> str:
    cmd = [
      self.binary_path,
      '--version'
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    retcode = process.wait()
    if retcode:
      raise RuntimeError(f'Error running DSSP: {stderr.decode()}')
    # parse version information
    return re.search(r'version(.*)', stdout.decode()).group(1).strip()
    
  def run(
    self, 
    pdb_filepath: Union[str, List[str]],
    output_filepath: str='stdout', # e.g. 1a00.dssp
    expected_length: Optional[int]=None,
    ) -> Tuple[Sequence[str], Sequence[str]]:
    """Run DSSP on PDB file(s)"""
    cmd = [
      self.binary_path,
      '-i', pdb_filepath,
      *(('-o', output_filepath) if output_filepath != 'stdout' else ''),
      '-v'
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    retcode = process.wait()
    
    if retcode:
      
      # If error occurs, log the error and continue ...
      with open(self.log_filepath, 'a') as f:
        f.write(f'Error running DSSP on {pdb_filepath}: {stderr.decode()}\n')
      return Path(pdb_filepath).stem, '' 
    
    if output_filepath == 'stdout':
      dssp_string = stdout.decode()
    else:
      with open(output_filepath, 'r') as f:
        dssp_string = f.read()
    
    return Path(pdb_filepath).stem, parse_dssp(dssp_string, expected_length)
  
  def run_dir(
    self, 
    pdb_dirpath: str,
    output_dirpath: str='stdout',
    max_workers: str=os.cpu_count(),
    extra_dict: Optional[str]=None,
    ) -> DSSPOutput:
    """Run DSSP on a directory of PDB files"""
    pdb_dirpath = Path(pdb_dirpath)
    pdb_filepaths = list(pdb_dirpath.glob('*.pdb'))
    results = []
    start = time.time()
    with tqdm(total=len(pdb_filepaths), desc=f'Running DSSP on {pdb_dirpath}') as pbar:
      with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as process_executor:
        tasks = []
        for pdb_filepath in pdb_filepaths:
          if output_dirpath != 'stdout':
            output_filepath = Path(output_dirpath) / f'{pdb_filepath.stem}.dssp'
          else:
            output_filepath = 'stdout'
          expected_length = len(extra_dict['md5_to_sequence_3'][extra_dict['meta_data'][pdb_filepath.stem]['md5']].split('-')) if extra_dict is not None else None
          tasks.append(process_executor.submit(self.run, pdb_filepath, output_filepath.absolute(), expected_length))
          
        for task in concurrent.futures.as_completed(tasks):
          results.append(task.result())
          pbar.update(1)
          
    return DSSPOutput(
      data=results,
      pdb_dirpath=pdb_dirpath, 
      output_dirpath=output_dirpath, 
      time_used=time.time()-start,
      num_files=len(results),
      )
    
      
      
      
