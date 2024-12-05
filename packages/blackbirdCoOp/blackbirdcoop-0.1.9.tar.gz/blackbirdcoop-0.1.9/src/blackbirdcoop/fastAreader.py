"""
LIFT - UCSC iGEM 2024

Module: FastAreader

Author: David L. Bernick
"""

import sys


class FastAreader:

    """

    Read fasta file from specified fname or STDIN if not given

    """

    def __init__(self, fname=""):
        """contructor: saves attribute fname"""

        self.fname = fname
        self.fileH = None

    def doOpen(self):

        """Opens Fasta file"""

        if self.fname == "":
            return sys.stdin
        else:
            return open(self.fname)

    def readFasta(self):

        """Reads and returns header and Fasta file content"""

        header = ""
        sequence = ""

        with self.doOpen() as self.fileH:

            header = ""
            sequence = ""

            # skip to first fasta header
            line = self.fileH.readline()
            while not line.startswith(">"):
                line = self.fileH.readline()
            header = line[1:].rstrip()

            for line in self.fileH:
                if line.startswith(">"):
                    yield header, sequence
                    header = line[1:].rstrip()
                    sequence = ""
                else:
                    sequence += "".join(line.rstrip().split()).upper()

        yield header, sequence
