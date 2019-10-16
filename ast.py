
class Node(object):
    def __init__(self):
        pass

    def pos(self):
        raise NotImplementedError("Must define a pos")

    def end(self):
        raise NotImplementedError("Must define an end")

class Expr:
    def __init__(self):
        super().__init__()

class Func:
    def __init__(self):
        super().__init__()

    def pos(self):
        pass
