import os
import sys
import pandas as pd
import json
from .parsers import parse_fasta, parse_uniprot_fasta_desc
from pathlib import Path


def convert_fasta2df(
  fasta_string: str, 
  save_jsonpath: str=None, 
  source_from: str='uniprot'
) -> pd.DataFrame:
  """Converts FASTA string to DataFrame"""
  seq, desc = parse_fasta(fasta_string)
  desc = '\n'.join(desc)
  if source_from == 'uniprot':
    uniprots_id, aux = parse_uniprot_fasta_desc(desc)
    data = {
    'uniprot_id': uniprots_id,
    'desc_aux': aux,
    'sequence': seq
  }
  else:
    data = {
      'desc_aux': desc,
      'sequence': seq
    }  
  df = pd.DataFrame(data)
  if save_jsonpath is not None:
    df.to_json(save_jsonpath, orient='records')
  return df