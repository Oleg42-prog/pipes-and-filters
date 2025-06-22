from pipes_and_filters.pipes.pipe import Pipe
from pipes_and_filters.pipes.splitter import Splitter
from pipes_and_filters.pipeline import Pipeline
from pipes_and_filters.flow import Flow
from pipes_and_filters.utils import identity


def test_pipe():

    f = Pipe(
        lambda x: x + 3,
        lambda x: x * 2,
        lambda x: x - 4,
        lambda x: x / 2
    )

    assert f(5) == 6


def test_splitter():

    f = Pipe(
        lambda x: 3 * x + 1,
        lambda x: x // 2,
    )

    f1 = Pipe(
        lambda x: x // 2,
        lambda x: x // 2
    )

    f2 = Pipe(
        lambda x: 3 * x + 1,
        lambda x: 3 * x + 1
    )

    actual = Splitter(
        input_pipe=f,
        outputs_pipes=[f1, f2]
    )

    assert actual(5) == [2, 76]


def test_pipeline():

    pipeline = Pipeline(
        source=range(10),
        pipe=lambda x: x ** 2
    )

    expected = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    assert list(pipeline()) == expected


def test_flow():

    flow = Flow(
        source=range(1, 6),
        splitter=Splitter(
            input_pipe=identity,
            outputs_pipes=[
                lambda x: x,
                lambda x: x ** 2
            ]
        ),
        sink=lambda x, y: x / y
    )

    assert list(flow()) == [1, 2/4, 3/9, 4/16, 5/25]
