from math import sqrt
from pipes_and_filters.flow import Flow
from pipes_and_filters.pipes.splitter import Splitter
from pipes_and_filters.utils import identity


def std_dev(scores):
    mean = sum(scores) / len(scores)
    return sqrt(sum((x - mean)**2 for x in scores) / len(scores))


def report(avg, max_score, min_score, score_range, std):
    return f"Mean: {avg:.1f} | Max: {max_score} | Min: {min_score} | Range: {score_range} | Std Dev: {std:.1f}"


student_scores = [
    [85, 92, 78, 96, 88],  # Студент 1
    [75, 68, 82, 91, 79],  # Студент 2
    [95, 85, 93, 87, 91],  # Студент 3
    [62, 74, 69, 83, 76],  # Студент 4
    [88, 85, 79, 92, 86],  # Студент 5
]

stats_splitter = Splitter(
    input_pipe=identity,
    outputs_pipes=[
        lambda scores: sum(scores) / len(scores),
        max,
        min,
        lambda scores: max(scores) - min(scores),
        std_dev
    ]
)

flow = Flow(
    source=student_scores,
    splitter=stats_splitter,
    sink=report
)

for i, report in enumerate(flow(), 1):
    print(f"Student {i}: {report}")
