import numpy as np
from dataclasses import dataclass

from pybamm import Experiment
from pybamm.experiment.step.steps import Current
import json

from .connection import connect
from .simulation import Simulation
from dandeliion.client.apps.simulation.core.models.export import BPX
from dandeliion.client.tools.misc import unflatten_dict, update_dict


discretizations = {
}

initial_condition_fields = {
    'Initial temperature [K]': 'params.cell.T0',
    'Initial concentration in electrolyte [mol.m-3]': 'params.cell.c0',
    'Initial state of charge': 'params.cell.Z0',
}

sim_params = {
    'x_n': 'params.anode.N',
    'x_s': 'params.separator.N',
    'x_p': 'params.cathode.N',
    'r_n': 'params.anode.M',
    'r_p': 'params.cathode.M',
}


@dataclass
class Simulator:
    """Data class containing informations about simulation server.

    Attributes:
        credential (tuple[str,str]): tuple consisting of the username and password
    """
    # server: str
    credential: tuple[str, str]


@dataclass
class DandeliionExperiment:
    """Class contains information extracted from :class:`Experiment`
    to be used in Dandellion simulations

    Attributes:
        current(dict): dictionary for times and currents
        t_output (list): list of times where outputs should be generated
        t_max (float): final time for simulation run (if not stopped by other criteria)
        V_min (float): minimum voltage allowed in simulation run (stop criterion)
    """
    current: dict
    t_output: list
    t_max: float
    V_min: float


def convertExperiment(
        experiment: Experiment,  # pybamm Experiment
        dt_eval: float,  # sets minimum step size for discretisation
) -> DandeliionExperiment:

    """ Processes :class:`Experiment` and returns :class:`DandeliionExperiment`

    Args:
        experiment (Experiment): A pybamm Experiment
        dt_eval (float): sets minimum step size for discretisation

    Returns:
        DandeliionExperiment: instance of Dandeliion Experiment class containing the
            processed information of the provided pybamm Experiment instance
    """
    # check for termination condition (max time, min voltage opt., others fail)
    V_min = experiment.termination.get('voltage', None)

    t_max = None
    t_output = None
    if 'time' in experiment.termination:
        t_max = experiment.termination['time']  # seconds
        t_output = np.arange(0., t_max, experiment.period).tolist()

    # check for unsupported termination conditions
    if set(experiment.termination.keys()) - {'time', 'voltage'}:
        raise NotImplementedError("Only supported termination conditions are 'time' and 'voltage'")

    # build current input based on Current steps
    current = {'x': [], 'y': []}   # x -> t[s], y -> I[A]
    for step in experiment.steps:
        if step.start_time:
            raise NotImplementedError('Dandeliion does not support experiment steps with start times yet.')
        if not isinstance(step, Current):
            raise NotImplementedError('Dandeliion only supports Current steps for experiments so far.')
        if not step.duration:
            raise NotImplementedError('Dandeliion only supports steps with explicity defined durations.')
        if current['x']:
            last_final = current['x'][-1]
            current['x'].append(last_final + dt_eval)
            current['x'].append(last_final + step.duration)
            current['y'].append(-1. * step.value)
            current['y'].append(-1. * step.value)
        else:
            current['x'].append(0)
            current['x'].append(step.duration - dt_eval)
            current['y'].append(-1. * step.value)
            current['y'].append(-1. * step.value)

    # TODO should we /do we need to extrapolate current to t_max?

    return DandeliionExperiment(
        current=current,
        t_output=t_output,
        V_min=V_min,
        t_max=t_max,
    )


class Solution:
    """Dictionary-style class for the solutions of a simulation run
    returned by :meth:`solve`. Currently contains:

            * 'Time [s]'
            * 'Voltage [V]'
            * 'Current [A]'
    """

    valid_keys = {
        "Time [s]": ("total_voltage", "t(s)"),
        "Voltage [V]": ("total_voltage", "total_voltage(V)"),
        "Current [A]": ("total_current", "total_current(A)"),
    }

    def __init__(self, sim: Simulation):
        """
        Args:
            sim (Simulation): Dandeliion simulation run (has to have finished successfully)
        """
        self._sim = sim
        sim.results  # need to trigger prefetching here since connection may change

    def __str__(self):
        return f"Solution(run {str(self._sim.id)})"

    def __getitem__(self, key: str):
        """Returns the results requested by the key.

        Args:
            key (str): key for results to be returned.

        Returns:
            object: data as requested by provided key
        """
        if key in self.valid_keys:
            return getattr(self._sim.results, self.valid_keys[key][0])[self.valid_keys[key][1]]
        else:
            raise KeyError(f'The following key is not (yet) found in the provided results: {key}')

    def __setitem__(self, key: str, value):
        raise NotImplementedError("This is a read-only dictionary")

    def __len__(self):
        return len(self.valid_keys)

    def __delitem__(self, key):
        raise NotImplementedError("This is a read-only dictionary")

    def clear(self):
        raise NotImplementedError("This is a read-only dictionary")

    def copy(self):
        return self  # nothing to do since read-only anyways

    def has_key(self, k):
        return k in self.valid_keys

    def update(self, *args, **kwargs):
        raise NotImplementedError("This is a read-only dictionary")

    def keys(self):
        return self.valid_keys.keys()

    def values(self):
        return [getattr(self._sim.results, val[0])[val[1]] for key, val in self.valid_keys.items()]

    def items(self):
        # a bit dirty, but since solution is read-only, it works
        return {key: getattr(self._sim.results, val[0])[val[1]] for key, val in self.valid_keys.items()}.items()

    def pop(self, *args):
        raise NotImplementedError("This is a read-only dictionary")

    def __contains__(self, item):
        return item in self.items()

    def __iter__(self):
        for key in self.valid_keys:
            yield key

    @property
    def stop_message(self):
        """
        stop message for simulation run linked to this solution
        """
        return self._sim.stop_message


