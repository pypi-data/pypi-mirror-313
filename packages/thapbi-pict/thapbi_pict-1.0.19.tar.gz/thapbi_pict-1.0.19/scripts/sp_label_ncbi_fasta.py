#!/usr/bin/env python3
"""Relabel an NCBI style FASTA file by taxonomy and taxid."""
import argparse
import os
import sys


from Bio.SeqIO.FastaIO import SimpleFastaParser


if "-v" in sys.argv or "--version" in sys.argv:
    print("v0.0.1")
    sys.exit(0)

usage = """\
The input FASTA file is expected to have records labeled with
'accession, space, species name, space, free text'. This will
be matched against an NCBI taxonomy dump (file names.dmp) and
relabeled as 'accesion, space, species name, space, taxid=XXX'
instead.
"""

parser = argparse.ArgumentParser(
    prog="sp_label_ncbi_fasta.py",
    description="Relabel an NCBI style FASTA file by taxonomy and taxid.",
    epilog=usage,
)
parser.add_argument(
    "-i",
    "--input",
    default="/dev/stdin",
    metavar="FASTA",
    help="Input FASTA file in NCBI style, default stdin.",
)
parser.add_argument(
    "-t",
    "--tax",
    type=str,
    required=True,
    metavar="DIRNAME",
    help="Folder containing NCBI taxonomy files 'names.dmp' etc.",
)
parser.add_argument(
    "-o",
    "--output",
    dest="output",
    default="/dev/stdout",
    metavar="FASTA",
    help="Output FASTA filename, defaults stdout.",
)

if len(sys.argv) == 1:
    sys.exit("ERROR: Invalid command line, try -h or --help.")
options = parser.parse_args()


def load_tax(taxdump):
    f = os.path.join(taxdump, "names.dmp")
    if not os.path.isfile(f):
        sys.exit(f"ERROR: Missing file {f}")
    from thapbi_pict.taxdump import load_names

    names, synonyms = load_names(f)
    rev_mapping = {name: taxid for (taxid, name) in names.items()}
    for taxid, alts in synonyms.items():
        for name in alts:
            rev_mapping[name] = taxid
    del synonyms
    return rev_mapping, names


name_to_taxid, taxid_to_name = load_tax(options.tax)
sys.stderr.write(f"Loaded {len(taxid_to_name)} taxids and their aliases\n")

with open(options.input) as in_handle, open(options.output, "w") as out_handle:
    for title, seq in SimpleFastaParser(in_handle):
        parts = title.split(None)
        idn = parts[0]
        name = parts[2:] if parts[1] in ("Uncultured", "UNVERIFIED:") else parts[1:]
        while " ".join(name) not in name_to_taxid:
            name.pop(-1)
            if not name:
                #sys.exit(f"ERROR: Could not match {title}")
                break
        if not name:
            sys.stderr.write(f"WARNING: Dropping {title}\n")
            continue
        taxid = name_to_taxid[" ".join(name)]
        sp = taxid_to_name[taxid]  # apply any synonym
        out_handle.write(f">{idn} {sp} taxid={taxid}\n{seq}\n")
