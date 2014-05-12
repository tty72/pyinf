import re
import filereader

class InfParser(object):
    FileReader = filereader.FileReader

    def __init__(self):
        self.regex_table = [
            ['addreg', re.compile('^(HKCR|HKCU|HKLM|HKU|HKR)'
                                  '(,[^,]*)?(,[^,]*)?(,[^,]*)?'
                                  '(,[^,]*)?(,[^,]*)?'), 
             self.do_addreg],
            ['section', re.compile('^\[(.*)\]$'), self.do_section],
            ['assignment', re.compile('^([^=]*)=(.*)$'),
             self.do_assign],
            ]
        self.callbacks = { 'addreg': [],
                           'section': [],
                           'assign': [],
                           'statement': [],
                           }

    def add_callback(self, name, cb):
        for k in self.callbacks:
            if k == name:
                self.callbacks[name].append(cb)
        
    def do_cb(self, name, *args):
        for cb in self.callbacks[name]:
            cb(*args)

    def do_addreg(self, match):
        """ Takes a regex match result, adds to addreg list """
        res = [x.lstrip(',')
               for x in match.groups() if x!=None]
        self.do_cb('addreg', res)

    def do_section(self, match):
        """ Takes a regex match result, adds a section """
        # FIXME: Allow for merge with existing section of same name
        name = match.group(1).upper()
        self.do_cb('section', name)

    def do_assign(self, match):
        """ Takes a regex match, adds a value assignment """
        var = match.group(1).strip()
        values = match.group(2).strip()
        #FIXME: Does not handle quoting
        values = [x.strip() for x in values.split(',')]
        self.do_cb('assign', var, values)

    def parse(self, fp):
        f = self.FileReader(fp)

        #for line in f:
        line = f.readline()
        while line:
            line = line.strip()#.decode('utf-16-LE')
            if line == '':
                line = f.readline()
                continue
            for m in self.regex_table:
                match = m[1].match(line) #Ugh. Really? This seems lame.
                if match:
                    m[2](match)
                    break
            else:
                print "UNHANDLED LINE: %s"%line
            line = f.readline()

