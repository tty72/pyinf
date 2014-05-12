import io

class FileReader(object):
    def __init__(self, fp):
        self.file = io.open(fp, encoding='utf-16')

    def readline(self):
        """ Get a single line from file pointer, merging
            lines continued with a trailing '\'
        """
        line = self.file.readline()
        # FIXME? This does not allow for escaping a trailing \ (e.g. \\)
        while line.rstrip()[-1:] == '\\':
            line = line.rstrip()[:-1]
            line += self.file.readline()
        if line.lstrip() and line.lstrip()[0]==';':
            return ' '
        # Remove trailing comments
        quoted = False
        for p,c in enumerate(line):
            if c == '"':
                quoted = not quoted
            if c == ';' and not quoted:
                line = line[:p]
                break
        return line

    def __iter__(self):
        return self

    def next(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line
