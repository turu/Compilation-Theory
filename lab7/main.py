import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()

    ast = parser.parse(text, lexer=Cparser.scanner)
    if ast:
        typeChecker = TypeChecker()
        typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
        if typeChecker.isValid:
            print "Type check finished"
            ast.accept(Interpreter())
            print "Interpretation finished"
        else:
            sys.stderr.write("Type check failed -> no interpretation")
    else:
        sys.stderr.write("Syntax check failed -> no type check & interpretation")
