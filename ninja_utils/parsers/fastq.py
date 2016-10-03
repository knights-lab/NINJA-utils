class FASTQ:
    def __init__(self, fh):
        self.fh = fh

    def read(self):
        line = next(fh)
        while line:
            title = line[1:].strip()
            data = ''
            qualities = ''
            flag = True
            line = next(fh)
            while line and (flag or len(data) != len(qualities)):
                if line[0] == '+':
                    flag = False
                elif flag:
                    data += line.strip()
                else:
                    qualities += line.strip()
                line = next(fh)
            yield title, data, qualities


class FASTQ2:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        line = next(self.fp)
        while line:
            title = line[1:].strip()
            data = ''
            qualities = ''
            flag = True
            line = next(self.fp)
            while not line[0] == '@' and line:
                if line[0] == '+':
                    flag = False
                elif flag:
                    data += line.strip()
                else:
                    qualities += line.strip()
                line = next(self.fp)
            yield title, data, qualities

    def __enter__(self):
        self.fp = open(self.filename, 'r')
        self.line = next(self.fp)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            while self.line:
                title = self.line[1:].strip()
                data = ''
                qualities = ''
                flag = True
                self.line = next(self.fp)
                while not self.line[0] == '@' and self.line:
                    if self.line[0] == '+':
                        flag = False
                    elif flag:
                        data += self.line.strip()
                    else:
                        qualities += self.line.strip()
                    self.line = next(self.fp)
                return title, data, qualities
        except Exception:
            raise StopIteration
