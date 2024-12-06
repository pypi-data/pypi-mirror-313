import psychopy.visual as pv
import psyquartz as pq
import pytest


@pytest.fixture
def window():
    win = pv.Window(
        screen=0,
        size=(800, 600),
        fullscr=False,
        winType="pyglet",
        allowStencil=False,
        monitor="testMonitor",
        color=[0, 0, 0],
        colorSpace="rgb",
        units="deg",
        checkTiming=False,
    )
    win.flip()
    return win


@pytest.fixture
def constructors():
    return {
        "w1": pv.TextStim,
        "w2": pv.TextStim,
        "fixdot": pv.ShapeStim,
    }


@pytest.fixture
def stim_kwargs():
    return {
        "w1": {"text": "hello", "height": 2.0, "pos": (-3, 0)},
        "w2": {"text": "world", "height": 2.0, "pos": (3, 0)},
        "fixdot": {"vertices": "circle", "anchor": "center", "size": (0.05, 0.05)},
    }


@pytest.fixture
def clock():
    return pq.Clock()
