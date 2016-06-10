class FASTQ:
    def __init__(self, fh):
        self.fh = fh

    def read(self):
        line = next(self.fh)
        while line:
            title = line[1:].strip()
            data = ''
            qualities = ''
            flag = True
            line = next(self.fh)
            while not line[0] == '@' and line:
                if line[0] == '+':
                    flag = False
                elif flag:
                    data += line.strip()
                else:
                    qualities += line.strip()
                line = next(self.fh)
            yield title, data, qualities

