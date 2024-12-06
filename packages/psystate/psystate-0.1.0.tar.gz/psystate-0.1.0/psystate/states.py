from __future__ import annotations

from collections.abc import Callable, Hashable, Mapping, Sequence
from dataclasses import dataclass, field
from logging import warning
from numbers import Number
from typing import TYPE_CHECKING, Any, Literal, Tuple

import numpy as np
from attridict import AttriDict

import psystate.events as events
import psystate.stimuli as stimuli
import psystate.utils as utils

if TYPE_CHECKING:
    import psychopy.core
    import psychopy.visual


@dataclass
class MarkovState:
    """
    Markov state class to allow for both deterministic and probabilistic state transitions,
    computing current state duration when determining the next state. Useful base class, not for
    direct use.

    Parameters
    ----------
    next : Hashable | Sequence[Hashable]
        Next state(s) to transition to. Can us any identifier that is hashable for the state.
        If a single state, the state is deterministic. If a sequence of multiple states,
        the next state is probabilistic and `transitions` must be provided.
    dur : float | Callable
        Duration of the current state. If a single float, the state has a fixed duration. If a
        callable, the state has a variable duration and the callable must return a duration.
    transition : None | Callable
        Probabilities of transitioning to the next state(s). If `next` is a single state, this
        attribute is not needed. If `next` is a sequence of states, this attribute must be a
        callable that returns an index in `next` based on the probabilities of transitioning.
    start_calls : list[Tuple[Callable, ...]]
        List of functions to call when the state is started. Each element must be a tuple with the
        callable as the first item. An additional sequence after the callable will be used as
        arguments, and a mapping will be used as kwargs. All functions will be called with the time
        as a first argument. Default is an empty list.
    end_calls : list[Tuple[Callable, ...]]
        List of functions to call when the state is ended. Same structrue as `start_calls`.
        Default is an empty list.
    update_calls : list[Tuple[Callable, ...]]
        List of functions to call when the state is updated. Same structrue as `start_calls`.
        Default is an empty list.
    set_onflip : list[Tuple[Object, str, Any]]
        List of attributes to set when the display is flipped. The first element is the object to
        set the attribute on, the second is the attribute name, and the third is the value to set.
        Handled by `ExperimentController` on flip, see `ExperimentController` for details.
        Default is an empty list.
    loggables : events.Loggables
        Loggable items for when the state is stated, updated, and ended. Used by
        `ExperimentController` to log state events. Default is an empty `Loggables` object.
    """

    next: Sequence[Hashable] | Hashable
    dur: float | Callable
    transition: None | Callable = None
    start_calls: list[Tuple[Callable, ...]] = field(default_factory=list)
    end_calls: list[Tuple[Callable, ...]] = field(default_factory=list)
    update_calls: list[Tuple[Callable, ...]] = field(default_factory=list)
    set_onflip: list[Tuple[object, str, Any]] = field(default_factory=list)
    loggables: events.Loggables = field(default_factory=events.Loggables)

    def __post_init__(self):
        if not isinstance(self.next, (Hashable, Sequence)):
            raise TypeError("Next state must be a hashable or sequence of hashables.")
        if not isinstance(self.dur, (Number, Callable)):
            raise TypeError(
                "Duration must be a float or callable function that gives an index" " into `next`."
            )
        if isinstance(self.next, Sequence) and not isinstance(self.next, str):
            if not isinstance(self.transition, Callable):
                raise TypeError(
                    "If `next` is a sequence, `transition` must be a callable function"
                    " that gives an index into `next`."
                )
            if not all(isinstance(i, Hashable) for i in self.next):
                raise TypeError("All elements of `next` must be hashable.")
        if isinstance(self.dur, int):
            self.dur = float(self.dur)
        self._update_log = []
        self.update_calls.insert(0, (self._clear_updates,))

    def get_next(self, *args, **kwargs):
        """
        Get next state from this state. Arguments are passed to the transition function if it is
        callable.

        Returns
        -------
        Hashable
            The hashable identifier of the next state.
        float
            The duration of the current state.
        """
        match (self.next, self.transition):
            case [Sequence(), Callable()]:
                try:
                    next = self.next[self.transition(*args, **kwargs)]  # type: ignore
                except IndexError:
                    raise ValueError("Transition function must return an index in `next`.")
            case [Hashable(), _]:
                next = self.next
        match self.dur:
            case float():
                dur = self.dur
            case Callable():
                dur = self.dur()
        return next, dur

    def start_state(self):
        """
        Initiate state by calling all functions in `start_calls`.
        """
        self._make_calls(self.start_calls)

    def update_state(self):
        """
        Update state by calling all functions in `update_calls`.
        """
        self._make_calls(self.update_calls)

    def end_state(self):
        """
        End state by calling all functions in `end_calls`.
        """
        self._make_calls(self.end_calls)

    def _make_calls(self, event_calls):
        if hasattr(self, "clock"):
            clock = self.clock
        else:
            clock = None
        for f, args, kwargs in utils.parse_calls(event_calls, clock):
            f(*args, **kwargs)

    def _clear_updates(self):
        """
        Clear the updates log.
        """
        self._update_log = []
        self.set_onflip = []


