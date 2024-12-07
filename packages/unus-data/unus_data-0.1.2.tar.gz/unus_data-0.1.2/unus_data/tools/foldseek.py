import os
import subprocess
import sys
import shutil
import pandas as pd
import re
import json
import time
import uuid
import pickle

from utils import PlotMixin

from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

UNKNOWN_VALUE: int = -1

@dataclass
class FoldSeekClusterOutput(PlotMixin):
  cluster_tsv_filepath: str
  all_seqs_fasta_filepath: str=None
  rep_seq_fast_filepath: str=None
  num_clusters: Optional[int]=UNKNOWN_VALUE
  time_used: float=UNKNOWN_VALUE
  cluster_dict: Dict=None

  
  def __post_init__(self):    
    self.cluster_dict = self.parse_cluster_tsv_data()
    
  def parse_cluster_tsv_data(self, save_filepath: Optional[str]=None) -> Dict[str, List[str]]:
    """Parse cluster data"""
    cluster_dict = {}
    with open(self.cluster_tsv_filepath, 'r') as f:
      lines = f.readlines()
      for line in lines:
        line = line.strip()
        rep_id, elem_id = re.split(r'\t', line)
        if cluster_dict.get(rep_id, None) is None:
          cluster_dict[rep_id] = [elem_id]
        else:
          cluster_dict[rep_id].append(elem_id)
      if save_filepath is not None:
        with open(save_filepath, 'w') as f:
          f.write(json.dumps(cluster_dict))
        print(f'Cluster data saved to {save_filepath}')
      return cluster_dict
    
    self.num_clusters = len(cluster_dict.keys())
    return cluster_dict
  
  @property
  def cluster_df(self) -> pd.DataFrame:
    """Convert cluster data to DataFrame"""
    cluster_data = self.cluster_dict
    cluster_stats = {}
    for rep_id in cluster_data.keys():
      cluster_stats[rep_id] = {
        'CLUSTER_ID': rep_id,
        'NUM_ELEMS': len(cluster_data[rep_id]),
        'ELEMS': cluster_data[rep_id]
      }
    df = pd.DataFrame(cluster_stats).T
    df.sort_values(by='num_elems', ascending=False, inplace=True)
    return df 
  
  @property
  def data(self) -> Dict[str, Dict]:
    _data = {}
    for k, v in self.cluster_dict.items():
      for elem in v:
        _data[elem] = {'CLUSTER_ID': k}
    return _data
  
  @property
  def data_as_df(self) -> pd.DataFrame:
    """Convert data to DataFrame"""
    return pd.DataFrame(self.data).T
  
  def save_self(self, filepath: str):
    """Save FoldSeekClusterOutput to local"""
    with open(filepath, 'wb') as f:
      pickle.dump(self, f)
  
  @classmethod
  def from_local_pkl(cls, filepath: str):
    """Load FoldSeekClusterOutput from local"""
    with open(filepath, 'rb') as f:
      return pickle.load(f)
  
  @classmethod
  def from_local(cls, filepath: str):
    """Load FoldSeekClusterOutput from local"""
    filepath = Path(filepath)
    if filepath.with_suffix('.pkl'):
      return cls.from_local_pkl(filepath)
    else:
      raise ValueError(f'Unknown file format for {filepath}')
                                                                                                             
class FoldSeek:
  """Python wrapper of FoldSeek tool."""

  def __init__(self, *, binary_path: str):
    self.binary_path = binary_path
  
  def cluster(
    self,
    *, 
    strut_dirpath: str, 
    tmp_dirpath: str='./tmp',
    prefix: str='res',
    output_dirpath: str='./output',
    converge_threshold: float=.9,
    ):
    """ Run easy-cluster algorithm. It accepts input in either PDB or MMCIF format, with support for both flat and gzipped files.
    """
    cmd = [
      self.binary_path,
      'easy-cluster',
      strut_dirpath,
      prefix,
      tmp_dirpath,
      '-c', str(converge_threshold),
    ]
    start = time.time()
    process = subprocess.Popen(
      cmd,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
      )
    
    stdout, stderr = process.communicate()
    print('Running FoldSeek easy-cluster ...')
    retcode = process.wait()
    end = time.time()
    if retcode:
      raise RuntimeError(f'FoldSeek easy-cluster failed with error code {retcode}.')
    
    save_dirpath = Path(output_dirpath) / f'output_{uuid.uuid4()}' 
    save_dirpath.mkdir(parents=True, exist_ok=True)
    files_to_move = [
      f'{prefix}_all_seqs.fasta',
      f'{prefix}_rep_seq.fasta',
      f'{prefix}_cluster.tsv'
      ]
    for file in files_to_move:
      shutil.move(
        file,
        save_dirpath
      )
    
    return FoldSeekClusterOutput(
      cluster_tsv_filepath=Path(save_dirpath) / f'{prefix}_cluster.tsv',
      all_seqs_fasta_filepath=Path(save_dirpath) / f'{prefix}_all_seqs.fasta',
      rep_seq_fast_filepath= Path(save_dirpath) / f'{prefix}_rep_seq.fasta',
      time_used=float(end-start)
    )
    
    
  


    