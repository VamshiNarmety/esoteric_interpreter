"""
Activation Record (Stack Frame) for function calls.
Stores local variables and parameters for each function invocation.
"""
class ActivationRecord:
    """
    Activation record represents the runtime stack frame for a function call.
    Contains parameters, local variables and return value.
    """
    def __init__(self, name, level, parent=None):
        """
        Initialize an activation record.
        Args:
            name: Function name or scope name
            level: Nesting level (global=0, functions=1+)
            parent: Parent activation record (for lexical scoping)
        """
        self.name = name
        self.level = level
        self.parent = parent
        self.members = {} #local variables and parameters
    
    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members.get(key)
    
    def get(self, key, default=None):
        return self.members.get(key, default)
    
    def __str__(self):
        return f"{self.name} (level: {self.level})\n" + "Members:\n" + "\n".join(f"  {k}: {v}" for k, v in self.members.items())
    
    def __repr__(self):
        return self.__str__()
