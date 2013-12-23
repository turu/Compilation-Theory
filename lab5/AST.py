class Node(object):
    def __str__(self):
        return self.printTree()


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    pass


class BinExpr(Node):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs


class ExpressionList(Node):
    def __init__(self):
        self.expressionList = []

    def addExpression(self, expr):
        self.expressionList.append(expr)


class GroupingExpr(Node):
    def __init__(self, inside):
        self.inside = inside


class InvocationExpression(Node):
    def __init__(self, id, inside):
        self.id = id
        self.inside = inside

   
class Argument(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id


class ArgumentList(Node):
    def __init__(self):
        self.args = []
        
    def addArgument(self, arg):
        self.args.append(arg)


class FunctionExpression(Node):
    def __init__(self, type, id, args, comp_instrs):
        self.type = type
        self.id = id
        self.args = args
        self.comp_instrs = comp_instrs


class FunDefList(Node):
    def __init__(self):
        self.fundefs = []

    def addDef(self, fundef):
        self.fundefs.append(fundef)


class DeclarationList(Node):
    def __init__(self):
        self.declarations = []
        
    def addDeclaration(self, decl):
        self.declarations.append(decl)
        
class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits
        
class InitList(Node):
    def __init__(self):
        self.inits = []
        
    def addInit(self, init):
        self.inits.append(init)
        
class Init(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class InstructionList(Node):
    def __init__(self):
        self.instructions = []
    
    def addInstr(self, instr):
        self.instructions.append(instr)
        
class Instruction(Node):
    pass
    
class PrintInstr(Instruction):
    def __init__(self, expr):
        self.expr = expr
        
class LabeledInstr(Instruction):
    def __init__(self, id, instr):
        self.id = id
        self.instr = instr

class Assignment(Instruction):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        
class ChoiceInstr(Instruction):
    def __init__(self, ifclause, thenclause, elseclause=None):
        self.ifclause = ifclause
        self.thenclause = thenclause
        self.elseclause = elseclause

class WhileInstr(Instruction):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        
class RepeatInstr(Instruction):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition
        
class ReturnInstr(Instruction):
    def __init__(self, expression):
        self.expression = expression
        
class ContinueInstr(Instruction):
    pass
    
class BreakInstr(Instruction):
    pass

class CompoundInstr(Instruction):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions
            
class Program(Node):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions
