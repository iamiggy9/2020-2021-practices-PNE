import pathlib


class Seq:
    NULL='NULL'
    INVALID='ERROR'

    def __init__(self, strbases=NULL):
        if strbases == Seq.NULL:
            print("NULL Seq Created")
            self.strbases = strbases
        elif Seq.is_valid_sequence_2(strbases):
            self.strbases=strbases
            print('New sequence created')
        else:
            self.strbases=Seq.INVALID
            print('Invalid sequence')



    @staticmethod
    def is_valid_sequence_2(strbases):
        for c in strbases:
            if c!='A' and c !='C' and c!='G' and c!= 'T':
               return False
        return True

    def __str__(self):
        return self.strbases

    def len(self):
        if self.strbases == Seq.NULL or self.strbases==Seq.INVALID:
            return 0
        else:
            return len(self.strbases)

    def count_base(self, base):
        return self.strbases.count(base)

    def count(self):
        bases = ["A", "C", "T", "G"]
        count_bases = []
        for base in bases:
            count_bases.append(self.count_base(base))
        dictionary = dict(zip(bases, count_bases))
        return dictionary

    @staticmethod
    def reverse(self):
        rev_seq = ''
        if self.strbases == Seq.NULL:
            return self.strbases
        else:
            for e in self.strbases[::-1]:
                if e not in ["A", "C", "T", "G"]:
                    rev_seq = Seq.INVALID
                    return rev_seq

                else:
                    rev_seq += e
        return rev_seq
    @staticmethod
    def complement(self):
        comp_seq = ""
        if self.strbases == Seq.NULL:
            return self.strbases
        else:
            for e in self.strbases:
                if e not in ["A", "C", "T", "G"]:
                    comp_seq = Seq.INVALID
                    return comp_seq
                else:
                    if e == "A":
                        comp_seq += "T"
                    if e == "T":
                        comp_seq += "A"
                    if e == "C":
                        comp_seq += "G"
                    if e == "G":
                        comp_seq += "C"
            return comp_seq

    def read_fasta(self, filename):
            file_lines = pathlib.Path(filename).read_text().split("\n")
            body = (file_lines[1:])
            self.strbases = ''.join(body)
            return self



