from collections.abc import Mapping
from typing import TYPE_CHECKING, Hashable

from frozendict import frozendict
from psychopy.visual import TextStim

from psystate.utils import nested_set

if TYPE_CHECKING:
    from psychopy.sound._base import _SoundBase
    from psychopy.visual import BaseVisualStim, Window


class StatefulStim:
    """
    A class for stateful presentation of stimulus. Usually not used directly, but instead passed
    to a state object (from `psystate.states`) to be used in a stateful manner.

    Parameters
    ----------
    win : psychopy.visual.Window
        The window that all stimuli will be drawn to.
    constructors : Mapping
        A dictionary of constructors for the stimuli. Each of the constructor values should be
        a function that returns a `psychopy.visual` stimulus object.
    stim_kwargs : Mapping
        A nested dictionary of kwargs for the constructors.

    Attributes
    ----------
    win : psychopy.visual.Window
        The window that all stimuli will be drawn to.
    constructors : Mapping
        A dictionary of constructors for the stimuli. Each of the constructor values should be
        a function that returns a Psychopy stimulus object.
    stim_kwargs : Mapping
        A nested dictionary of kwargs for the constructors. The structure of the dictionary
        should match the structure of `constructors`.
    states : Mapping
        A dictionary, matching the structure of `constructors`, that keeps track of whether each
        stimulus is currently being shown on the screen or not. If the `states` has no keys
        then the stimuli have not been started yet with `start_stim`, or have been ended with
        `end_stim`.
    stim : Mapping
        A nested dictionary of the Psychopy stimulus objects, once created. This dict will
        be empty if the stimuli are not currently active (before the `start_stim` call or
        after the `end_stim` call), and will be populated with the Psychopy stimulus objects
        once the stimuli start.

    Notes
    -----
    The class handles the creation, updating, and ending of stimuli. The stimuli are created
    using a dictionary of constructors and a nested dictionary of corresponding kwargs. Top-level
    methods for the class will create and draw the stimuli, update whether they are drawn or not,
    and stop drawing the stimuli when needed.

    Additionally, the attribute `states` is a dictionary that keeps track of whether each stimulus
    is currently being shown on the screen or not. This is useful for updating the stimuli within
    a state.

    **StatefulStim objects should persist for the whole life of the experiment**, and only define
    a set of stimuli that will be associated with a state. The class handles creating and
    destroying the actual Psychopy stimulus objects as needed.

    If, after creating the StatefulStim object, the stimuli parameters need to be changed (for
    example before the next time the state runs) then the `stim_kwargs` attribute can be
    directly changed. The next time `start_stim` is called the stimuli will be updated with the
    new parameters.

    Note, however, that once the stimuli are created the `stim_kwargs` attribute should not be
    changed as the stimuli will not be updated with the new parameters. Instead `stim` attribute
    contains a dictionary of the psychopy stimuli objects that can be directly manipulated.
    """

    def __init__(self, window: "Window", constructors: Mapping, stim_kwargs: Mapping):
        self.win = window
        self._constructors = frozendict(constructors)
        self.stim_kwargs = stim_kwargs

        self.states = {}
        for k in self.constructors.keys():
            self.states[k] = False
        self.stim: Mapping[Hashable, BaseVisualStim | _SoundBase] = {}

    @property
    def constructors(self):
        return self._constructors

    @constructors.setter
    def constructors(self, *args, **kwargs):
        raise AttributeError(
            "Cannot set constructors after creating stimulus. "
            "Create a new `StatefulStim` instance instead."
        )

    def start_stim(self):
        """
        Create the stimulus objects using the constructors and kwargs passed.

        Will raise an error if all of the constructors are not represented in `stim_kwargs`, or if
        a window is passed to the stimuli (the window associated with the `StatefulStim` object is
        passed to all constructors with the `win` key).

        The stimuli will be drawn to the screen on the next flip.
        """
        const_keys = self.constructors.keys()
        kw_keys = self.stim_kwargs.keys()
        if not set(const_keys).issubset(set(kw_keys)):
            raise ValueError(
                "Missing constructor kwargs for some constructors: "
                f"{set(const_keys).difference(set(kw_keys))}"
            )
        if any(["win" in self.stim_kwargs[k] for k in kw_keys]):
            raise ValueError("Cannot pass window to StatefulStim as it already has a window.")
        for k in const_keys:
            self.stim[k] = self.constructors[k](win=self.win, **self.stim_kwargs[k])
            self.stim[k].setAutoDraw(True)
            self.states[k] = True

    def update_stim(self, newstates):
        """
        Update attributes of stimuli that are currently being shown on the screen for the next
        flip.

        Parameters
        ----------
        newstates : Mapping
            The dictionary (or any mapping) of the attributes of the stimuli. The keys
            should be a subset of the `constructors` keys, and the values should be a dictionary
            mapping attribute names to their new values.

        Returns
        -------
        list
            A list of tuples of the stimuli that have been changed. The first element of the tuple
            is the key of the stimulus that has been changed, the second element is the
            attribute that has been changed, and the third is the new value.

        """
        updatekeys = list(newstates.keys())
        if not set(updatekeys).issubset(set(self.states)):
            raise ValueError("Mismatched keys between new states and current states.")
        changed = []

        for k in updatekeys:
            currstim = self.stim[k]
            for attrib in newstates[k]:
                newval = newstates[k][attrib]
                if getattr(currstim, attrib) != newval:
                    if attrib == "autoDraw":
                        self.states[k] = newval
                    if isinstance(currstim, TextStim):
                        setattr(currstim, attrib, newval)
                        currstim._needSetText = True
                    changed.append((k, attrib, newval))
        return changed

    def stop_stim(self):
        """
        End the stimuli, stopping them from being drawn and removing them from the `states` and
        `stim` dict attributes.
        """
        allkeys = list(self.stim.keys())
        for k in allkeys:
            self.stim.pop(k).setAutoDraw(False)
            nested_set(self.states, k, False)
