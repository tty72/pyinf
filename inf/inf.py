import parser

class Section:
    def __init__(self, name):
        self.name = name
        self.regmods = []
        self.vars = {}

    def add_reg(self, values):
        self.regmods.append(values)

    def assign(self, name, values):
        self.vars[name]=values

class Inf(object):
    """ Attempt to parse an MS INF file """
    Parser = parser.InfParser
    
    def __init__(self, fp=None):
        root_section = Section('ROOT')
        self.sections = {'ROOT': root_section}
        self.comments = []
        self.curr_section = root_section
        if fp:
            self.parse(fp)

    def add_addreg(self, vals):
        """ Add add_registry values to section """
        self.curr_section.add_reg(vals)

    def add_section(self, name):
        """ Add a new section """
        self.curr_section = Section(name)
        self.sections[name] = self.curr_section

    def add_assign(self, var, values):
        """ Add a value assignment to current section """
        self.curr_section.assign(var, values)

    def parse(self, fp):
        p = self.Parser()
        p.add_callback('addreg', self.add_addreg)
        p.add_callback('section', self.add_section)
        p.add_callback('assign', self.add_assign)
        p.parse(fp)
