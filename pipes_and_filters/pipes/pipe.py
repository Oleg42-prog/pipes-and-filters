class Pipe:

    def __init__(self, *filters):
        self.filters = filters

    def __call__(self, arg):
        result = arg
        for f in self.filters:
            result = f(result)
        return result
