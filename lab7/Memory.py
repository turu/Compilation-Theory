class Memory:
    def __init__(self, name): # memory name
        pass

    def has_key(self, name):  # variable name
        pass

    def get(self, name):         # get from memory current value of variable <name>
        pass

    def put(self, name, value):  # puts into memory current value of variable <name>
        pass

class MemoryStack:
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        pass

    def get(self, name):             # get from memory stack current value of variable <name>
        pass

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        pass

    def set(self, name, value): # sets variable <name> to value <value>
        pass

    def push(self, memory): # push memory <memory> onto the stack
        pass

    def pop(self):          # pops the top memory from the stack
        pass

