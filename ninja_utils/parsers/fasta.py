class FASTA:
    def __init__(self, fh):
        """

        :param fh: str
        :return:
        """
        self.fh = fh

    def read(self):
        """
        :return: tuples of (title, seq)
        """
        title = None
        data = None
        for line in self.fh:
            if line[0] == ">":
                if title:
                    yield (title.strip(), data)
                title = line[1:]
                data = ''
            else:
                data += line.strip()
        if not title:
            yield None
        yield (title.strip(), data)

    def __call__(self):
        self.read()