@dataclass
class StimulusState(MarkovState):
    """
    Markov state class for handling stimuli. This class is a base class for handling stimuli in
    Psystate. It can be used for static stimuli which do not update during the state. For more
    complex stimuli involving motion or flicker the `FlickerStimState` class can be used.

    Alternatively, this class can be subclassed to allow for more complex stimuli handling. The
    `_create_stim`, `_update_stim`, and `_end_stim` methods can be overridden to allow for custom
    stimulus handling.

    Parameters
    ----------
    window : psychopy.visual.Window
        The window to draw the stimuli on.
    stim : stimuli.StatefulStim
        The stimulus object to draw at the start of the state. Will stop drawing at the end of the
        state.
    clock : psychopy.core.Clock
        The clock object to get the current time from. This is used to define `stimon_t` when
        the display flips after the state is started.

    Attributes
    ----------
    stimon_t : float
        The time at which the stimulus was turned on. This is set when the state is started and
        the stimulus is created. Starts as None and is set to the current time when the stimulus
        is created. After state end it is set to None.
    """

    window: psychopy.visual.Window = field(kw_only=True)
    stim: stimuli.StatefulStim = field(kw_only=True)
    clock: psychopy.core.Clock = field(kw_only=True)

    def __post_init__(self):
        self.start_calls.append(self._create_stim)
        self.update_calls.append(self._update_stim)
        self.end_calls.append(self._end_stim)
        self.stimon_t = None
        if self.loggables.empty:
            self.loggables.add(
                "start",
                events.FunctionLogItem("on_t", True, timely=True, func=self.clock.getTime),
            )
            self.loggables.add(
                "end",
                events.FunctionLogItem("off_t", True, timely=True, func=self.clock.getTime),
            )

        super().__post_init__()

    def _create_stim(self):
        """
        Internal function to call when the stimulus is created. Should always call the `start_stim`
        method of `stim` and set the `stimon_t` attribute to the current time.
        """
        self.stim.start_stim()
        self.set_onflip.append((self, "stimon_t", utils.lazy_time(self.clock)))

    def _update_stim(self):
        """
        Placeholder function. Classes that inherit from this class should override this method to
        allow for updating stimuli during the state. Note that if you want to call _update_stim with
        additional arguments, you can do so by adding them to the update_calls list in the state
        post_init method.
        """
        pass

    def _end_stim(self):
        """
        Internal function to call when the stimulus is ended. Should always call the `end_stim`
        method of `stim` and set the `stimon_t` attribute to None.
        """
        self.stim.stop_stim()
        self.stimon_t = None


