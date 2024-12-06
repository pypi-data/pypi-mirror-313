import asyncio

import pytest  # noqa: F401

import psystate.states as ps
import psystate.stimuli as pi
from psystate.tests.fixtures import clock, constructors, stim_kwargs, window  # noqa: F401


class TestIntegratedTask:
    def test_states_manual_nolog(self, window, constructors, stim_kwargs, clock):  # noqa: F811
        framerate = 165
        wordstim = pi.StatefulStim(window, constructors, stim_kwargs)
        fixstim = pi.StatefulStim(
            window, {"fixdot": constructors["fixdot"]}, {"fixdot": stim_kwargs["fixdot"]}
        )
        states = {
            "words": ps.FrameFlickerStimState(
                next="iti",
                dur=2.0,
                framerate=framerate,
                window=window,
                stim=wordstim,
                clock=clock,
                frequencies={"w1": 5.156, "w2": 2.012, "fixdot": None},
            ),
            "iti": ps.MarkovState(next="fixation", dur=1.0),
            "fixation": ps.StimulusState(
                next="words",
                dur=0.5,
                window=window,
                stim=fixstim,
                clock=clock,
            ),
        }

        def state_setter(state):
            for ob, attr, val in state.set_onflip:
                if asyncio.iscoroutine(val):
                    val = asyncio.run(val)
                setattr(ob, attr, val)

        nstates = 0
        t = 0
        nextstate = "fixation"
        while nstates < 10:
            curr = states[nextstate]
            nextstate, dur = curr.get_next()
            curr.start_state()
            window.flip()
            state_setter(curr)
            t_start = t
            curr._clear_updates()
            while t < (t_start + dur):
                t += 1 / framerate
                curr.update_state()
                window.flip()
                state_setter(curr)
                curr._clear_updates()
            curr.end_state()
            window.flip()
            state_setter(curr)
            curr._clear_updates()
            nstates += 1

    def test_flicker_singlestate_manual_nolog(self, window, constructors, stim_kwargs, clock):  # noqa: F811
        framerate = 165
        wordstim = pi.StatefulStim(window, constructors, stim_kwargs)
        states = {
            "words": ps.FrameFlickerStimState(
                next="iti",
                dur=6.0,
                framerate=framerate,
                window=window,
                stim=wordstim,
                clock=clock,
                strict_freqs="allow",
                frequencies={"w1": 10, "w2": 20, "fixdot": None},
            ),
            "iti": ps.MarkovState(next="words", dur=1.0),
        }

        def state_setter(state):
            for ob, attr, val in state.set_onflip:
                if asyncio.iscoroutine(val):
                    val = asyncio.run(val)
                setattr(ob, attr, val)

        def incword(state):
            if (state.frame_num + 1) % (165 * 2) == 0:
                state.stim.stim["w1"].text += "!"
                state.stim.stim["w2"].text += "!"
            return

        states["words"].update_calls.append((incword, (states["words"],)))
        nstates = 0
        t = 0
        nextstate = "iti"
        while nstates < 4:
            curr = states[nextstate]
            nextstate, dur = curr.get_next()
            curr.start_state()
            window.flip()
            state_setter(curr)
            t_start = t
            curr._clear_updates()
            while t < (t_start + dur):
                t += 1 / framerate
                curr.update_state()
                window.flip()
                state_setter(curr)
                curr._clear_updates()
            curr.end_state()
            window.flip()
            state_setter(curr)
            curr._clear_updates()
            nstates += 1
