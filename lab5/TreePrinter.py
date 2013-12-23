
import AST


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
        return "".join(map(lambda x: x.printTree(level+1), self.expressions))
        
    @addToClass(AST.BinExpr)
    def printTree(self, level=0):
        return "|" * level + self.op + "\n" + \
        self.left.printTree(level+1) + \
        self.right.printTree(level+1)
    
    @addToClass(AST.GroupingExpr)
    def printTree(self, level=0):
        return self.inside.printTree(level)
        
    @addToClass(AST.FunCallExpr)
    def printTree(self, level=0):
        return "|" * level + "FUNCALL\n" + \
        "|" * (level+1) + self.id.__str__() + "\n" + \
        self.inside.printTree(level+1)
        
    @addToClass(AST.Const)
    def printTree(self, level=0):
        return "|" * level + self.value.__str__() + "\n"
        
    @addToClass(AST.Argument)
    def printTree(self, level=0):
        return "|" * level + "ARG " + self.id + "\n"

    @addToClass(AST.ArgumentList)
    def printTree(self,level=0):
        return "".join(map(lambda x: x.printTree(level), self.args))
            
    @addToClass(AST.FunDefList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.fundefs))
    
    @addToClass(AST.FunDef)
    def printTree(self, level=0):
        return "|" * level + "FUNDEF\n" + \
        "|" * (level+1) + self.id.__str__() + "\n" + \
        "|" * (level+1) + "RET " + self.type.__str__() + "\n" + \
        self.args.printTree(level+1) + \
        self.comp_instrs.printTree(level)
         
    @addToClass(AST.DeclarationList)
    def printTree(self, level=0):
        return "|"*level + "DECL\n" + "".join(map(lambda x: x.printTree(level+1), self.declarations))
        
    @addToClass(AST.Declaration)
    def printTree(self, level=0):
        return self.inits.printTree(level)
        
    @addToClass(AST.InitList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.inits))
        
    @addToClass(AST.Init)
    def printTree(self, level=0):
        return "|"*level + "=\n" +\
        "|"*(level+1) + self.id.__str__() + "\n" + \
        self.expr.printTree(level+1)
        
    @addToClass(AST.InstructionList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.instructions))
        
    @addToClass(AST.PrintInstr)
    def printTree(self, level=0):
        return "|" * level + "PRINT\n" + self.expr.printTree(level+1)
    
    @addToClass(AST.LabeledInstr)
    def printTree(self, level=0):
        return "|" * level + "LABEL\n" +\
        "|"*(level+1) + self.id.__str__() + "\n" + \
        self.instr.printTree(level+1)
        
    @addToClass(AST.Assignment)
    def printTree(self, level=0):
        return "|"*level + "=\n" +\
        "|"*(level+1) + self.id.__str__() + "\n" + \
        self.expr.printTree(level+1)
        
    @addToClass(AST.ChoiceInstr)
    def printTree(self, level=0):
        elsestr =  "" if self.elseclause is None else \
        "|"*level + "ELSE\n" + self.elseclause.printTree(level+1)
        
        return "|"*level + "IF\n" + \
        self.ifclause.printTree(level+1) + \
        self.thenclause.printTree(level+1) + \
        elsestr
        
    @addToClass(AST.WhileInstr)
    def printTree(self, level=0):
        return "|"*level + "WHILE\n" +\
        self.condition.printTree(level+1) + \
        self.instruction.printTree(level)
        
    @addToClass(AST.RepeatInstr)
    def printTree(self, level=0):
        return "|"*level + "REPEAT\n" +\
        self.instructions.printTree(level+1) + \
        "|"*level + "UNTIL\n" +\
        self.condition.printTree(level+1)
        
    @addToClass(AST.ReturnInstr)
    def printTree(self, level=0):
        return "|" * level + "RETURN\n" + self.expression.printTree(level+1)
       
    @addToClass(AST.ContinueInstr)
    def printTree(self, level=0):
        return "|"*level + "CONTINUE\n"
        
    @addToClass(AST.BreakInstr)
    def printTree(self, level=0):
        return "|"*level + "BREAK\n"
            
    @addToClass(AST.CompoundInstr)
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