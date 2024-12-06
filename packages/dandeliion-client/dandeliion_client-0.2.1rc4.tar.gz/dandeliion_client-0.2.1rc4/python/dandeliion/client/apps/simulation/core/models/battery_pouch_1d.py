from .model import Model
from .results import ZIPFileArchive, CSVFile
from .plot import Plot, SequencePlot
from . import battery_model
from .battery_model import Battery_Model
from .fields import (
    IntegerField,
    FloatField,
    FunctionField,
    MinValueValidator,
    MaxValueValidator,
    ValidationError,
)
from dandeliion.client.tools.misc import get_dict
import math

# This classes are used internally, if it is resusable, it should be best moved into its own module


class _Contact(Model):

    # TODO decimal or float fields? correct decimal places? do we need new validator to exclude 0?

    # Electrode section

    N = IntegerField(initial=20, label="Number of nodes in the electrolyte",
                     validators=[MinValueValidator(2), MaxValueValidator(1000)])
    L = FloatField(label="Electrode thickness [μm]",
                   validators=[MinValueValidator(0)])
    el = FloatField(label="Volume fraction of electrolyte (porosity)",
                    validators=[MinValueValidator(0), MaxValueValidator(1)])
    B = FloatField(label="Permeability factor of electrolyte (transport efficiency)",
                   validators=[MinValueValidator(0)])

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['L'] *= 1e6  # scale back into [um] used inside model
        return representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'L' in data and data['L']:
            data['L'] *= 1e-6  # [m]
        return data