def solve(
        simulator: Simulator,
        params: str,
        experiment: Experiment,
        var_pts: dict = None,
        model: str = 'DFN',
        initial_condition: dict = None,
        t_output: list = None,
        dt_eval: float = 0.1,
) -> Solution:

    """Method for submitting/running a Dandeliion simulation.

    Args:
        simulator (Simulator): instance of simulator class providing information
            to connect to simulation server
        params (str): path to BPX parameter file
        experiment (Experiment): instance of pybamm Experiment;
            currently only those supported with

            * only :class:`pybamm.experiment.step.steps.Current` steps (or their
              equivalent in str representation) as steps
            * time and/or voltage termination criteria
        var_pts (dict, optional): simulation mesh specified by the following parameters in dictionary (if none or only subset is provided, either user-defined values stored in the bpx or, if not present, default values will be used instead):

            * 'x_n' - Number of nodes in the electrolyte (negative electrode). Default is 30.
            * 'x_s' - Number of nodes in the electrolyte (separator). Default is 20.
            * 'x_p' - Number of nodes in the electrolyte (positive electrode). Default is 30.
            * 'r_n' - Number of nodes in particles (negative electrode). Default is 30.
            * 'r_p' - Number of nodes in particles (positive electrode). Default is 30.
        model (str, optional): name of model to be simulated. Default is 'DFN'. Currently supported models are:

            * 'DFN' - Newman 1D model
        initial_condition (dict, optional): dictionary of additional initial conditions
            (overwrites parameters provided in parameter file if they exist).
            Currently supported initial conditions are:

            * 'Initial temperature [K]'
            * 'Initial concentration in electrolyte [mol.m-3]'
            * 'Initial state of charge'
        t_output (list, optional): list of times to create outputs for. If not provided, then output times derived from experiment will be used (requires time stop criterion to be provided then)
        dt_eval (float, optional): time step used for resolving discontinuities in experiment. Default is 0.1 seconds.

    Returns:
        :class:`Solution`: solution for this simulation run
    """

    connect(
        username=simulator.credential[0],
        password=simulator.credential[1],
        # endpoint=f'{simulator.server}/accounts/',  # TODO
    )

    with open(params) as f:
        data = BPX.import_(data=json.load(f))
    # add/overwrite initial conditions
    if initial_condition:
        update_dict(data, unflatten_dict(
            {initial_condition_fields[field]: value
             for field, value in initial_condition.items()}
        ))

    # add/overwrite simulation params
    if var_pts is not None:
        update_dict(data, unflatten_dict(
            {sim_params[field]: value
             for field, value in var_pts.items()}
        ))

    # set discretisation to FECV (default) if not already set
    if not data['params'].get('discretisation', None):
        data['params']['discretisation'] = 'FECV'

    # convert Experiment into something Dandeliion can use
    experiment = convertExperiment(experiment, dt_eval)

    # set V_min if provided in Experiment
    if experiment.V_min is not None:
        data['params']['cell']['V_min'] = experiment.V_min

    # set charge/discharge current
    data['params']['cell']['current'] = experiment.current

    # set output times and t_max
    if t_output is None and experiment.t_output is None:
        raise ValueError('Either Experiment has to provide time termination condition'
                         + ' or output list t_output has to be exlicitly provided to this function')

    if t_output is None:
        t_output = experiment.t_output
    # set output times
    data['params']['cell']['t_output'] = t_output
    # set maximum discharge time
    if experiment.t_max is not None:
        data['params']['cell']['t_max'] = experiment.t_max
    else:
        data['params']['cell']['t_max'] = t_output[-1]

    data['agree'] = True

    # run simulation
    sim = Simulation(
        data=data,
        # endpoint_results=f'{simulator.server}/results/',  # TODO
    )
    sim.compute()

    return Solution(sim)
