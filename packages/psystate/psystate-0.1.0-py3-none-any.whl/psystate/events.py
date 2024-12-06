from __future__ import annotations

import asyncio
import pickle
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from logging import warning
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Hashable, Literal

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from psystate.states import MarkovState

LOGGABLES = {
    "per_state": [
        "state_number",
        "state",
        "next_state",
        "state_start",
        "target_end",
        "state_end",
        "trial_number",
        "block_number",
        "block_trial",
        "trial_end",
        "block_end",
        "condition",
    ],
    "continuous_per_state": [
        "stim1",
        "stim2",
    ],
}


@dataclass
class LogItem:
    """
    A simple dataclass for storing what should be logged and how. Note that regardless of method,
    the value `None` will not be logged.

    Attributes
    ----------
    origin : Literal["attribute", "index", "function", "value"]
        The origin of the value to be logged. Can access an attribute (object must be passed),
        index an object (key and object must be passed), call a function (obj must be passed,
        optionally kwargs), or log a value directly.
    name : str
        The key to log the value under. Will be used as the column name in the log dataframe.
    unique : bool
        Whether the log item is logged only once per state (True) or can possible be logged
        many times within a single state (False).
    timely : bool
        Does this value need to be logged as quickly as possible when the event occurs? Timely
        logs will be processed in parallel when the event is triggered, while non-timely logs will
        be processed in sequence after all timely logs are processed. See Notes for more details.
        Default is False.
    cond : callable | None
        An optional callable that returns a boolean. If the callable returns False, the value will
        not be logged. Will be called every time the value could possibly be logged
        (see `StateLoggables`) if not None. Default is None (always logged).
    obj : object | None
        If the origin is "attribute" or "index", the object to access the attribute of or index
        in to. Ignored otherwise.
    func : callable | None
        If the origin is "function", the function to call. Ignored otherwise.
    key : str | None
        If the origin is "index", the key to index the object with. If the origin is "attribute",
        the attribute to access. Ignored otherwise.
    kwargs : Mapping[str, Any] | None
        If the origin is "function", the kwargs to pass to the function. Ignored otherwise.
    value : str | float | int | bool | None
        If the origin is "value", the value to log every time the item is logged.
        Ignored otherwise.

    Notes
    -----

    The `LogItem` class is a simple container to hold the information needed to log a value. Many
    LogItems can be combined into a `Loggables` object, which can be used to log multiple values
    at once at discrete state-related events.

    Some events need to be logged with the maximum accuracy possible. Normally processing the logs
    in sequence will mean that, if a time is logged via e.g. psychopy.core.Clock.getTime(), the
    times returned by the last log will be offset to the event by the amount of time needed to
    process all the previous logs.

    When a log is marked as "timely", the logger will process all timely logs in parallel when the
    event occurs with priority. For example, if multiple timely logs are set to log the time of a
    flip, the logger will call `getTime()` in parallel for each of these logs to minimize the
    offset to the event. Another example would be to log the subject's eye position at the time of
    the flip, which would require the eye tracker to be polled as quickly as possible after the
    flip.
    """

    name: str
    unique: bool

    def __post_init__(self):
        self._check_fields()
        if self.timely:
            self.get_value = self._timely_get_value
        else:
            self.get_value = self._get_value

    async def _timely_get_value(self):
        return self._get_value()

    def _check_fields(self):
        if not isinstance(self.timely, bool):
            raise ValueError("Timely must be a boolean.")
        if not isinstance(self.name, str):
            raise ValueError("Name must be a string.")
        if self.cond is not None and not callable(self.cond):
            raise ValueError("Condition must be callable that returns `True` or `False`.")
        if not isinstance(self.unique, bool):
            raise ValueError("Unique must be a boolean.")


@dataclass
class AttributeLogItem(LogItem):
    obj: object
    key: str
    timely: bool = False
    cond: Callable | None = None

    def _get_value(self):
        if self.cond is not None:
            if not self.cond():
                return
        if "." in self.key:
            keys = self.key.split(".")
            value = self.obj
            for k in keys:
                value = getattr(value, k)
            return value
        else:
            return getattr(self.obj, self.key)

    def _check_fields(self):
        super()._check_fields()
        if self.obj is None or self.key is None:
            raise ValueError(
                "An object and key must be passed, so that getattr(obj, key) " "can be called."
            )


