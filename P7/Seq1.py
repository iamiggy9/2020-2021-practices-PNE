from pathlib import Path


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

    def count_base(self):
        a,c,g,t = 0,0,0,0
        if not(self.strbases == Seq.NULL)and not(self.strbases == Seq.INVALID):
            for ch in self.strbases:
                if ch == 'A':
                    a += 1
                elif ch == 'G':
                    g += 1
                elif ch == 'C':
                    c += 1
                elif ch == 'T':
                    t += 1
        return a,c,g,t

    def count(self):
       a,c,g,t = self.count_base()
       return {'A': a,'C': c ,'G': g,'T': t}
    def percentage_base(self,count_bases, seq_len):
        a = 'A: ' + str(round(count_bases[0] / seq_len*100, 2)) + '%'
        c = 'C: ' + str(round(count_bases[1] / seq_len * 100, 2)) + '%'
        g = 'G: ' + str(round(count_bases[2] / seq_len * 100, 2)) + '%'
        t = 'T: ' + str(round(count_bases[3] / seq_len * 100, 2)) + '%'
        return{'A': a,'C': c ,'G': g,'T': t}
    @staticmethod
    def frequent_base(dict_count):
        return max(dict_count, key=dict_count.get)
    def count(self):
        a, c,g,t = self.count_base()
        return{'A': a,'C': c ,'G': g,'T': t}
    @staticmethod
    def take_out_first_line(seq):
        return seq[seq.find('\n') + 1:].replace('\n','')


    def read_fasta(self,filename):
            self.strbases =Seq.take_out_first_line(Path(filename).read_text())
            print(self.strbases)




