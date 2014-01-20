#!/usr/bin/python
from collections import defaultdict


class Symbol():
    pass


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class FunctionSymbol():
    def __init__(self, name, type, params):
        self.name = name
        self.type = type
        self.params = params


class SymbolTable(object):
    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.entries = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.entries[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        return self.entries[name]

    def getParentScope(self):
        return self.parent




