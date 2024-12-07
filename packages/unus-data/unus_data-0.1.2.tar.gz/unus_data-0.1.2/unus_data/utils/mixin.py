"""Provide Mixin classes ..."""

import pandas as pd
import seaborn as sns
import numpy as np


from matplotlib.axes import Axes
from typing import Optional 

class PlotMixin:
  """Class for plotting Mixin via seaborn ... Thus, no __init__ method ..."""
     
  def plot_histogram_map(
    self,
    df: pd.DataFrame,
    *,
    title: str='Untitled',
    bins: int=20,
    x: Optional[str]=None, 
    y: Optional[str]=None,
    hue: Optional[str]=None,
    is_kde: bool=True,
    log_scale: bool=False,
    ax: Optional[Axes]=None,
    shrink: float=1,
    stat: str='count', # choices: count, percent, density, probability
  ) -> Axes:
    """Plot histogram map"""
    ax = sns.histplot(
      df, 
      x=x,
      y=y,
      hue=hue,
      kde=is_kde,
      log_scale=log_scale,
      ax=ax,
      stat=stat,
      bins=bins,
      shrink=shrink,
    )
    ax.set_title(title)
    return ax
  
  def plot_2d_density_map(self, df: pd.DataFrame, x: str, y: str):
    ...
  
  def plot_tenary_map(self, df: pd.DataFrame, a: str, b: str, c: str):
    ...
    

class DataFilterMixin:
  ...
#   # Filtering condition, dssp proportion, length, contact relation, missing_atoms
#   DATACARD_SCHEMA = [
#     ('ID', str, None), # file name id, not necessarily pdb_id
#     ('ATOM_COORDS', np.ndarray,  None), # atom coordinates in terms of atom37, (..., 37, 3)
#     ('RESIDUE_INDEX', List[int], None), # residue index of the protein, LIst
#     ('ATOM_MASK', np.ndarray, None), # atom mask of the protein.
#     ('SEQUENCE', str, ''), # sequence of the protein.
#     ('SOLVED_LENGTH', int,  0), # [Optional] solved length of the protein, should be strictly equal to the length of the residue index.
#     ('EXPECTED_LENGTH', int, 0), # [Optional] expected length of the protein, should be strictly equal to the length of the sequence.\
#     ('SS_STRING', str, ''), # [Optional] secondary structure string of the protein.
#     ('PLDDT', float, 0.0), # [Optional] PLDDT score of the protein.  
#     ('METHOD', str, ''), 
#     ('RESOLUTION', float, 0.0),
#     ('RELEASE_DATE', str, ''),
#     ('CHAIN_INDEX', str, ''),
#     ('B_FACTORS', np.ndarray, None),
#     ('CLUSTER_ID', str, None),
#   ]
  