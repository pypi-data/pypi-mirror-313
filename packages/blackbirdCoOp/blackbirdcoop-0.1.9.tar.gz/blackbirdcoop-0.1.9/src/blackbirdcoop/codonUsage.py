"""
LIFT - UCSC iGEM 2024

Module: CodonUsage

Author: Vibhitha Nandakumar
"""
from .fastAreader import FastAreader

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

# codon tally dictionary
codon_count = {
    # U
    "TTT": 0,
    "TCT": 0,
    "TAT": 0,
    "TGT": 0,  # UxU
    "TTC": 0,
    "TCC": 0,
    "TAC": 0,
    "TGC": 0,  # UxC
    "TTA": 0,
    "TCA": 0,
    "TAA": 0,
    "TGA": 0,  # UxA
    "TTG": 0,
    "TCG": 0,
    "TAG": 0,
    "TGG": 0,  # UxG
    # C
    "CTT": 0,
    "CCT": 0,
    "CAT": 0,
    "CGT": 0,  # CxU
    "CTC": 0,
    "CCC": 0,
    "CAC": 0,
    "CGC": 0,  # CxC
    "CTA": 0,
    "CCA": 0,
    "CAA": 0,
    "CGA": 0,  # CxA
    "CTG": 0,
    "CCG": 0,
    "CAG": 0,
    "CGG": 0,  # CxG
    # A
    "ATT": 0,
    "ACT": 0,
    "AAT": 0,
    "AGT": 0,  # AxU
    "ATC": 0,
    "ACC": 0,
    "AAC": 0,
    "AGC": 0,  # AxC
    "ATA": 0,
    "ACA": 0,
    "AAA": 0,
    "AGA": 0,  # AxA
    "ATG": 0,
    "ACG": 0,
    "AAG": 0,
    "AGG": 0,  # AxG
    # G
    "GTT": 0,
    "GCT": 0,
    "GAT": 0,
    "GGT": 0,  # GxU
    "GTC": 0,
    "GCC": 0,
    "GAC": 0,
    "GGC": 0,  # GxC
    "GTA": 0,
    "GCA": 0,
    "GAA": 0,
    "GGA": 0,  # GxA
    "GTG": 0,
    "GCG": 0,
    "GAG": 0,
    "GGG": 0,  # GxG
}


class CodonUsage:

    """
    Class to build target codon usage tables (current version 0.0.4)

    Input: complete genome file of target organism in Fasta format

    Output: Dictionary containing the relative codon biases within the organism

    """

    def __init__(self, genome):
        self.genome_In = genome

    def find_start(codon):

        """Find start codons to determine ORF"""

        if codon in aa_to_codon["M"]:
            return True
        else:
            return False

    def find_end(genome, length, start_pos):

        """Finds stop codons to determine ORF"""

        for i in range(start_pos, length, 3):
            if genome[i : i + 3] in aa_to_codon["-"]:
                return i

    def find_orf(self, genome):

        """Finds and stores ORFs in list"""

        all_orfs = []

        for i in range(0, len(genome), 3):
            if CodonUsage.find_start(genome[i : i + 3]):
                end_pos = CodonUsage.find_end(genome, len(genome), i)

                all_orfs.append(genome[i : end_pos + 3])

        return all_orfs

    def tally(self, all_orfs):

        """Counts codons in ORFs and adds to codon_count"""

        total_codons = 0

        for orf in all_orfs:
            for i in range(0, len(orf), 3):
                codon = orf[i : i + 3]
                total_codons += 1
                if codon in codon_count:
                    codon_count[codon] += 1

        return total_codons

    def percentage(self, total_codons):

        """Calculates percentages of codon usages"""

        for codon in codon_count:
            if isinstance(codon_count[codon], list):
                break

            p = codon_count[codon]

            each = f"{(p/total_codons)*1000:.2f}"

            codon_count[codon] = [codon_count[codon], float(each)]

    def returnDict(self):

        """Runs and formats output codon bias dictionary"""

        sourceReader = FastAreader(self.genome_In)
        fileRead = sourceReader.readFasta()
        genomeRead = []

        for (_, i) in fileRead:
            genomeRead.append(i)
        whole_genome = genomeRead[0]

        all_orfs = self.find_orf(whole_genome)

        total = self.tally(all_orfs)

        self.percentage(total)

        for key in aa_to_codon:

            aa_to_codon[key] = [
                [item] + codon_count.get(item, [])
                for item in aa_to_codon[key]
                if not isinstance(item, list)
            ]

        for key, value in aa_to_codon.items():
            aa_to_codon[key] = sorted(value, key=lambda x: x[2], reverse=True)

        return aa_to_codon
