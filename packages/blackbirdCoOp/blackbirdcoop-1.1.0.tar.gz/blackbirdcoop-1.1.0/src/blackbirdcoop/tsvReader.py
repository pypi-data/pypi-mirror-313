"""
LIFT - UCSC iGEM 2024

Module: TSVReader

Author: Vibhitha Nandakumar
"""

aa_to_codon = {
    "A": ["GCT", "GCC", "GCA", "GCG"],  # Alanine
    "C": ["TGT", "TGC"],  # Cysteine
    "D": ["GAT", "GAC"],  # Aspartic Acid
    "E": ["GAA", "GAG"],  # Glutamic Acid
    "F": ["TTT", "TTC"],  # Phenylalanine
    "G": ["GGT", "GGC", "GGA", "GGG"],  # Glycine
    "H": ["CAT", "CAC"],  # Histidine
    "I": ["ATT", "ATC", "ATA"],  # Isoleucine
    "K": ["AAA", "AAG"],  # Lysine
    "L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],  # Leucine
    "M": ["ATG"],  # Methionine (start codon)
    "N": ["AAT", "AAC"],  # Asparagine
    "P": ["CCT", "CCC", "CCA", "CCG"],  # Proline
    "Q": ["CAA", "CAG"],  # Glutamine
    "R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],  # Arginine
    "S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],  # Serine
    "T": ["ACT", "ACC", "ACA", "ACG"],  # Threonine
    "V": ["GTT", "GTC", "GTA", "GTG"],  # Valine
    "W": ["TGG"],  # Tryptophan
    "Y": ["TAT", "TAC"],  # Tyrosine
    "-": ["TAA", "TAG", "TGA"],  # Stop codons
}


class TSVReader:

    """
    Class to read codon usage files in TSV format

    Input: Host organism's codon usage table in .tsv format (most commonly found format for this purpose)

    Output: Dictionary containing the relative codon biases within the organism in a readable format

    """

    def __init__(self, inFile):
        self.inFile = inFile

    def format_usage(self):

        codonCount = {}

        with open(self.inFile, "r") as file:
            for line in file:
                codon, percent, count = line.strip().split()
                codonCount[codon] = [abs(float(count)), float(percent)]

            codonCount = {
                k: sorted(v, key=lambda v: v, reverse=True)
                for k, v in codonCount.items()
            }

        for key in aa_to_codon:
            aa_to_codon[key] = [
                [item] + codonCount.get(item, []) for item in aa_to_codon[key]
            ]

        for key, value in aa_to_codon.items():

            aa_to_codon[key] = sorted(value, key=lambda x: x[2], reverse=True)

        return aa_to_codon
