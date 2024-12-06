import enum

class RpaException(Exception):
    def __init__(self, message):
        self.message = message
        pass
    pass

class TypeMothod:
    Auto = "auto"
    Ring = "ring"
    pass
