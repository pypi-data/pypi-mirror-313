from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Callable

import numpy as np

if TYPE_CHECKING:
    import psychopy.core


def nested_iteritems(d):
    for k, v in d.items():
        if isinstance(v, dict):
            for subk, v in nested_iteritems(v):
                yield (k, *subk), v
        else:
            yield (k,), v


def nested_deepkeys(d):
    for k, v in d.items():
        if isinstance(v, dict):
            for subk in nested_deepkeys(v):
                yield (k, *subk)
        else:
            yield (k,)


def nested_keys(d, keys=[]):
    for k, v in d.items():
        if type(v) is dict:
            yield (*keys, k)
            yield from nested_keys(v, keys=[*keys, k])
        else:
            yield (*keys, k)


def maxdepth_keys(d, depth=10, deepest=False):
    """Return all keys in a nested dictionary up to a maximum depth. Not only those keys not pointing to dicts.
    If depth is negative, return keys up to -N length relative to the maximum depth of the dict."""
    allkeys = list(nested_deepkeys(d)) if deepest else list(nested_keys(d))
    if depth < 0:
        maxd = max(map(len, allkeys))
        return [k for k in allkeys if len(k) <= maxd + depth]
    depth += 1
    return [k for k in allkeys if len(k) <= depth]


def nested_get(d, keys):
    for key in keys[:-1]:
        d = d[key]
    return d[keys[-1]]


def nested_set(d, keys, value):
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def nested_pop(d, keys):
    for key in keys[:-1]:
        d = d[key]
    return d.pop(keys[-1])


async def lazy_time(clock):
    return clock.getTime()


def parse_calls(call_list, clock: psychopy.core.Clock | None = None):
    """
    Parse a list of calls to be made during a state. Calls can either be a single callable or a
    tuple of (callable, [args], [kwargs]), where the arg and kwargs are optional. A tuple element
    will be inferred to be [args] if it is a sequence and [kwargs] if it is a mapping.

    Certain key values are reserved in [args] and [kwargs] specific to `psystate`:
    - [args] : "t" if `clock` is not None, the current clock time will be passed with the key `t`.
    - [kwargs] : {"get": Tuple[object, attribute, kw]}, will attempt to add the attribute of the
        object to the kwargs with the key `kw`.


    Parameters
    ----------
    call_list : list[Tuple[Callable, ...]]
        List of functions to call during the state.
    index : int
        Index of the call list to parse.

    Returns
    -------
    Callable
        The callable function to be called.
    Tuple
        The arguments to be passed to the callable.
    Mapping
        The keyword arguments to be passed to the callable.
    """
    for call in call_list:
        if not isinstance(call, Sequence):
            if isinstance(call, Callable):
                yield call, (), {}
                continue
            else:
                raise TypeError("Call list must be a list-like.")
        sequences = tuple(filter(lambda x: isinstance(x, Sequence), call))
        mappings = tuple(filter(lambda x: isinstance(x, Mapping), call))
        f = call[0]
        if len(sequences) > 0:
            args = list(sequences[0])
            if len(sequences) > 1:
                raise ValueError("Only one sequence of arguments is allowed.")
        else:
            args = ()

        if len(mappings) > 0:
            kwargs = dict(mappings[0])
            if len(mappings) > 1:
                raise ValueError("Only one mapping of keyword arguments is allowed.")
        else:
            kwargs = {}

        if clock is not None:
            for idx, arg in enumerate(args):
                if isinstance(arg, str) and arg == "t":
                    args.pop(idx)
                    kwargs["t"] = clock.getTime()
        yield f, args, kwargs


def nearest_f_squarewave(target: float, framerate: float) -> float:
    """
    Get the nearest possible square-wave flicker frequency to a target f given an underlying
    framerate, assuming an equal number of on/off cycles.

    Note that in practice you are constrained by *double* the target frame rate, as you need to
    switch twice per cycle.

    Parameters
    ----------
    target : float
        The target flicker frame rate in Hz.
    framerate : float
        The framerate of the underlying system in Hz.

    Returns
    -------
    float
        The closest possible frequency to the target given the underlying framerate.
    float
        The relative error between the target and the closest possible frequency.
    """
    switchf = 2 * target
    frameint = 1 / framerate
    switchint = 1 / switchf
    mult = np.round(switchint / frameint)
    nearest = (1 / (mult * frameint)) / 2
    return nearest, (target - nearest) / target


def target_frames(f: float, framerate: float, precompute_t: float) -> np.ndarray:
    """
    Generate target frame counts to switch a square-wave flicker at a given frequency.

    Parameters
    ----------
    f : float
        The frequency to flicker at in Hz. **Will not be checked for validity!**
    framerate : float
        Refresh rate of the display in Hz.
    precompute_t : float
        Time to compute flickers for, in seconds. Will be rounded to the nearest frame.

    Returns
    -------
    np.ndarray
        One-dimensional array of integer frame counts to switch state at.
    """
    frames_per_halfcycle = int(framerate / (2 * f))
    return np.arange(
        frames_per_halfcycle - 1,  # Start at the end of the first half-cycle (minus 1 for index)
        frames_per_halfcycle + precompute_t * framerate,  # Go until the end of the precompute time
        frames_per_halfcycle,  # Step by the number of frames per half-cycle
        dtype=int,
    )


def target_opacity(frames):
    """
    Compute a square-wave flicker target opacity (0 or 1) for a given set of frame switches.

    Parameters
    ----------
    frames : numpy.ndarray
        A one-dimensional array of frame indices to switch state at.

    Returns
    -------
    numpy.ndarray
        A one-dimensional array of the same shape as `frames` with opacity values to set.
    """
    opac = np.zeros_like(frames)
    opac[1::2] = 1.0
    return opac


def flip_state(t, target_t, keymask, framerate):
    close_enough = np.isclose(t, target_t, rtol=0.0, atol=1 / (2 * framerate) - 1e-6)
    past_t = t > target_t
    goodclose = (close_enough & keymask) | (past_t & keymask)
    # breakpoint()
    if np.any(goodclose):
        ts_idx = np.argwhere(goodclose).flatten()[-1]
        keymask[ts_idx] = False
        return True, keymask
    return False, keymask
