"""
LIFT - UCSC iGEM 2024

Module: CodonOp ADD THE PERIOD BEFORE EACH FILE IMPORT

Author: Vibhitha Nandakumar
"""

from .fastAreader import FastAreader
from . import stealthParser
from .stealthHits import StealthHits
from .codonChoice import CodonChoice

import argparse


class RunAll:

    """
    Main functions that optimizes inserts based on host and target codon biases

    Input: insert file (.fasta), stealth file (.stealth/.txt), host codon bias file (.tsv), target genome file (.fa/.fasta)

    Output: An output file containing the most optimized sequence

    """

    def __init__(self, insert_In, stealth_In, host_In, target_In, outFile):
        self.insert = insert_In
        self.stealth = stealth_In
        self.host = host_In
        self.target = target_In

        self.outFile = outFile

    def find_tempStart(start, pos):

        """
        Sets a temporary 'start' position for a chosen subsequence. This choice 'start' position is approximately 2 codons
        away from a given stealth hit

        """

        temp = start % 3
        temps = pos - 6
        if start < 3:
            return 0
        if temp == 0:
            if temps < 0:
                return pos
            else:
                return temps
        else:
            if (temps - temp) < 0:
                return pos - temp
            else:
                return temps - temp

    def find_tempEnd(length, end, pos):

        """
        Sets a temporary 'end' position for a chosen subsequence. This choice 'end' position is approximately 2 codons
        away from a given stealth hit

        """

        temp = end % 3
        temps = pos + 6
        if end < 3:
            return length - 1
        if temp == 0:
            if temps < 0:
                return pos
            else:
                return temps
        else:
            if (temps - temp) < 0:
                return pos + temp
            else:
                return temps + temp

    def what_changes(seq, hits):

        """Builds and returns the subsequences or windows to be optimized"""

        seq_len = len(seq)
        tempAAs = []
        for hit in hits:
            start_pos = hit[0]
            end_pos = start_pos + len(hit[1]) - 1
            start = len(seq[0:start_pos])
            end = len(seq[end_pos:]) - 1
            tempStart_pos = RunAll.find_tempStart(start, start_pos)
            tempEnd_pos = RunAll.find_tempEnd(seq_len, end, end_pos)
            tempAAs.append([tempStart_pos, seq[tempStart_pos:tempEnd_pos]])

        return tempAAs

    def replaced(seq, replaced):

        """Formats the final sequence with all the altered sequences from CodonUsage.altSeqMaker()"""

        for stuff in replaced:
            length = len(stuff[1])

            seq = (
                seq[: stuff[0]] + stuff[1] + seq[stuff[0] + length :]
            )  # replaces choice sequence at position

        return seq

    def find_stealth_hits(self, iSeq):

        """Finds stealth hits and returns in list format"""

        stealthHit = StealthHits(self.stealthList)
        all_hits = stealthHit.find_hits(iSeq)  # finds initial stealth hits

        return all_hits

    def run_all(self):

        """

        Main function that runs all necessary modules

        """

        sourceReader = FastAreader(self.insert)
        insertRead = sourceReader.readFasta()  # Reads insert file
        for (header, seq) in insertRead:
            self.insert_title = header
            iSeq = seq

        self.stealthList = stealthParser.textReader(
            self.stealth
        )  # reads and deciphers the stealth file's contents

        codon_usage = CodonChoice(
            self.host, self.target
        )  # establishes host and target organisms' codon bias tables

        temps = []
        all_hits = self.find_stealth_hits(iSeq)  # finds initial stealth hits

        temp = RunAll.what_changes(
            iSeq, all_hits
        )  # formats the stealth hit site into sub-sequence in order to 'spot optimize'

        for thing in temp:
            binch = codon_usage.altSeqMaker(
                thing[1], self.stealthList, 6, []
            )  # processes and outputs an optimized sub-sequence
            if binch is None:
                binch = thing[1]

            temps.append([thing[0], binch])

        sequence = RunAll.replaced(
            iSeq, temps
        )  # appends all fixes to initial stealth sites

        return self.insert_title, sequence

    def outputFile(self):

        header, final_sequence = self.run_all()
        final_hits = self.find_stealth_hits(final_sequence)
        num_hits = len(final_hits)

        with open(self.outFile, "w") as file:
            file.write(f">{header} output [{num_hits}]\n")

            file.write(f"{final_sequence}")


def main():

    """
    Main function that stores CLI commands and executes BLACKBIRD

    The main input CLI that are manadatory are an gene insert file in Fasta format, a stealth hit file in txt format,
    a host (organism of origin for intended insert) organism's genome file (currently only supports in codon usage tsv format), and
    a target complete genome file in Fasta format

    """

    parser = argparse.ArgumentParser(
        description="Blackbird optimizes an insert sequence for non-model organisms.",
        usage=f"""blackbirdCoOp --insert (-n) <insert infile> --stealth (-s) <stealth infile> --hostT (-ht) <host genome infile> --target (-t) <target genome infile> --outfile -o [outfile | default: stdout]""",
    )

    parser.add_argument(
        "-n",
        "--insert",
        type=str,
        action="store",
        help="insert input file in FastA format",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--stealth",
        type=str,
        action="store",
        help="stealth input file in .txt format",
        required=True,
    )
    parser.add_argument(
        "-ht",
        "--hostT",
        type=str,
        action="store",
        help="host organism codon usage input file in TSV format",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        action="store",
        help="target organism genome input file in FastA format",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--outfile",
        default=None,
        type=str,
        action="store",
        help="output filename, default = STDOUT",
    )

    args = parser.parse_args()

    insert_In = args.insert
    stealth_In = args.stealth
    host_In = args.hostT
    target_In = args.target

    outFile = args.outfile

    run_blackbird = RunAll(insert_In, stealth_In, host_In, target_In, outFile)

    run_blackbird.outputFile()


# # will be removed after testing
# if __name__ == "__main__":
#     main()
