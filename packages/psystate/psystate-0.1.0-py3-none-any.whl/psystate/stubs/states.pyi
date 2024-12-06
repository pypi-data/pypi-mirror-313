from collections.abc import Callable, Hashable, Mapping, Sequence
from dataclasses import dataclass
from numbers import Number
from typing import Any, Literal

import psychopy.core
import psychopy.visual

import psystate.events as events
import psystate.stimuli as stimuli

@dataclass
class MarkovState:
    next: Sequence[Hashable] | Hashable
    dur: float | Callable
    transition: None | Callable = ...
    start_calls: list[tuple[Callable, ...]] = ...
    end_calls: list[tuple[Callable, ...]] = ...
    update_calls: list[tuple[Callable, ...]] = ...
    set_onflip: list[tuple[object, str, Any]] = ...
    loggables: events.Loggables = ...
    def __post_init__(self) -> None: ...
    def get_next(self, *args, **kwargs): ...
    def start_state(self) -> None: ...
    def update_state(self, t) -> None: ...
    def end_state(self, t) -> None: ...
    def __init__(
        self,
        next,
        dur,
        transition=...,
        start_calls=...,
        end_calls=...,
        update_calls=...,
        set_onflip=...,
        loggables=...,
    ) -> None: ...

@dataclass
class StimulusState(MarkovState):
    window: psychopy.visual.Window = ...
    stim: stimuli.StatefulStim = ...
    clock: psychopy.core.Clock = ...
    stimon_t = ...
    def __post_init__(self) -> None: ...
    def __init__(
        self,
        next,
        dur,
        transition=...,
        start_calls=...,
        end_calls=...,
        update_calls=...,
        set_onflip=...,
        loggables=...,
        *,
        window,
        stim,
        clock,
    ) -> None: ...

@dataclass
class FlickerStimState(StimulusState):
    frequencies: Mapping[Hashable, Number | Mapping] = ...
    framerate: float = ...
    flicker_handler: Literal["target_t", "frame_count"] = ...
    precompute_flicker_t: float = ...
    strict_freqs: bool = ...
    def __post_init__(self) -> None: ...
    def __init__(
        self,
        next,
        dur,
        transition=...,
        start_calls=...,
        end_calls=...,
        update_calls=...,
        set_onflip=...,
        loggables=...,
        framerate=...,
        flicker_handler=...,
        precompute_flicker_t=...,
        strict_freqs=...,
        *,
        window,
        stim,
        clock,
        frequencies,
    ) -> None: ...

@dataclass
class FrameFlickerStimState(StimulusState):
    frequencies: Mapping[Hashable, Number | Mapping] = ...
    framerate: float = ...
    precompute_flicker_t: float = ...
    state_func: Callable = ...
    strict_freqs: bool | Literal["allow"] = ...
    log_updates: bool = ...
    def __post_init__(self) -> None: ...
    def __init__(
        self,
        next,
        dur,
        transition=...,
        start_calls=...,
        end_calls=...,
        update_calls=...,
        set_onflip=...,
        loggables=...,
        framerate=...,
        precompute_flicker_t=...,
        state_func=...,
        strict_freqs=...,
        log_updates=...,
        *,
        window,
        stim,
        clock,
        frequencies,
    ) -> None: ...