@dataclass
class IndexLogItem(LogItem):
    obj: object
    idx: str
    timely: bool = False
    cond: Callable | None = None

    def _get_value(self):
        if self.cond is not None:
            if not self.cond():
                return
        return self.obj[self.key]

    def _check_fields(self):
        super()._check_fields()
        if self.obj is None or self.key is None:
            raise ValueError(
                "An object and key must be passed, so that obj[key] " "can be called."
            )


@dataclass
class FunctionLogItem(LogItem):
    func: Callable
    kwargs: Mapping[str, Any] | None = None
    timely: bool = False
    cond: Callable | None = None

    def _get_value(self):
        if self.cond is not None:
            if not self.cond():
                return
        if self.kwargs is None:
            return self.func()
        else:
            return self.func(**self.kwargs)

    def _check_fields(self):
        super()._check_fields()
        if self.func is None:
            raise ValueError("A function must be passed to log a value.")
        if self.kwargs is not None and not isinstance(self.kwargs, Mapping):
            raise ValueError("Kwargs must be a mapping of keyword arguments.")


@dataclass
class ValueLogItem(LogItem):
    value: Hashable
    timely: bool = False
    cond: Callable | None = None

    def _get_value(self):
        if self.cond is not None:
            if not self.cond():
                return
        return self.value

    def _check_fields(self):
        super()._check_fields()
        if self.value is None:
            raise ValueError("A value must be passed to log a value. None is not allowed.")


@dataclass
class UpdateLogItem:
    """
    A simple dataclass for storing updates to a state. Cannot be timely.

    Checks the `log_updates` attribute of the
    state to see what has changed. If the attribute is not empty, will log the
    (key, attribute, value) set, with the key as the name and the (attribute, value) tuple as the
    value. If the attribute is empty, will log the value directly.
    """

    name: str
    state: MarkovState
    unique: bool = False
    cond: Callable | None = None

    def __post_init__(self):
        self._check_fields()
        self.timely = False

    def get_value(self):
        if self.cond is not None:
            if not self.cond():
                return
        if self.state.log_updates:
            return self.state._update_log
        else:
            return None

    def _check_fields(self):
        if self.cond is not None and not callable(self.cond):
            raise ValueError("Condition must be callable that returns `True` or `False`.")
        if not isinstance(self.unique, bool):
            raise ValueError("Unique must be a boolean.")


@dataclass
class Loggables:
    start: list[LogItem] = field(default_factory=list)
    update: list[LogItem] = field(default_factory=list)
    end: list[LogItem] = field(default_factory=list)

    def __post_init__(self):
        self._futures = []
        self._future_names = []
        self._future_uniqe = []
        self._arm_count = 0
        self._trigger_count = 0
        self._event = None

    def merge(self, other: "Loggables"):
        return Loggables(
            start=self.start + other.start,
            update=self.update + other.update,
            end=self.end + other.end,
        )

    def add(self, event: Literal["start", "update", "end"], item: LogItem):
        if event in ["start", "update", "end"]:
            getattr(self, event).append(item)
        else:
            raise ValueError("Event must be one of 'start', 'update', or 'end'.")

    def arm(self, event: Literal["start", "update", "end"]):
        if event in ["start", "update", "end"]:
            self._event = event
            self.armed = True
            self._futures.extend([li.get_value() for li in getattr(self, event) if li.timely])
            self._future_names.extend([li.name for li in getattr(self, event) if li.timely])
            self._future_uniqe.extend([li.unique for li in getattr(self, event) if li.timely])
        else:
            raise ValueError("Event must be one of 'start', 'update', or 'end'.")

    def disarm(self):
        self.armed = False

    async def trigger(self):
        if self.armed:
            self._trigger_count += 1
            values = await asyncio.gather(*self._futures)
            names = self._future_names.copy()
            uniques = self._future_uniqe.copy()
            tags = [None] * len(values)

            for li in getattr(self, self._event):
                if not li.timely:
                    if isinstance(li, UpdateLogItem):
                        items = li.get_value()
                        for item in items:
                            match len(item):
                                case 4:
                                    key, attrib, val, tag = item
                                    tags.append(tag)
                                case 3:
                                    key, attrib, val = item
                                    tags.append(None)
                            values.append(val)
                            names.append(".".join((key, attrib)))
                            uniques.append(False)
                    else:
                        values.append(li.get_value())
                        names.append(li.name)
                        uniques.append(li.unique)
                        tags.append(None)

            self.armed = False
            return names, uniques, values, tags
        else:
            raise ValueError("Loggables must be armed before triggering.")

    @property
    def armed(self):
        return self._armed

    @armed.setter
    def armed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Armed must be a boolean.")
        if value is True:
            self._armed = True
            self._arm_count += 1
        else:
            self._armed = False
            self._futures = []
            self._future_names = []
            self._future_uniqe = []

    @property
    def triggered(self):
        return len(self._futures) != 0

    @property
    def trigger_count(self):
        return self._trigger_count

    @property
    def empty(self):
        return all([len(getattr(self, event)) == 0 for event in ["start", "update", "end"]])

    def __repr__(self):
        return f"Loggables(start={self.start},\nupdate={self.update},\nend={self.end})"