class _Electrode(_Contact):

    # TODO decimal or float fields? correct decimal places? do we need new validator to exclude 0?

    class Meta:
        plots = {
            'diffusivity': Plot(
                reqs=['diffusivity'],
                data=[
                    {
                        'field': 'diffusivity.eval',
                        'type': 'Line'
                    },
                ],
                layout={
                    'title': 'Diffusivity in Electrode',
                    'xaxis_title': 'Electrode stoichiometry',
                    'yaxis_title': 'D<sub>s</sub> (m<sup>2</sup>/s)',
                    'yaxis_type': 'log',
                }
            ),
            'eqm_potential': Plot(
                reqs=['eqm_potential'],
                data=[
                    {
                        'field': 'eqm_potential.eval',
                        'type': 'Line'
                    },
                ],
                layout={
                    'title': 'Equilibrium potential in Electrode',
                    'xaxis_title': 'Electrode stoichiometry',
                    'yaxis_title': 'U<sub>eq</sub> (V)',
                }
            ),
        }

    # Electrode section

    M = IntegerField(initial=20, label="Number of nodes in particles",
                     validators=[MinValueValidator(2), MaxValueValidator(1000)])
    R = FloatField(label="Particle radius [μm]",
                   validators=[MinValueValidator(0)])
    # to 1e-6 or rescale in get_params
    bet = FloatField(label="Surface area per unit volume [m<sup>-1</sup>]",
                     validators=[MinValueValidator(0)])
    sigma_s = FloatField(label="Electric conductivity of particles [S&middot;m<sup>-1</sup>]",
                         validators=[MinValueValidator(0)])
    E_act_Ds = FloatField(label="Activation energy of diffusion coefficient [J&middot;mol<sup>-1</sup>]",
                          validators=[MinValueValidator(0)])
    E_act_k0 = FloatField(label="Activation energy of reaction rate [J&middot;mol<sup>-1</sup>]",
                          validators=[MinValueValidator(0)])
    k0 = FloatField(label="Reaction rate constant "
                    + "[m<sup>5/2</sup>&middot;mol<sup>-1/2</sup>&middot;s<sup>-1</sup>]",
                    validators=[MinValueValidator(0)])
    s_min = FloatField(label="Minimum stoichiometry",
                       validators=[MinValueValidator(0)])
    s_max = FloatField(label="Maximum stoichiometry",
                       validators=[MinValueValidator(0)])
    cmax = FloatField(label="Maximum concentration of Li ions in particles [mol&middot;m<sup>-3</sup>]",
                      validators=[MinValueValidator(0)])

    # Double particle size
    x_r = FloatField(initial=0.5, label="Dimensionless coordinate <i>x<sub>R</sub></i> in the electrode, "
                     + "0&nbsp;&lt;&nbsp;<i>x<sub>R</sub></i>&nbsp;&lt;&nbsp;1",
                     validators=[MinValueValidator(0), MaxValueValidator(1)],
                     required=False)
    r_left = FloatField(initial=1, label="Particle radius multiplier <i>R</i><sub>left</sub> "
                        + "(for <i>x</i>&nbsp;&lt;&nbsp;<i>x<sub>R</sub></i>)",
                        validators=[MinValueValidator(0)],
                        required=False)
    r_right = FloatField(initial=1, label="Particle radius multiplier <i>R</i><sub>right</sub> "
                         + "(for <i>x</i>&nbsp;&gt;&nbsp;<i>x<sub>R</sub></i>)",
                         validators=[MinValueValidator(0)],
                         required=False)

    eqm_potential = FunctionField(
        label="Equilibrium potential vs concentration [V]",
        with_derivative=True,
        help_text="Enter equilibrium potential (V) as a function of the electrode stoichiometry <code>x</code>. "
        + "For square root use <code>sqrt()</code>, exponential function is "
        + "<code>exp()</code>, x<sup>y</sup> is <code>power(x,y)</code>, "
        + "hyperbolic tangent is <code>tanh()</code>.",
        rows=4
    )
    diffusivity = FunctionField(
        label="Diffusivity in particles vs concentration [m<sup>2</sup>&middot;s<sup>-1</sup>]",
        help_text="Enter diffusivity (m<sup>2</sup>/s) at the reference temperature "
        + "as a function of the electrode stoichiometry <code>x</code> "
        + "or provide a constant value. "
        + "For square root use <code>sqrt()</code>, exponential function is "
        + "<code>exp()</code>, x<sup>y</sup> is <code>power(x,y)</code>.",
        rows=4
    )

    def evaluate(self, validated_data, initial_data=None, fields=None):

        errors = {}
        try:
            validated_data = super().evaluate(validated_data, initial_data=initial_data, fields=fields)
        except ValidationError as exc:
            errors.update(exc.detail)

        need_eval = (not initial_data
                     or validated_data['s_min'] != initial_data['s_min']
                     or validated_data['s_max'] != initial_data['s_max'])

        fct_fields = {
            'diffusivity': {'lower': validated_data['s_min'],
                            'upper': validated_data['s_max'],
                            'steps': 10001,
                            'force_eval': need_eval},
            'eqm_potential': {'lower': validated_data['s_min'],
                              'upper': validated_data['s_max'],
                              'steps': 10001,
                              'force_eval': need_eval},
        }
        for name, kwargs in fct_fields.items():
            if not fields or name in fields:
                try:
                    fct_field = self._declared_fields[name]
                    validated_data[name] = fct_field.evaluate(
                        validated_data[name],
                        initial_data=initial_data.get(name, None) if initial_data else None,
                        **kwargs
                    )
                except ValidationError as exc:
                    errors.update({name: exc.detail})

        if errors:
            raise ValidationError(errors)

        return validated_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['R'] *= 1e6  # scale back into [um] used inside model
        return representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'R' in data and data['R']:
            data['R'] *= 1e-6  # [m]
        return data


class _Cell(battery_model._Cell):

    Ncells = IntegerField(initial=1, label="Number of electrode pairs connected in parallel to make a cell",
                          validators=[MinValueValidator(1)])
    Z0 = FloatField(initial=1, label="Initial State of Charge (SoC)",
                    help_text="Accepts values between 0 and 1, where 0 corresponds to the fully discharged"
                    + " state of a battery, and 1 to its fully charged state respectively.",
                    validators=[MinValueValidator(0.), MaxValueValidator(1.)])


