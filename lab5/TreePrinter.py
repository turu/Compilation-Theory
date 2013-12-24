import AST

INDENT_TOKEN = "| "


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.ExpressionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent + 1), self.expressionList))
        
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.lhs.printTree(indent + 1) + self.rhs.printTree(indent + 1)

    @addToClass(AST.GroupedExpression)
    def printTree(self, indent=0):
        return self.interior.printTree(indent)
        
    @addToClass(AST.InvocationExpression)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "FUNCALL\n" + INDENT_TOKEN * (indent + 1) + str(self.name) + "\n" + \
            self.args.printTree(indent+1)
        
    @addToClass(AST.Const)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + str(self.value) + "\n"
        
    @addToClass(AST.Argument)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "ARG " + self.name + "\n"

    @addToClass(AST.ArgumentList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.argList))
            
    @addToClass(AST.FunctionExpressionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.fundefs))
    
    @addToClass(AST.FunctionExpression)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "FUNDEF\n" + INDENT_TOKEN * (indent + 1) + str(self.name) + "\n" + \
            INDENT_TOKEN * (indent + 1) + "RET " + str(self.retType) + "\n" + self.args.printTree(indent + 1) + \
            self.body.printTree(indent)
         
    @addToClass(AST.DeclarationList)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "DECL\n" + "".join(map(lambda x: x.printTree(indent + 1), self.declarations))
        
    @addToClass(AST.Declaration)
    def printTree(self, indent=0):
        return self.inits.printTree(indent)
        
    @addToClass(AST.InitList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.inits))
        
    @addToClass(AST.Init)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "=\n" + INDENT_TOKEN * (indent + 1) + str(self.name) + "\n" + \
            self.expr.printTree(indent + 1)

    @addToClass(AST.InstructionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.instructions))

    @addToClass(AST.CompoundInstruction)
    def printTree(self, indent=0):
        return ("" if self.declarations is None else self.declarations.printTree(indent + 1)) + \
               self.instructions.printTree(indent + 1)

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "PRINT\n" + self.expr.printTree(indent + 1)

    @addToClass(AST.LabeledInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "LABEL\n" + INDENT_TOKEN * (indent + 1) + str(self.id) + "\n" + \
            self.instr.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "=\n" + INDENT_TOKEN * (indent + 1) + str(self.id) + "\n" + \
            self.expr.printTree(indent + 1)

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "IF\n" + self.condition.printTree(indent + 1) + self.action.printTree(indent + 1) + \
            ("" if self.alternateAction is None else INDENT_TOKEN * indent + "ELSE\n" +
                self.alternateAction.printTree(indent + 1))

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "WHILE\n" + self.condition.printTree(indent + 1) + self.instruction.printTree(indent)

    @addToClass(AST.RepeatInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "REPEAT\n" + self.instructions.printTree(indent + 1) + INDENT_TOKEN * indent + \
            "UNTIL\n" + self.condition.printTree(indent + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "RETURN\n" + self.expression.printTree(indent + 1)

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "CONTINUE\n"

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        return  ("" if self.declarations is None else self.declarations.printTree(indent)) + \
                ("" if self.fundefs is None else self.fundefs.printTree(indent)) + \
                self.instructions.printTree(indent+1)