class ExperimentLog:
    """
    Event-driven logger for `ExperimentController`. Supports logging of values on an ad-hoc basis
    as well as from a set of log items in `Loggables`.

    For convenience the logger supports two methods of logging: ad-hoc logging and logging using
    a set of loggable items `Loggables`. The `Loggables` object is a dataclass that contains three
    lists of `LogItem` objects: `start`, `update`, and `end`. These lists contain the `LogItems`
    which are associated with those events. The logger allows all logs related to those events to
    quickly be logged at once.

    Ad-hoc logging is done using the `.log` method, which immediately logs a value for a given
    state number and key. The value can be logged as unique (i.e. only once per state) or
    non-unique (i.e. multiple times within a single state).

    When logging using `Loggables`, the logger must first be armed before a given event (start,
    update, end) and then triggered after the event has occurred. When triggered after being
    armed the logger will log all values in the `Loggables` object at the same time, with the
    objects that are marked as "timely" being logged in parallel to minimize the time offset to
    the event. Attempting to trigger the logger without arming it with loggables will raise an
    error.

    Attributes
    ----------
    armed : bool
        Whether the logger is armed or not. If armed, the logger is ready to log values from
        an already-stored `Loggables` object.
    triggered : bool
        Whether the logger has been triggered after being armed. If triggered, the logger has
        logged all values from the `Loggables` object.
    states : dict
        A dictionary that stores the logged data that needs to be logged at most once per state.
        The keys are the state numbers and the values are dictionaries with the values logged
        for that state so far.
    continuous : dict
        A dictionary that stores the logged data that needs to be logged multiple times within a
        single state. The keys are the state numbers and the values are also dictionaries. Each of
        the inner dicts is a has a key paired with a list. When a new value is logged for the
        state, the list is extended with the new value.
    statesdf : property (pandas.DataFrame)
        Dataframe of the current "per-state" logged data
    contdf : property (pandas.DataFrame)
        Dataframe of the current "continuous" logged data
    """

    def __init__(self):
        self.states = defaultdict(dict)
        self.continuous = defaultdict(lambda: defaultdict(list))
        self._loggables = None

    def arm(self, loggables: Loggables, event: Literal["start", "update", "end"]):
        """
        Arm the logger to prepare for an event that will trigger timely logging. Will prepare the
        loggables to be logged at the moment that the `.trigger()` method is called. Will generate
        coroutines for all timely log items as well.

        Parameters
        ----------
        loggables : Loggables
            Loggables object containing the log items that will be logged at the event.
        event : Literal['start', 'update', 'end']
            The event identity that the loggables are associated with, with respect to the state
            that is currently active.
        """
        if event not in ["start", "update", "end"]:
            raise ValueError("Event must be one of 'start', 'update', or 'end'.")
        if loggables.empty:
            warning("Loggables are empty. No values will be logged.")
        self._loggables = loggables
        self._event = event
        loggables.arm(event)

    def disarm(self):
        """
        Disarm the logger, removing all to-be-logged items without actually logging them.
        """
        self._loggables.disarm()
        del self._loggables

    def trigger(self, state_num: int):
        """
        Immediately log all of the values that have been armed for logging. Will raise an error
        if the `.arm()` method has not been called before this method is called. `.arm()` must be
        called for each time `.trigger()` is called.
        """
        if self._loggables is None:
            raise ValueError("Loggables must be armed before triggering.")
        if self._loggables.armed:
            names, uniques, values, tags = asyncio.run(self._loggables.trigger())
            for name, unique, val, tag in zip(names, uniques, values, tags):
                if val is not None:
                    self.log(state_num, name, val, unique, tag)

    def log(
        self,
        state_number: int,
        key: Hashable,
        value: Hashable,
        unique: bool,
        tag: Hashable | None = None,
    ):
        """
        Log a value for the given state number and key. If the log is unique, i.e. called only
        once in a given state, the value will be stored in the `states` dictionary. If the log is
        not unique, i.e. called multiple times in a given state, the value will be stored in the
        `continuous` dictionary.

        Be warned: if the same key is logged multiple times with `unique=True` the value will be
        overwritten for the given state number.

        Parameters
        ----------
        state_number : int
            The state ID to log the value for.
        key : Hashable
            The key to log the value under.
        value : Hashable
            The value to be logged.
        unique : bool
            Whether the value should be logged only once per state (True) or multiple times
            within a single state (False). Changes the dictionary/dataframe the log is stored in.
        """
        if tag is not None and unique:
            raise ValueError("Tags can only be used with non-unique logs in continuous logging.")
        if state_number not in self.states:
            self.states[state_number]["state_number"] = state_number

        if unique:
            self.states[state_number][key] = value
        else:
            self.continuous[state_number][key].append(value)
            self.continuous[state_number][f"{key}_tag"].append(tag)

    def save(self, fn: str | Path):
        """
        Save logged data to a pickle file. Saves a dictionary with two key: dataframe pairs, one
        for the states (each row is a state) and one for the continuous data (each row is a logged
        value, columns indicate state number and key).


        Parameters
        ----------
        fn : str | Path
            File path to save the data to.
        """
        if isinstance(fn, Path):
            fn = fn.resolve()
        statesdf = self.statesdf()
        contdf = self.contdf()
        with open(fn, "wb") as fw:
            pickle.dump({"continuous": contdf, "states": statesdf}, fw)

    @property
    def statesdf(self):
        """
        Dataframe of the current "per-state" logged data. Each row is a state, with the index
        indicating the state number and the columns indicating the keys logged for that state.

        Returns
        -------
        pandas.DataFrame
        """
        state_nums = list(self.states.keys())
        statesdf = pd.DataFrame.from_records([self.states[sn] for sn in sorted(state_nums)])
        return statesdf.convert_dtypes().set_index("state_number")

    @property
    def contdf(self):
        """
        Dataframe of the current "continuous" logged data. Each row is a logged value, with the
        associated state number and log key stored in columns. The indices are not meaningful,
        unlike `statesdf`.

        Returns
        -------
        pandas.DataFrame
        """
        state_nums = list(self.continuous.keys())
        data = {
            "state_number": np.empty(0, dtype=int),
            "key": np.empty(0, dtype=np.str_),
            "key_number": np.empty(0, dtype=int),
            "value": np.empty(0, dtype=np.str_),
            "tag": np.empty(0, dtype=np.float64),
        }
        for sn in state_nums:
            for key, values in self.continuous[sn].items():
                if "_tag" in key:
                    continue
                currlen = len(values)
                data["state_number"] = np.append(data["state_number"], np.ones(currlen) * sn)
                data["key"] = np.append(data["key"], np.array([key] * currlen))
                data["key_number"] = np.append(data["key_number"], np.arange(currlen))
                data["value"] = np.append(data["value"], values)
                data["tag"] = np.append(data["tag"], self.continuous[sn][f"{key}_tag"])

        contdf = pd.DataFrame.from_dict(data)
        return contdf.convert_dtypes()

    @property
    def armed(self):
        if hasattr(self, "_loggables"):
            return self._loggables.armed
        else:
            return False

    @armed.setter
    def armed(self, value):
        raise AttributeError(
            "Armed is read-only. If you wish to disarm the logger, use the `disarm` method."
        )

    @property
    def triggered(self):
        if hasattr(self, "_loggables"):
            return self._loggables.triggered
        else:
            return False
