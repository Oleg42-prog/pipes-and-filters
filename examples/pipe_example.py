from pipes_and_filters import Pipe


def even_step(x):
    print('Even step:', x)
    return x // 2


def odd_step(x):
    print('Odd step:', x)
    return 3 * x + 1


f = Pipe(
    even_step,  # 12 / 2 = 6
    even_step,  # 6 / 2 = 3
    odd_step,   # 3 * 3 + 1 = 10
    even_step,  # 10 / 2 = 5
    odd_step,   # 3 * 5 + 1 = 16
    even_step,  # 16 / 2 = 8
    even_step,  # 8 / 2 = 4
    even_step,  # 4 / 2 = 2
    even_step   # 2 / 2 = 1
)

print('Result:', f(12))
