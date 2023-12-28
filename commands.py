

class Commands(dict):

    def __init__(self) -> None:
        dict.__init__(self)
    
    def exec(self, command):
        if command == "":
            return self["_default"]()
        available_commands = [c for c in self.keys() if c.startswith(command)]
        if len(available_commands) == 1:
            return self[available_commands[0]]()
        return None

    
if __name__ == "__main__":
    commands = Commands()
    commands["testy"] = lambda: print("testy")
    commands["test1"] = lambda: print("test1111")
    commands["hello"] = lambda: print("hello")
    commands.exec(input("> "))