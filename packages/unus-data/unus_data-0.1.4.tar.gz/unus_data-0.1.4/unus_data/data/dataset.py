import concurrent.futures
import os
import warnings
warnings.filterwarnings("ignore")
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import torch
import uuid
import pandas as pd
import pickle
import concurrent

from utils.io_utils import run_pool_tasks
from .protein import Protein, from_pdb_string
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union, Any, Dict, Optional, Sequence



# DATACARD SCHEMA AND ITS DEFAULT VALUES

DATACARD_SCHEMA = [
  ('ID', str, None), # file name id, not necessarily pdb_id
  ('ATOM_COORDS', np.ndarray,  None), # atom coordinates in terms of atom37, (..., 37, 3)
  ('RESIDUE_INDEX', List[int], None), # residue index of the protein, LIst
  ('ATOM_MASK', np.ndarray, None), # atom mask of the protein.
  ('SEQUENCE', str, ''), # sequence of the protein.
  ('SOLVED_LENGTH', int,  0), # [Optional] solved length of the protein, should be strictly equal to the length of the residue index.
  ('EXPECTED_LENGTH', int, 0), # [Optional] expected length of the protein, should be strictly equal to the length of the sequence.\
  ('SS_STRING', str, ''), # [Optional] secondary structure string of the protein.
  ('PLDDT', float, 0.0), # [Optional] PLDDT score of the protein.  
  ('METHOD', str, ''), 
  ('RESOLUTION', float, 0.0),
  ('RELEASE_DATE', str, ''),
  ('CHAIN_INDEX', str, ''),
  ('B_FACTORS', np.ndarray, None),
  ('CLUSTER_ID', str, None),
]


@dataclass
class UnusDataCard(DataFilterMixin):
  """Dataset profiling ..."""
  name: str=f'Untitled_{uuid.uuid4()}'
  num_struts: int=0
  num_strut_clusters: int=0
  data: Dict[str, Dict]=None
  
  @property
  def data_as_df(self) -> pd.DataFrame:
    """Convert data to DataFrame"""
    return pd.DataFrame(self.data).T
  
  @classmethod
  def read_pdb_one(cls, pdb_filepath: str) -> Dict:
    """Read pdb file"""
    try:
      with open(pdb_filepath, 'r') as f:
        pdb_string = f.read()
        protein = from_pdb_string(pdb_string)
        protein_data = {
          'ID': str(pdb_filepath.stem),
          'ATOM_COORDS': protein.atom_positions,
          'SEQUENCE': protein.aatype,
          'ATOM_MASK': protein.atom_mask,
          'RESIDUE_INDEX': protein.residue_index,
          'CHAIN_INDEX': protein.chain_index,
          'B_FACTORS': protein.b_factors,
        }
        return str(pdb_filepath.stem), protein_data
    except:
        return str(pdb_filepath.stem), None
  
  @classmethod
  def from_local_pdb(
    cls,
    pdb_dirpath: str,
    *,
    max_workers: int=os.cpu_count(),
    name: str=f'Untitled_{uuid.uuid4()}',
  ) -> 'UnusDataCard':
    data = {}
    tasks = []
    pdb_dirpath = Path(pdb_dirpath)
    pdb_files = list(pdb_dirpath.rglob('*.pdb'))
    results = run_pool_tasks(cls.read_pdb_one, pdb_files, num_workers=max_workers)
    for (pdb_id, protein_data) in results:
      if protein_data is not None:
        data[pdb_id] = protein_data
    return cls(
      name=name, 
      num_struts=len(data.keys()), 
      data=data
      )
  
  @classmethod
  def from_local_pkl(cls, filepath: str) -> 'UnusDataCard':
    """Load UnusDataCard from local"""
    with open(filepath, 'rb') as f:
      return pickle.load(f)
  
  
  @classmethod
  def from_local(cls, filepath: Sequence[str], num_workers: int=os.cpu_count()) -> 'UnusDataCard':
    """Load UnusDataCard from local"""
    filepath = Path(filepath)
    if filepath.suffix == '.pkl':
      return cls.from_local_pkl(filepath)
    elif filepath.is_dir():
      return cls.from_local_pdb(filepath, max_workers=num_workers)
    
  def save_self(
    self, 
    save_filepath: str
  ) -> None:
    with open(save_filepath, 'wb') as f:
      pickle.dump(self, f)
  
  def save_data_as_json(
    self,
    save_filepath: str
  ) -> None:
    self.data_as_df.to_json(save_filepath)
    
  
  def with_extra_stats_dict(
    self, 
    stats_dict: Dict[str, Dict],
  ) -> Dict[str, Dict]:
    for pdb_id in self.data.keys():
      self.data[pdb_id].update(stats_dict.get(pdb_id, {}))
    return self.data
  
  def merge(
    self, 
    other: 'UnusDataCard',
  ) -> 'UnusDataCard':
    intersection = set(self.data.keys).intersection(set(other.data.keys()))
    if len(intersection) > 0:
      raise ValueError(f'Intersection of keys: {intersection}')
    self.data.update(other.data)
    return self
  
  def add_stats(
    self, 
    stat_names: List,
    default_values: List,
  ) -> 'UnusDataCard':
    if not isinstance(stat_names, list):
      stat_names = [stat_names]
    if not isinstance(default_values, list):
      default_values = [default_values]
    for pdb_id in self.data.keys():
      for stat_name, default_value in zip(stat_names, default_values):
        self.data[pdb_id][stat_name] = self.data[pdb_id].get(stat_name, default_value)
    return self
  

  

