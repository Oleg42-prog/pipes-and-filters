class Splitter:

    def __init__(self, input_pipe, outputs_pipes):
        self.input_pipe = input_pipe
        self.outputs_pipes = outputs_pipes

    def __call__(self, *args):
        result = self.input_pipe(*args)
        split_results = []
        for output_pipe in self.outputs_pipes:
            split_results.append(output_pipe(result))
        return split_results
