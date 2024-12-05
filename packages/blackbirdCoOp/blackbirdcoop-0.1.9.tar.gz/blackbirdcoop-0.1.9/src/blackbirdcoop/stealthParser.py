"""
LIFT - UCSC iGEM 2024

Module: StealthParser

Generates stealth sequences based on IUPAC nucelotide usage within original file

Author: Vibhitha Nandakumar
"""


def replace_letters(input_str, replacements_dict):

    """Find all positions and possible replacements"""

    all_str = []
    positions = []
    for i, char in enumerate(input_str):
        if char in replacements_dict:
            positions.append((i, replacements_dict[char]))

    def gen_combos(input_str, positions, index=0):

        """Generate all combinations by replacing the characters"""

        if index >= len(positions):
            all_str.append("".join(input_str))
            return

        pos, replacements = positions[index]
        for replacement in replacements:
            new_str = list(input_str)
            new_str[pos] = replacement
            gen_combos(new_str, positions, index + 1)

    gen_combos(list(input_str), positions)

    return all_str


def return_seq(input_str):

    """Return function for all stealth sequences with extended IUPAC conventions"""

    u_nucleotide = {
        "N": ["A", "T", "C", "G"],
        "R": ["A", "G"],
        "Y": ["C", "T"],
        "K": ["G", "T"],
        "M": ["A", "C"],
        "S": ["C", "G"],
        "W": ["A", "T"],
        "B": ["C", "G", "T"],
        "D": ["A", "G", "T"],
        "H": ["A", "C", "T"],
        "V": ["A", "C", "G"],
    }

    all_str = replace_letters(input_str, u_nucleotide)

    return all_str


def textReader(filename):

    """Reads a text file with stealth hits and deciphers the IUPAC conventions"""

    stealthList = []
    # u_nucleotide = {'A','T','C','G'}
    u_nucleotide = {
        "N": ["A", "T", "C", "G"],
        "R": ["A", "G"],
        "Y": ["C", "T"],
        "K": ["G", "T"],
        "M": ["A", "C"],
        "S": ["C", "G"],
        "W": ["A", "T"],
        "B": ["C", "G", "T"],
        "D": ["A", "G", "T"],
        "H": ["A", "C", "T"],
        "V": ["A", "C", "G"],
    }

    with open(filename, "r") as file:

        next(file)

        for line in file:
            n_seq = line.split()[0] if line.split() else ""
            for n in n_seq:
                if n in u_nucleotide:
                    changed = return_seq(n_seq)

                    stealthList.extend(changed)
            else:
                stealthList.append(n_seq)

    return stealthList