@dataclass
class FrameFlickerStimState(StimulusState):
    frequencies: Mapping[Hashable, Number | Mapping] = field(kw_only=True)
    framerate: float = 60.0
    precompute_flicker_t: float = 300.0
    state_func: Callable = utils.target_opacity
    strict_freqs: bool | Literal["allow"] = True
    log_updates: bool = False

    def __post_init__(self):
        if self.strict_freqs not in (True, False, "allow"):
            raise ValueError("`strict_freqs` must be a boolean or 'allow'.")
        self.frequencies = AttriDict(self.frequencies)
        super().__post_init__()

        self.start_calls.append(self._compute_flicker)
        if self.log_updates:
            self.loggables.add("update", events.UpdateLogItem(name="state_update", state=self))

    def _create_stim(self):
        """Same as StimulusState._create_stim but also assigns the `flicker_handler` attribute
        indicating whether frame number or target switch times are used to flicker the stimulus."""
        self.frame_num = 0
        super()._create_stim()

    def _compute_flicker(self):
        """
        Computes the target switches (frames or times) for flickering the stimulus.
        """
        if self.frame_num is None:
            raise AttributeError("Stimulus must be created before computing flicker.")

        # Get keys of all possible constructors and iterate over them to check if they need targets
        switch_targets = {}
        switch_opacities = {}
        for key in self.stim.constructors:
            try:  # Handle cases where the frequency is not set
                f = self.frequencies[key]
                if f in (None, 0):  # If the frequency is None/0, set targets to None (no flicker)
                    switch_targets[key] = None
                else:  # Otherwise, compute the target switch times from the frequency
                    closef = self._nearest_f(f)
                    switch_targets[key] = utils.target_frames(
                        closef, self.framerate, self.precompute_flicker_t
                    )
                    switch_opacities[key] = self.state_func(switch_targets[key])

            except KeyError:
                switch_targets[key] = None
        self.target_switches = switch_targets
        self.target_opacities = switch_opacities

    def _update_stim(self):
        if self.frame_num is None:
            raise AttributeError("Stimuli must be created before updating.")
        if not hasattr(self, "target_switches"):
            raise AttributeError("Flicker targets must be computed before updating.")

        # Create a new state dictionary to update the stimulus, and define our checking method
        newstates = {}
        for key in self.target_switches:
            # Get the targets for this stimulus
            keytargets = self.target_switches[key]
            if keytargets is None:
                continue  # don't bother for non-flickering stimuli
            keyopacities = self.target_opacities[key]
            frame_num = self.frame_num
            # If we're at a point where we need to switch the stimulus,
            if frame_num in keytargets:
                idx = np.flatnonzero(keytargets == frame_num)[0]
                newstates[key] = {"opacity": keyopacities[idx]}

        changed = self.stim.update_stim(newstates)
        changed = [(*v, self.frame_num) for v in changed]
        self.frame_num += 1
        self._update_log.extend(changed)

    def _nearest_f(self, target):
        """
        Get the nearest possible square-wave flicker frequency to a target f given an underlying
        framerate, assuming an equal number of on/off cycles.

        If the frequency cannot be achieved exactly, an error will be raised if strict_freqs is
        true, or a warning will be emitted and the nearest possible frequency will be returned if
        strict_freqs is false.
        """
        framerate = self.framerate
        f, err = utils.nearest_f_squarewave(target, framerate)
        match err, self.strict_freqs:
            case 0.0, _:
                return f
            case _, True:
                if np.abs(f - target) <= 1e-3:
                    return f
                raise ValueError(
                    f"Frequency must be a divisor of 1/2 the frame rate. "
                    f"Actual frequency: {target:0.3f}, nearest possible: {f:0.3f}, "
                    f"frame rate: {framerate:0.3f}."
                )
            case _, False:
                if np.abs(err) < 0.05:
                    warning(
                        "WARNING: Frequency is not a divisor of 1/2 the frame rate. Using the"
                        f" nearest possible frequency: {f:0.3f} instead of {target:0.3f}."
                    )
                    return f
                else:
                    raise ValueError(
                        f"Frequency must be a divisor of 1/2 the frame rate. "
                        f"Actual frequency: {target:0.3f}, nearest possible: {f:0.3f}, "
                        f"frame rate: {framerate:0.3f}. `strict_freqs` is set to False, but"
                        " cowardly refusing to use the nearest frequency since it is > 5% off."
                    )
            case _, "allow":
                warning(
                    "WARNING: Frequency is not a divisor of 1/2 the frame rate. Using the"
                    f" nearest possible frequency: {f:0.3f} instead of {target:0.3f}."
                    " `strict_freqs` is set to 'allow', so any deviation is acceptable."
                )
                return f
