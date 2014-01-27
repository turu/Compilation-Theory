class Memory:
    def __init__(self, name): # memory name
        self.name = name
        self.dict = {}

    def has_key(self, name):  # variable name
        return name in dict

    def get(self, name):         # get from memory current value of variable <name>
        if self.has_key(name):
            return self.dict[name]
        return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.dict[name] = value


class MemoryStack:
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        if memory is not None:
            self.stack.append(memory)
        else:
            self.stack.append(Memory())

    def get(self, name):             # get from memory stack current value of variable <name>
        for i in range(len(self.stack) - 1, 0):
            if self.stack[i].has_key(name):
                return self.stack[i].get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for i in range(len(self.stack) - 1, 0):
            if self.stack[i].has_key(name):
                self.stack[i].put(name, value)

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()

