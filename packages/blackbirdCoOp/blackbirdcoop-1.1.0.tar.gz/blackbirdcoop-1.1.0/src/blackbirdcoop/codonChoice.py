"""
LIFT - UCSC iGEM 2024

Module: CodonChoice

Author: Aurko Mahesh, Vibhitha Nandakumar
"""
from .stealthHits import StealthHits
from .codonUsage import CodonUsage
from .tsvReader import TSVReader

codon_to_aa = {
    # codon to amino acid code
    # convert T to U because they are translated...
    # T
    "TTT": "F",
    "TCT": "S",
    "TAT": "Y",
    "TGT": "C",  # UxU
    "TTC": "F",
    "TCC": "S",
    "TAC": "Y",
    "TGC": "C",  # UxC
    "TTA": "L",
    "TCA": "S",
    "TAA": "-",
    "TGA": "-",  # UxA
    "TTG": "L",
    "TCG": "S",
    "TAG": "-",
    "TGG": "W",  # UxG
    # C
    "CTT": "L",
    "CCT": "P",
    "CAT": "H",
    "CGT": "R",  # CxU
    "CTC": "L",
    "CCC": "P",
    "CAC": "H",
    "CGC": "R",  # CxC
    "CTA": "L",
    "CCA": "P",
    "CAA": "Q",
    "CGA": "R",  # CxA
    "CTG": "L",
    "CCG": "P",
    "CAG": "Q",
    "CGG": "R",  # CxG
    # A
    "ATT": "I",
    "ACT": "T",
    "AAT": "N",
    "AGT": "S",  # AxU
    "ATC": "I",
    "ACC": "T",
    "AAC": "N",
    "AGC": "S",  # AxC
    "ATA": "I",
    "ACA": "T",
    "AAA": "K",
    "AGA": "R",  # AxA
    "ATG": "M",
    "ACG": "T",
    "AAG": "K",
    "AGG": "R",  # AxG
    # G
    "GTT": "V",
    "GCT": "A",
    "GAT": "D",
    "GGT": "G",  # GxU
    "GTC": "V",
    "GCC": "A",
    "GAC": "D",
    "GGC": "G",  # GxC
    "GTA": "V",
    "GCA": "A",
    "GAA": "E",
    "GGA": "G",  # GxA
    "GTG": "V",
    "GCG": "A",
    "GAG": "E",
    "GGG": "G",  # GxG
}


class CodonChoice:

    """
    Class that creates a sequence with the optimal codon choices. Is recursively called to edit a target site until it exits the site

    Input: Host and Target organisms complete genome files, Stealth site list, and target sequence being editted

    Output: a sub-sequence that does not contain a stealth hit after correction

    """

    def __init__(self, hostIn, targetIn):

        self.hostIn = hostIn
        self.targetIn = targetIn

        targetCodonUsage = CodonUsage(self.targetIn)
        self.targetUsage_dict = targetCodonUsage.returnDict()

        tsvReader = TSVReader(self.hostIn)
        self.hostUsage_dict = tsvReader.format_usage()

    # def hostUsage(self):
    #     tsvReader = TSVReader(self.hostIn)
    #     hostUsage_dict = tsvReader.format_usage()

    #     return hostUsage_dict

    def host(self, codon):
        aa = codon_to_aa[codon]
        return self.hostUsage_dict[aa]

    def target(self, codon):
        aa = codon_to_aa[codon]

        return self.targetUsage_dict[aa]

    def if_same(new_index):
        try:
            new_index -= 1
            return new_index
        except IndexError:
            new_index += 1
            return new_index

    def replaceCodon(self, codon):

        """
        Function produces the most ideal codon replacement according to inherent host/target organism codon biases

        Input: A codon that is meant to be replaced

        Output: A replaceable codon
        """

        hostList = self.host(codon)
        targetList = self.target(codon)

        hostIndex = next(
            (i for i, sublist in enumerate(hostList) if codon in sublist), None
        )
        targetIndex = next(
            (i for i, sublist in enumerate(targetList) if codon in sublist), None
        )

        newIndex = 0

        if targetList[targetIndex][0] != hostList[hostIndex][0]:
            newIndex = hostIndex
        if targetList[targetIndex][0] in ["ATG", "TGG"]:
            newIndex = hostIndex
        else:
            newIndex = CodonChoice.if_same(hostIndex)
        if targetList[newIndex][0] == hostList[hostIndex][0]:
            newIndex = CodonChoice.if_same(newIndex)

        try:
            newCodon = targetList[newIndex][0]

        except IndexError:
            newIndex = 0
            newCodon = targetList[newIndex][0]

        return newCodon

    def altSeqMaker(self, input_dna, stealthHits, start=None, altList=None):

        """
        Function that alters and confirms the absense of a stealth hit in a given subsequence

        Input: A subsequence of the insert (format = 'codon-codon-stealth hit-codon-codon'), a list of stealth hits,
        a start value that defaults to 6 (the center codon) and an empty list

        Output: From the filled list of alternative subsequences, the first one that is ordered to be the best fit

        """

        if start == None:
            start = 6
        if altList == None or altList == []:
            altList = list()

        if len(input_dna[start : start + 3]) < 3:
            return altList[0][1] if altList else None
        

        hitStart = input_dna[start : start + 3]
        bias_codon = self.replaceCodon(hitStart)
        biasSeq = input_dna[:start] + bias_codon + input_dna[start + 3 :]
        biasStealth = StealthHits(stealthHits)
        biasHits = biasStealth.find_hits(
                biasSeq
            ) 
        altList.append((len(biasHits), biasSeq)) # codon bias sequence option


        targetList = self.target(hitStart)
        for target in targetList:
            newSeq = input_dna[:start] + target[0] + input_dna[start + 3 :]
            stealthHit = StealthHits(stealthHits)
            hits = stealthHit.find_hits(
                newSeq
            )  # finds hits to reconfirm if codon choice is favorable
            altList.append((len(hits), newSeq))

        altList.sort(key=lambda x: x[0])
        

        # Check if there is a valid alternative sequence
        for alt in altList:
            if alt[0] == 0:
                return alt[1]  # Return the first valid sequence

        return self.altSeqMaker(input_dna, stealthHits, start + 3, altList)