class Battery_Pouch_1D(Battery_Model):

    label = 'Newman'

    class Meta:

        plots = {
            **Battery_Model.Meta.plots,
            'anode.eqm_potential': Plot(
                layout={'title': 'Equilibrium potential in Negative Electrode'}
            ),
            'cathode.eqm_potential': Plot(
                layout={'title': 'Equilibrium potential in Positive Electrode'}
            ),
            'anode.diffusivity': Plot(
                layout={'title': 'Diffusivity in Negative Electrode'}
            ),
            'cathode.diffusivity': Plot(
                layout={'title': 'Diffusivity in Positive Electrode'}
            ),
            'results.anode.concentration_final': Plot(
                data=[
                    {
                        'field': 'results.concentration_solid_anode_xrel_0_00',
                        'type': 'Line',
                        'line': {'color': '#33ddaa', 'width': 1},
                        'name': 'x<sub>rel</sub>=0.00',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_anode_xrel_0_25',
                        'type': 'Line',
                        'line': {'color': '#33aaff', 'width': 1},
                        'name': 'x<sub>rel</sub>=0.25',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_anode_xrel_0_50',
                        'type': 'Line',
                        'line': {'color': '#ff0000', 'width': 3},
                        'name': 'x<sub>rel</sub>=0.50',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_anode_xrel_0_75',
                        'type': 'Line',
                        'name': 'x<sub>rel</sub>=0.75',
                        'line': {'color': '#9900ff', 'width': 1},
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_anode_xrel_1_00',
                        'type': 'Line',

                        'name': 'x<sub>rel</sub>=1.00',
                        'line': {'color': '#000000', 'width': 1},
                        'ycol': -1,
                    },
                ],
                layout={
                    'title': 'Negative Particle Concentration (t<sub>final</sub>)',
                    'yaxis_title': 'Concentration (mol/m<sup>3</sup>)',
                    'xaxis_title': 'r (μm)',
                }
            ),
            'results.anode.concentration': SequencePlot(
                data={
                    'field': 'results.concentration_solid_anode_xrel_0_50',
                    'type': 'Line',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'Negative Particle Concentration (x<sub>rel</sub>=0.50)',
                    'yaxis_title': 'Concentration (mol/m<sup>3</sup>)',
                    'xaxis_title': 'r (μm)',
                }
            ),
            'results.anode.potential': SequencePlot(
                data={
                    'field': 'results.potential_solid_anode',
                    'type': 'Line',
                    'xcol': 'x',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'Potential at particles\' surfaces in Negative Electrode',
                    'yaxis_title': 'φ<sub>s</sub> (V)',
                    'xaxis_title': 'x (μm)',
                }
            ),
            'results.cathode.concentration_final': Plot(
                data=[
                    {
                        'field': 'results.concentration_solid_cathode_xrel_0_00',
                        'type': 'Line',
                        'line': {'color': '#000000', 'width': 1},
                        'name': 'x<sub>rel</sub>=0.00',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_cathode_xrel_0_25',
                        'type': 'Line',
                        'line': {'color': '#9900ff', 'width': 1},
                        'name': 'x<sub>rel</sub>=0.25',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_cathode_xrel_0_50',
                        'type': 'Line',
                        'line': {'color': '#ff0000', 'width': 3},
                        'name': 'x<sub>rel</sub>=0.50',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_cathode_xrel_0_75',
                        'type': 'Line',
                        'name': 'x<sub>rel</sub>=0.75',
                        'line': {'color': '#33aaff', 'width': 1},
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_cathode_xrel_1_00',
                        'type': 'Line',

                        'name': 'x<sub>rel</sub>=1.00',
                        'line': {'color': '#33ddaa', 'width': 1},
                        'ycol': -1,
                    },
                ],
                layout={
                    'title': 'Positive Particle Concentration (t<sub>final</sub>)',
                    'yaxis_title': 'Concentration (mol/m<sup>3</sup>)',
                    'xaxis_title': 'r (μm)',
                }
            ),
            'results.cathode.concentration': SequencePlot(
                data={
                    'field': 'results.concentration_solid_cathode_xrel_0_50',
                    'type': 'Line',
                    'xcol': 0,
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'Positive Particle Concetration (x<sub>rel</sub>=0.50)',
                    'yaxis_title': 'Concentration (mol/m<sup>3</sup>)',
                    'xaxis_title': 'r (μm)',
                }
            ),
            'results.cathode.potential': SequencePlot(
                data={
                    'field': 'results.potential_solid_cathode',
                    'type': 'Line',
                    'xcol': 'x',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'Potential at particles\' surfaces in Positive Electrode',
                    'yaxis_title': 'φ<sub>s</sub> (V)',
                    'xaxis_title': 'x (μm)',
                }
            ),
            'results.cell.concentration': SequencePlot(
                data={
                    'field': 'results.concentration_liquid',
                    'type': 'Line',
                    'xcol': 'x',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'Concentration in the electrolyte',
                    'yaxis_title': 'Concentration (mol/m<sup>3</sup>)',
                    'xaxis_title': 'x (μm)',
                }
            ),
            'results.cell.potential': SequencePlot(
                data={
                    'field': 'results.potential_liquid',
                    'type': 'Line',
                    'xcol': 'x',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'Potential in the electrolyte',
                    'yaxis_title': 'φ (V)',
                    'xaxis_title': 'x (μm)',
                }
            ),
        }

        results = ('data.zip', ZIPFileArchive, {
            'files': [
                *Battery_Model.Meta.results[2]['files'],
                ('concentration_liquid', 'concentration_liquid.dat', CSVFile, {}),
                ('potential_liquid', 'potential_liquid.dat', CSVFile, {}),
                ('potential_solid_anode', 'potential_solid_anode.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_00', 'concentration_solid_anode_xrel_0_00.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_25', 'concentration_solid_anode_xrel_0_25.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_50', 'concentration_solid_anode_xrel_0_50.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_75', 'concentration_solid_anode_xrel_0_75.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_1_00', 'concentration_solid_anode_xrel_1_00.dat', CSVFile, {}),
                ('potential_solid_cathode', 'potential_solid_cathode.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_00', 'concentration_solid_cathode_xrel_0_00.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_25', 'concentration_solid_cathode_xrel_0_25.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_50', 'concentration_solid_cathode_xrel_0_50.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_75', 'concentration_solid_cathode_xrel_0_75.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_1_00', 'concentration_solid_cathode_xrel_1_00.dat', CSVFile, {}),
            ]
        })

        class BPX_0_1:

            version = 0.1
            label = 'DFN'

            @classmethod
            def export(cls, params, meta=None):  # from internal
                ret = {
                    'Header': {
                        'BPX': cls.version,
                        'Model': cls.label,
                    },
                    'Parameterisation': {
                        'Cell': {
                            'Initial temperature [K]': params['cell.T0'],
                            'Reference temperature [K]': params['cell.T_ref'],
                            'Electrode area [m2]': params['cell.A'],
                            'Lower voltage cut-off [V]': params['cell.V_min'],
                            'Upper voltage cut-off [V]': params['cell.V_max'],
                            'Number of electrode pairs connected in parallel to make a cell': 1,
                        },
                        'Electrolyte': {
                            'Initial concentration [mol.m-3]': params['cell.c0'],
                            'Cation transference number': params['cell.tplus'],
                            'Conductivity [S.m-1]': FunctionField().to_representation(
                                {'func': params['cell.conductivity.func']}
                            )['func'],  # necessary to deserialize
                            'Diffusivity [m2.s-1]': FunctionField().to_representation(
                                {'func': params['cell.diffusivity.func']}
                            )['func'],  # necessary to deserialize
                            'Conductivity activation energy [J.mol-1]': params['cell.E_act_cond'],
                            'Diffusivity activation energy [J.mol-1]': params['cell.E_act_diff'],
                        },
                        'Negative electrode': {
                            'Particle radius [m]': params['anode.R'],
                            'Thickness [m]': params['anode.L'],
                            'Diffusivity [m2.s-1]': FunctionField().to_representation(
                                {'func': params['anode.diffusivity.func']}
                            )['func'],  # necessary to deserialize
                            'OCP [V]': FunctionField().to_representation(
                                {'func': params['anode.eqm_potential.func']}
                            )['func'],  # necessary to deserialize
                            'Conductivity [S.m-1]': params['anode.sigma_s'],
                            'Surface area per unit volume [m-1]': params['anode.bet'],
                            'Porosity': params['anode.el'],
                            'Transport efficiency': params['anode.B'],
                            'Reaction rate constant [mol.m-2.s-1]': params['anode.k0'] * (
                                math.sqrt(params['cell.c0']) * params['anode.cmax']
                            ),
                            'Minimum stoichiometry': params['anode.s_min'],
                            'Maximum stoichiometry': params['anode.s_max'],
                            'Maximum concentration [mol.m-3]': params['anode.cmax'],
                            'Diffusivity activation energy [J.mol-1]': params['anode.E_act_Ds'],
                            'Reaction rate constant activation energy [J.mol-1]': params['anode.E_act_k0'],
                        },
                        'Positive electrode': {
                            'Particle radius [m]': params['cathode.R'],
                            'Thickness [m]': params['cathode.L'],
                            'Diffusivity [m2.s-1]': FunctionField().to_representation(
                                {'func': params['cathode.diffusivity.func']}
                            )['func'],  # necessary to deserialize
                            'OCP [V]': FunctionField().to_representation(
                                {'func': params['cathode.eqm_potential.func']}
                            )['func'],  # necessary to deserialize
                            'Conductivity [S.m-1]': params['cathode.sigma_s'],
                            'Surface area per unit volume [m-1]': params['cathode.bet'],
                            'Porosity': params['cathode.el'],
                            'Transport efficiency': params['cathode.B'],
                            'Reaction rate constant [mol.m-2.s-1]': params['cathode.k0'] * (
                                math.sqrt(params['cell.c0']) * params['cathode.cmax']
                            ),
                            'Minimum stoichiometry': params['cathode.s_min'],
                            'Maximum stoichiometry': params['cathode.s_max'],
                            'Maximum concentration [mol.m-3]': params['cathode.cmax'],
                            'Diffusivity activation energy [J.mol-1]': params['cathode.E_act_Ds'],
                            'Reaction rate constant activation energy [J.mol-1]': params['cathode.E_act_k0'],
                        },
                        'Separator': {
                            'Thickness [m]': params['separator.L'],
                            'Porosity': params['separator.el'],
                            'Transport efficiency': params['separator.B'],
                        },
                    },
                }

                if meta and 'job_name' in meta:
                    ret['Header']['Title'] = meta['job_name']
                if meta and 'description' in meta:
                    ret['Header']['Description'] = meta['description']

                # cell.current will not exist in params if user input a table of currents, which cannot be
                # contained in BPX

                if 'cell.current' in params.keys():
                    ret['Parameterisation']['Cell']['Nominal cell capacity [A.h]'] = - params['cell.current']

                return ret

            @classmethod
            def import_(cls, data):  # to representation (!)
                header = data['Header']
                data_ = data['Parameterisation']
                ret = {
                    'job_name': header['Title'] if len(header['Title']) <= 64 else header['Title'][:61] + '...',  # noqa: E501
                    'description': header['Description'],
                    'model': 'Battery_Pouch_1D',
                    'params.cell.T0': data_['Cell']['Initial temperature [K]'],
                    'params.cell.T_ref': data_['Cell']['Reference temperature [K]'],
                    'params.cell.Z0': 1.,  # assuming fully charged battery in BPX
                    'params.cell.A': data_['Cell']['Electrode area [m2]'],
                    'params.cell.V_min': data_['Cell']['Lower voltage cut-off [V]'],
                    'params.cell.V_max': data_['Cell']['Upper voltage cut-off [V]'],
                    'params.cell.t_max': 4000,
                    'params.cell.Ncells': data_['Cell']['Number of electrode pairs connected in parallel to make a cell'],  # noqa: E501
                    'params.cell.c0': data_['Electrolyte']['Initial concentration [mol.m-3]'],
                    'params.cell.tplus': data_['Electrolyte']['Cation transference number'],
                    'params.cell.conductivity': FunctionField().to_representation(
                        FunctionField().to_internal_value(
                            {'func': data_['Electrolyte']['Conductivity [S.m-1]']}
                        )
                    ),
                    'params.cell.diffusivity': FunctionField().to_representation(
                        FunctionField().to_internal_value(
                            {'func': data_['Electrolyte']['Diffusivity [m2.s-1]']}
                        )
                    ),
                    'params.cell.E_act_cond': data_['Electrolyte']['Conductivity activation energy [J.mol-1]'],
                    'params.cell.E_act_diff': data_['Electrolyte']['Diffusivity activation energy [J.mol-1]'],
                    'params.anode.N': 20,
                    'params.anode.M': 20,
                    'params.anode.R': data_['Negative electrode']['Particle radius [m]'] * 1e6,
                    'params.anode.L': data_['Negative electrode']['Thickness [m]'] * 1e6,
                    'params.anode.diffusivity': FunctionField().to_representation(
                        FunctionField().to_internal_value(
                            {'func': data_['Negative electrode']['Diffusivity [m2.s-1]']}
                        )
                    ),
                    'params.anode.eqm_potential': FunctionField().to_representation(
                        FunctionField().to_internal_value(
                            {'func': data_['Negative electrode']['OCP [V]']}
                        )
                    ),
                    'params.anode.sigma_s': data_['Negative electrode']['Conductivity [S.m-1]'],
                    'params.anode.bet': data_['Negative electrode']['Surface area per unit volume [m-1]'],
                    'params.anode.el': data_['Negative electrode']['Porosity'],
                    'params.anode.B': data_['Negative electrode']['Transport efficiency'],
                    'params.anode.s_min': data_['Negative electrode']['Minimum stoichiometry'],
                    'params.anode.s_max': data_['Negative electrode']['Maximum stoichiometry'],
                    'params.anode.cmax': data_['Negative electrode']['Maximum concentration [mol.m-3]'],
                    'params.anode.E_act_Ds': data_['Negative electrode']['Diffusivity activation energy [J.mol-1]'],  # noqa: E501
                    'params.anode.E_act_k0': data_['Negative electrode']['Reaction rate constant activation energy [J.mol-1]'],  # noqa: E501
                    'params.cathode.N': 20,
                    'params.cathode.M': 20,
                    'params.cathode.R': data_['Positive electrode']['Particle radius [m]'] * 1e6,
                    'params.cathode.L': data_['Positive electrode']['Thickness [m]'] * 1e6,
                    'params.cathode.diffusivity': FunctionField().to_representation(
                        FunctionField().to_internal_value(
                            {'func': data_['Positive electrode']['Diffusivity [m2.s-1]']}
                        )
                    ),
                    'params.cathode.eqm_potential': FunctionField.Function(
                        FunctionField().to_internal_value(
                            {'func': data_['Positive electrode']['OCP [V]']}
                        )
                    ),
                    'params.cathode.sigma_s': data_['Positive electrode']['Conductivity [S.m-1]'],
                    'params.cathode.bet': data_['Positive electrode']['Surface area per unit volume [m-1]'],
                    'params.cathode.el': data_['Positive electrode']['Porosity'],
                    'params.cathode.B': data_['Positive electrode']['Transport efficiency'],
                    'params.cathode.s_min': data_['Positive electrode']['Minimum stoichiometry'],
                    'params.cathode.s_max': data_['Positive electrode']['Maximum stoichiometry'],
                    'params.cathode.cmax': data_['Positive electrode']['Maximum concentration [mol.m-3]'],
                    'params.cathode.E_act_Ds': data_['Positive electrode']['Diffusivity activation energy [J.mol-1]'],  # noqa: E501
                    'params.cathode.E_act_k0': data_['Positive electrode']['Reaction rate constant activation energy [J.mol-1]'],  # noqa: E501
                    'params.separator.N': 20,
                    'params.separator.L': data_['Separator']['Thickness [m]'] * 1e6,
                    'params.separator.el': data_['Separator']['Porosity'],
                    'params.separator.B': data_['Separator']['Transport efficiency'],
                }

                # Nominal cell capacity will be blank if loaded from a simulation which had a table input for current

                if 'Nominal cell capacity [A.h]' in data_['Cell']:
                    ret['params.cell.current'] = - float(data_['Cell']['Nominal cell capacity [A.h]'])

                c_e_0 = float(data_['Electrolyte']['Initial concentration [mol.m-3]'])

                k0_n = float(data_['Negative electrode']['Reaction rate constant [mol.m-2.s-1]'])
                c_n_max = float(data_['Negative electrode']['Maximum concentration [mol.m-3]'])
                ret['params.anode.k0'] = k0_n / (math.sqrt(c_e_0) * c_n_max)

                k0_p = float(data_['Positive electrode']['Reaction rate constant [mol.m-2.s-1]'])
                c_p_max = float(data_['Positive electrode']['Maximum concentration [mol.m-3]'])
                ret['params.cathode.k0'] = k0_p / (math.sqrt(c_e_0) * c_p_max)

                return ret

        class BPX_0_2(BPX_0_1):
            version = 0.2

        class BPX_0_3(BPX_0_2):
            version = 0.3

        class BPX_0_4(BPX_0_3):
            version = 0.4

            @classmethod
            def export(cls, params, meta=None):
                ret = super().export(params, meta)
                ret['Parameterisation']['User-defined'] = {
                    'Number of nodes in the electrolyte (Negative electrode)': params['anode.N'],
                    'Number of nodes in particles (Negative electrode)': params['anode.M'],
                    'Number of nodes in the electrolyte (Positive electrode)': params['cathode.N'],
                    'Number of nodes in particles (Positive electrode)': params['cathode.M'],
                    'Number of nodes in the electrolyte (Separator)': params['separator.N'],
                    'Discretisation': params['discretisation'],
                }
                return ret

            @classmethod
            def import_(cls, data):
                ret = super().import_(data)
                data_ = data['Parameterisation']
                ret['params.anode.N'] = data_['User-defined'].get('Number of nodes in the electrolyte (Negative electrode)', 30)
                ret['params.anode.M'] = data_['User-defined'].get('Number of nodes in particles (Negative electrode)', 30)
                ret['params.cathode.N'] = data_['User-defined'].get('Number of nodes in the electrolyte (Separator)', 30)
                ret['params.cathode.M'] = data_['User-defined'].get('Number of nodes in particles (Positive electrode)', 30)
                ret['params.separator.N'] = data_['User-defined'].get('Number of nodes in the electrolyte (Separator)', 20)
                ret['params.discretisation'] = data_['User-defined'].get('Discretisation', None)
                return ret

        exports = {
            'bpx': {
                'default': 0.4,
                'description': 'BPX file (Battery only)',
                'version': {
                    0.1: BPX_0_1,
                    0.2: BPX_0_2,
                    0.3: BPX_0_3,
                    0.4: BPX_0_4,
                }
            }
        }

    # TODO decimal or float fields? correct decimal places? do we need new validator to exclude 0?

    # Cell section
    cell = _Cell(label='Battery cell general parameters')

    # Electrode section

    cathode = _Electrode(
        label='Positive Electrode',
        initial={
            'E_act_Ds': 30300,
            'diff': "",
        }
    )

    anode = _Electrode(
        label='Negative Electrode',
        initial={  # overloads initial set in fields
            'E_act_Ds': 80600,
            'diff': "",
        })

    separator = _Contact(label='Separator')

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if (
                'anode' in data
                and 's_min' in data['anode']
                and 's_max' in data['anode']
                and 'cmax' in data['anode']
                and 'Z0' in data['cell']
        ):
            data['anode']['cs0'] = data['anode']['cmax'] * (
                data['cell']['Z0'] * data['anode']['s_max'] + (1.0 - data['cell']['Z0']) * data['anode']['s_min']
            )
        if (
                'cathode' in data
                and 's_min' in data['cathode']
                and 's_max' in data['cathode']
                and 'cmax' in data['cathode']
                and 'Z0' in data['cell']
        ):
            data['cathode']['cs0'] = data['cathode']['cmax'] * (
                data['cell']['Z0'] * data['cathode']['s_min'] + (1.0 - data['cell']['Z0']) * data['cathode']['s_max']
            )
        return data

    def get_meta(self, data):
        dae = {
            'n_a': get_dict(data, 'anode', 'N', default=0),
            'm_a': get_dict(data, 'anode', 'M', default=0),
            'n_c': get_dict(data, 'cathode', 'N', default=0),
            'm_c': get_dict(data, 'cathode', 'M', default=0),
            'n_s': get_dict(data, 'separator', 'N', default=0),
        }
        method = data.get('discretisation', None)
        if method == 'FV':
            # N_eq = 2 * (a.N + s.N + c.N - 3) + (a.N + c.N - 2) + (a.N - 1) * (a.M - 1) + (c.N - 1) * (c.M - 1) + 5
            dae['total'] = (2 * (dae['n_a'] + dae['n_s'] + dae['n_c'] - 3)
                            + (dae['n_a'] + dae['n_c'] - 2)
                            + (dae['n_a'] - 1) * (dae['m_a'] - 1)
                            + (dae['n_c'] - 1) * (dae['m_c'] - 1)
                            + 5)
        elif method == 'FECV':
            # N_eq = 2 * (a.N + s.N + c.N - 2) + (a.N + c.N) + a.N * a.M + c.N * c.M + 4
            dae['total'] = (2 * (dae['n_a'] + dae['n_s'] + dae['n_c'] - 2)
                            + (dae['n_a'] + dae['n_c'])
                            + dae['n_a'] * dae['m_a']
                            + dae['n_c'] * dae['m_c']
                            + 4)
        return {
            'dae': dae,
            'method': method,
        }
