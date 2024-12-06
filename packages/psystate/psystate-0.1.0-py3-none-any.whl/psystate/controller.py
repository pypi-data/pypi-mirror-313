import asyncio
from typing import Callable, Hashable, Literal, Mapping, Sequence, Tuple

import numpy as np
import psychopy.core
import psychopy.visual

from psystate.events import ExperimentLog
from psystate.states import MarkovState
from psystate.utils import parse_calls


class ExperimentController:
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
        state_calls: Mapping[Hashable, Sequence[Callable | Tuple[Callable, Mapping]]] = {},
        trial_calls: Sequence[Callable | Tuple[Callable, Mapping]] = [],
        block_calls: Sequence[Callable | Tuple[Callable, Mapping]] = [],
    ) -> None:
        self.state_num: int = 0
        self.trial: int = 0
        self.block_trial: int = 0
        self.block: int = 0
        self.states = states
        self.win = window
        self.start = start
        self.next = start if current else None
        self.t_next: float | None = None
        self.current: Hashable | None = current if current else start
        self.logger = logger
        self.clock = clock
        self.trial_endstate = trial_endstate
        self.N_blocks = N_blocks
        self.K_trials = K_blocktrials
        self.state_calls = state_calls
        self.trial_calls = trial_calls
        self.block_calls = block_calls
        self.state: MarkovState = None
        self._paused: bool = False
        self._quitting: bool = False
        if "pause" not in self.states:
            self._add_pause()

    def run_state(self, statekey: Hashable | None = None) -> None:
        # If the user manually ran a state, use that state otherwise default to current
        if statekey is None:
            if self.states[self.current] is not self.state:
                raise ValueError("Current state does not match stored state.")
            state = self.state
            statekey = self.current
        else:
            state = self.states[statekey]
            self.state = state
            self.current = statekey
        self.next, dur = state.get_next()

        # Start the state once we have the next one and duration sorted
        state.start_state()
        self.logger.arm(state.loggables, "start")
        flip_t = self.win.flip()  # Flip display
        self._flip_sets(state)
        self.logger.trigger(self.state_num)
        # Record accurate end time and log start, state, target end
        self.t_next = flip_t + dur
        state_logs = {
            "state_start": flip_t,
            "state": statekey,
            "next_state": self.next,
            "target_end": self.t_next,
            "trial_number": self.trial,
        }
        for key, value in state_logs.items():
            self.logger.log(self.state_num, key, value, unique=True)

        self._event_calls(statekey, "start")  # Call any start events

        # Run updates while we wait on the next state
        while self.win.getFutureFlipTime(clock=self.clock) < self.t_next:
            state.update_state()
            self.logger.arm(state.loggables, "update")
            # print(f"Current time is {t}, we want to end at {self.t_next}")
            self.win.flip()
            self._flip_sets(state)
            self.logger.trigger(self.state_num)
            self._event_calls(statekey, "update")  # Call any update events
            if self._check_pause():
                break
            if self._quitting:
                return

        # End the state
        state.end_state()
        self.logger.arm(state.loggables, "end")
        self.win.flip()  # Flip display
        self._flip_sets(state)
        self.logger.trigger(self.state_num)
        self._event_calls(statekey, "end")  # Call any end events

    def inc_counters(self) -> None:
        old_state_num = self.state_num
        self.state_num += 1
        # import ipdb; ipdb.set_trace()  # noqa
        self.logger.log(old_state_num, "block_number", self.block, unique=True)
        self.logger.log(old_state_num, "block_trial", self.block_trial, unique=True)
        if self.current == self.trial_endstate:
            self.logger.log(old_state_num, "trial_end", True, unique=True)
            self.trial += 1
            self.block_trial += 1
            for f, args, kwargs in parse_calls(self.trial_calls):
                f(*args, **kwargs)
            if self.block_trial == self.K_trials:
                self.logger.log(old_state_num, "block_end", True, unique=True)
                self.block += 1
                self.block_trial = 0
                for f, args, kwargs in parse_calls(self.block_calls):
                    f(*args, **kwargs)
                if self.block == self.N_blocks:
                    self.next = None
        else:
            self.logger.log(old_state_num, "trial_end", False, unique=True)
            self.logger.log(old_state_num, "block_end", False, unique=True)
        return

    def run_experiment(self) -> None:
        if self.state is not None:
            raise ValueError("Experiment already running. How did we get here?")
        self.state = self.states[self.current]
        self.run_state(self.current)
        # breakpoint()
        if self.current == self.start:
            self.inc_counters()
        while self.next:
            self.current = self.next
            self.state = self.states[self.current]
            self.run_state(self.current)
            if self._quitting:
                break
            self.inc_counters()
        return

    def toggle_pause(self):
        self._paused = not self._paused
        return

    def quit(self):
        self._quitting = True
        return

    def _add_pause(self):
        self.states["pause"] = MarkovState(
            next="pause",
            dur=np.inf,
        )
        return

    def _check_pause(self):
        """Return True if we should break out of the current state, either to pause or resume."""
        if self.state is self.states["pause"]:
            if not self._paused:  # We are resuming
                self.next = self._resume
                del self._resume
            return not self._paused
        else:
            if self._paused:  # We are pausing, store the planned next state for resume
                self._resume = self.next
                self.next = "pause"
            return self._paused

    def _event_calls(self, state: Hashable, event: Literal["start", "update", "end"]):
        if state in self.state_calls and event in self.state_calls[state]:
            if isinstance(self.state_calls[state][event], Callable):
                self.state_calls[state][event]()
            else:
                for f, args, kwargs in parse_calls(self.state_calls[state][event]):
                    f(*args, **kwargs)

        if "all" in self.state_calls and event in self.state_calls["all"]:
            if isinstance(self.state_calls["all"][event], Callable):
                self.state_calls["all"][event]()
            else:
                for f, args, kwargs in parse_calls(self.state_calls["all"][event]):
                    f(*args, **kwargs)
        return

    def _flip_sets(self, state: MarkovState):
        if len(state.set_onflip) > 0:
            for obj, attr, val in state.set_onflip:
                if asyncio.iscoroutine(val):
                    val = asyncio.run(val)
                setattr(obj, attr, val)
