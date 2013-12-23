import AST

INDENT_TOKEN = "| "


def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, level=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.ExpressionList)
    def printTree(self,level=0):
        return "".join(map(lambda x: x.printTree(level+1), self.expressionList))
        
    @addToClass(AST.BinExpr)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + self.op + "\n" + \
        self.lhs.printTree(level+1) + \
        self.rhs.printTree(level+1)

    @addToClass(AST.GroupedExpression)
    def printTree(self, level=0):
        return self.interior.printTree(level)
        
    @addToClass(AST.InvocationExpression)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + "FUNCALL\n" + \
        INDENT_TOKEN * (level+1) + str(self.name) + "\n" + \
        self.args.printTree(level+1)
        
    @addToClass(AST.Const)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + str(self.value) + "\n"
        
    @addToClass(AST.Argument)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + "ARG " + self.name + "\n"

    @addToClass(AST.ArgumentList)
    def printTree(self,level=0):
        return "".join(map(lambda x: x.printTree(level), self.argList))
            
    @addToClass(AST.FunctionExpressionList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.fundefs))
    
    @addToClass(AST.FunctionExpression)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + "FUNDEF\n" + \
        INDENT_TOKEN * (level+1) + str(self.name) + "\n" + \
        INDENT_TOKEN * (level+1) + "RET " + str(self.retType) + "\n" + \
        self.args.printTree(level+1) + \
        self.body.printTree(level)
         
    @addToClass(AST.DeclarationList)
    def printTree(self, level=0):
        return INDENT_TOKEN*level + "DECL\n" + "".join(map(lambda x: x.printTree(level+1), self.declarations))
        
    @addToClass(AST.Declaration)
    def printTree(self, level=0):
        return self.inits.printTree(level)
        
    @addToClass(AST.InitList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.inits))
        
    @addToClass(AST.Init)
    def printTree(self, level=0):
        return INDENT_TOKEN*level + "=\n" +\
        INDENT_TOKEN*(level+1) + str(self.name) + "\n" + \
        self.expr.printTree(level+1)
        
    @addToClass(AST.InstructionList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.instructions))
        
    @addToClass(AST.PrintInstruction)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + "PRINT\n" + self.expr.printTree(level+1)
    
    @addToClass(AST.LabeledInstruction)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + "LABEL\n" +\
        INDENT_TOKEN*(level+1) + str(self.id) + "\n" + \
        self.instr.printTree(level+1)
        
    @addToClass(AST.Assignment)
    def printTree(self, level=0):
        return INDENT_TOKEN*level + "=\n" +\
        INDENT_TOKEN*(level+1) + str(self.id) + "\n" + \
        self.expr.printTree(level+1)
        
    @addToClass(AST.ChoiceInstruction)
    def printTree(self, level=0):
        elsestr =  "" if self.elseclause is None else \
        INDENT_TOKEN*level + "ELSE\n" + self.elseclause.printTree(level+1)
        
        return INDENT_TOKEN*level + "IF\n" + \
        self.ifclause.printTree(level+1) + \
        self.thenclause.printTree(level+1) + \
        elsestr
        
    @addToClass(AST.WhileInstruction)
    def printTree(self, level=0):
        return INDENT_TOKEN*level + "WHILE\n" +\
        self.condition.printTree(level+1) + \
        self.instruction.printTree(level)
        
    @addToClass(AST.RepeatInstruction)
    def printTree(self, level=0):
        return INDENT_TOKEN*level + "REPEAT\n" +\
        self.instructions.printTree(level+1) + \
        INDENT_TOKEN*level + "UNTIL\n" +\
        self.condition.printTree(level+1)
        
    @addToClass(AST.ReturnInstruction)
    def printTree(self, level=0):
        return INDENT_TOKEN * level + "RETURN\n" + self.expression.printTree(level+1)
       
    @addToClass(AST.ContinueInstruction)
    def printTree(self, level=0):
        return INDENT_TOKEN*level + "CONTINUE\n"
        
    @addToClass(AST.BreakInstruction)
    def printTree(self, level=0):
        return INDENT_TOKEN*level + "BREAK\n"
            
    @addToClass(AST.CompoundInstruction)
    def printTree(self, level=0):
        declstr = "" if self.declarations is None else self.declarations.printTree(level+1)
        return declstr + \
        self.instructions.printTree(level+1)
    
    @addToClass(AST.Program)
    def printTree(self,level=0):
        declstr = "" if self.declarations is None else self.declarations.printTree(level)
        fundefstr = "" if self.fundefs is None else self.fundefs.printTree(level)
        return  declstr + \
        fundefstr + \
        self.instructions.printTree(level+1)