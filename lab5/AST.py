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


class GroupedExpression(Node):
    def __init__(self, interior):
        self.interior = interior

class FunctionExpression(Node):
    def __init__(self, retType, name, args, body):
        self.retType = retType
        self.name = name
        self.args = args
        self.body = body


class FunctionExpressionList(Node):
    def __init__(self):
        self.fundefs = []

    def addFunction(self, fundef):
        self.fundefs.append(fundef)


class DeclarationList(Node):
    def __init__(self):
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class InvocationExpression(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

   
class Argument(Node):
    def __init__(self, type, name):
        self.type = type
        self.name = name


class ArgumentList(Node):
    def __init__(self):
        self.argList = []
        
    def addArgument(self, arg):
        self.argList.append(arg)


class InitList(Node):
    def __init__(self):
        self.inits = []
        
    def addInit(self, init):
        self.inits.append(init)


class Init(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class InstructionList(Node):
    def __init__(self):
        self.instructions = []
    
    def addInstruction(self, instr):
        self.instructions.append(instr)


class PrintInstruction(Node):
    def __init__(self, expr):
        self.expr = expr


class LabeledInstruction(Node):
    def __init__(self, id, instr):
        self.id = id
        self.instr = instr

class Assignment(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        
class ChoiceInstruction(Node):
    def __init__(self, ifclause, thenclause, elseclause=None):
        self.ifclause = ifclause
        self.thenclause = thenclause
        self.elseclause = elseclause

class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        
class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition
        
class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression
        
class ContinueInstruction(Node):
    pass
    
class BreakInstruction(Node):
    pass

class CompoundInstruction(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions
            
class Program(Node):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions
