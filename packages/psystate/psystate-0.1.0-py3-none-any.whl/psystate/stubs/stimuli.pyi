from collections.abc import Mapping
from typing import Hashable

from psychopy.visual import BaseVisualStim as BaseVisualStim
from psychopy.visual import Window as Window

from psystate.states import MarkovState
from psystate.utils import nested_deepkeys as nested_deepkeys
from psystate.utils import nested_get as nested_get
from psystate.utils import nested_set as nested_set

class StatefulStim:
    win: Window
    stim_kwargs: Mapping
    states: Mapping[Hashable, MarkovState]
    stim: Mapping[Hashable, BaseVisualStim]
    def __init__(self, window: Window, constructors: Mapping, stim_kwargs: Mapping) -> None: ...
    @property
    def constructors(self): ...
    @constructors.setter
    def constructors(self, *args, **kwargs) -> None: ...
    def start_stim(self) -> None: ...
    def update_stim(self, newstates): ...
    def stop_stim(self) -> None: ...
