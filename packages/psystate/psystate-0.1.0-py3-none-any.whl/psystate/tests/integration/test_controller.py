import psychopy.logging as psylog

import psystate.controller as pc
import psystate.events as pe
import psystate.states as ps
import psystate.stimuli as pi
from psystate.tests.fixtures import clock, constructors, stim_kwargs, window  # noqa: F401


class TestIntegratedTask:
    def test_states_controller(self, window, constructors, stim_kwargs, clock):  # noqa: F811
        framerate = 165
        wordstim = pi.StatefulStim(window, constructors, stim_kwargs)
        fixstim = pi.StatefulStim(
            window, {"fixdot": constructors["fixdot"]}, {"fixdot": stim_kwargs["fixdot"]}
        )
        psylog.setDefaultClock(clock)
        states = {
            "words": ps.FrameFlickerStimState(
                next="fixation",
                dur=2.0,
                framerate=framerate,
                window=window,
                stim=wordstim,
                clock=clock,
                frequencies={"w1": 5.156, "w2": 2.012, "fixdot": None},
                loggables=pe.Loggables(
                    start=[pe.FunctionLogItem("state_start", True, clock.getTime)],
                    end=[pe.FunctionLogItem("state_end", True, clock.getTime)],
                ),
                log_updates=True,
            ),
            "fixation": ps.StimulusState(
                next="words",
                dur=0.5,
                window=window,
                stim=fixstim,
                clock=clock,
                loggables=pe.Loggables(
                    start=[pe.FunctionLogItem("state_start", True, clock.getTime)],
                    end=[pe.FunctionLogItem("state_end", True, clock.getTime)],
                ),
            ),
        }

        controller = pc.ExperimentController(
            states=states,
            window=window,
            start="fixation",
            logger=pe.ExperimentLog(),
            clock=clock,
            trial_endstate="words",
            N_blocks=1,
            K_blocktrials=3,
        )

        clock.reset()
        controller.run_experiment()
        print(controller.logger.statesdf)
        controller.logger.contdf.to_csv("testcont.csv")
        print(controller.logger.contdf)
        controller.logger.statesdf.to_csv("teststates.csv")
