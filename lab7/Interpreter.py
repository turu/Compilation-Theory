import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *


class Interpreter(object):
    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.lhs.accept(self)
        r2 = node.rhs.accept(self)
        eval("a" + node.op + "b", {"a": r1, "b": r2})
        # try sth smarter than:
        # elsif(node.op=='-') ...
        # if(node.op=='+') return r1+r2

    @when(AST.Assignment)
    def visit(self, node):
        pass

    @when(AST.GroupedExpression)
    def visit(self, node):
        pass

        #
    #

    #!
    @when(AST.Const)
    def visit(self, node):
        return node.value

    #!
    # simplistic while loop interpretation
    @when(AST.WhileInstruction)
    def visit(self, node):
        r = None
        while node.condition.accept(self):
            r = node.instruction.accept(self)
        return r


