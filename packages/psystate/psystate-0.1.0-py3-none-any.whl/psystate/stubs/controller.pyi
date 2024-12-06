from typing import Callable, Hashable, Literal, Mapping, Sequence

import psychopy.core
import psychopy.visual
from _typeshed import Incomplete

from psystate.events import ExperimentLog as ExperimentLog
from psystate.states import MarkovState as MarkovState
from psystate.utils import lazy_time as lazy_time
from psystate.utils import parse_calls as parse_calls

class ExperimentController:
    state_num: int
    trial: int
    block_trial: int
    block: int
    states: Mapping[Hashable, MarkovState]
    win: psychopy.visual.Window
    start: Hashable
    next: Hashable | None
    t_next: float | None
    current: Hashable
    logger: ExperimentLog
    clock: psychopy.core.Clock
    trial_endstate: Hashable
    N_blocks: int
    K_trials: int
    state_calls: Sequence
    trial_calls: Sequence
    block_calls: Sequence
    state: MarkovState | None
    def __init__(
        self,
        states: Mapping[Hashable, MarkovState],
        window: psychopy.visual.Window,
        start: Hashable,
        logger: ExperimentLog,
        clock: psychopy.core.Clock,
        trial_endstate: Hashable,
        N_blocks: int,
        K_blocktrials: int,
        current: Hashable | None = None,
        state_calls: Mapping[Hashable, Sequence[Callable | tuple[Callable, Mapping]]] = {},
        trial_calls: Sequence[Callable | tuple[Callable, Mapping]] = [],
        block_calls: Sequence[Callable | tuple[Callable, Mapping]] = [],
    ) -> None: ...
    def run_state(self, state: Hashable | None = None) -> None: ...
    def inc_counters(self) -> None: ...
    def run_experiment(self) -> None: ...
    def toggle_pause(self) -> None: ...
    def quit(self) -> None: ...
    def add_loggable(
        self,
        state: Hashable,
        event: Literal["start", "update", "end"],
        key: str,
        value: str | float | int | bool | None = None,
        object: Incomplete | None = None,
        attribute: str | Sequence | None = None,
    ) -> None: ...
