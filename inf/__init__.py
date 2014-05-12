from inf import Inf

def register_parser(parser):
    inf.Inf.Parser = parser

def register_filereader(fr):
    inf.parser.InfParser.FileReader = fr
