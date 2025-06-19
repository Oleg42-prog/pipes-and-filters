from math import sqrt
from pipes_and_filters import Splitter
from pipes_and_filters import Pipe

# Quadratic equation
# Solve x^2 - x - 6 == 0 equation

params = (1, -1, -6)

f = Pipe(
    lambda x: (x, x[1] * x[1] - 4 * x[0] * x[2]),  # x = (a, b, c)
    lambda y: (y[0], sqrt(y[1]))  # y[0] = (a, b, c); y[1] = D
)

solver = Splitter(
    input_pipe=f,
    outputs_pipes=[
        lambda z: (-z[0][1] + z[1]) / (2 * z[0][0]),  # z[0] = (a, b, c); z[1] = sqrt(D)
        lambda z: (-z[0][1] - z[1]) / (2 * z[0][0]),  # z[0] = (a, b, c); z[1] = sqrt(D)
    ]
)

solve = solver(params)
print(solve)
