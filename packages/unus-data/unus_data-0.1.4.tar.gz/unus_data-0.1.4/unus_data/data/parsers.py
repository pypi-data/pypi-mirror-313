import os
import sys
import re
from typing import Tuple, Sequence, Dict, Optional


def parse_fasta(fasta_string: str) -> Tuple[Sequence[str], Sequence[str]]:
  """Parses FASTA string and returns list of strings with amino-acid sequences.
  Arguments:
    fasta_string: The string contents of a FASTA file.

  Returns:
    A tuple of two lists:
    * A list of sequences.
    * A list of sequence descriptions taken from the comment lines. In the
      same order as the sequences.
  """
  sequences = []
  descriptions = []
  index = -1
  for line in fasta_string.splitlines():
    line = line.strip()
    if line.startswith('>'):
      index += 1
      descriptions.append(line[1:])  # Remove the '>' at the beginning.
      sequences.append('')
      continue
    elif not line:
      continue  # Skip blank lines.
    sequences[index] += line

  return sequences, descriptions

def parse_uniprot_fasta_desc(desc_string: str) -> Dict:
  """Parses the description string in a Uniprot FASTA file and return lists of strings"""
  auxs = []
  uniprot_ids = []
    
  for line in desc_string.splitlines():
    line = line.strip()
    if not line:
      continue
    else:
      print(re.split(r'\|', line))
      _, uniprot_id, aux = re.split(r'\|', line)
      uniprot_ids.append(uniprot_id)
      auxs.append(aux)
  return uniprot_ids, auxs


# def parse_dssp(dssp_string: str) -> Tuple[Sequence[str], Sequence[str]]:
#   """Parses DSSP output and returns a dictionary"""

#   ss_pos = slice(16, 17)
#   # Only keep the main part of dssp output
#   dssp_string = re.search(
#     r'  #  RESIDUE AA STRUCTURE(.*)',
#     dssp_string, 
#     flags=re.S
#     ).group(0) 
#   dssp_lines = re.split(r'\n', dssp_string.strip())  
#   ss_string = ''.join(line[ss_pos] if line[ss_pos] != ' ' else 'X' for line in dssp_lines)
  
#   return ss_string


def parse_dssp(dssp_string: str, expected_length: Optional[int]=None) -> Tuple[Sequence[str], Sequence[str]]:
  """Parses DSSP output and returns a dictionary. Note that the orginal PDB can contain missing residues, the length of the sequence is not always equal to the length of the DSSP output. Therefore, complete length is passed as an optional input to fill the missing residues with 'X'; Otherwise, we will use the length of the DSSP output as the length of the sequence."""
  
  residue_index_pos = slice(5, 10)
  ss_pos = slice(16, 17)
  
  dssp_string = re.search(
    r'  #  RESIDUE AA STRUCTURE(.*)',
    dssp_string, 
    flags=re.S
    ).group(0) 
  dssp_lines = re.split(r'\n', dssp_string.strip())[1:] # Skip the first line, # RESIDUE ...  
  length = int(dssp_lines[-1][residue_index_pos].strip()) if expected_length is None else expected_length
  ss_string = ['X'] * length

  for line in dssp_lines:
    residue_index = int(line[residue_index_pos].strip()) if line[residue_index_pos].strip() != '' else None
    if residue_index is None:
      continue
    
    ss_string[residue_index-1] = line[ss_pos].strip() if line[ss_pos].strip() != '' else ss_string[residue_index-1]

  return ''.join(ss_string)


  