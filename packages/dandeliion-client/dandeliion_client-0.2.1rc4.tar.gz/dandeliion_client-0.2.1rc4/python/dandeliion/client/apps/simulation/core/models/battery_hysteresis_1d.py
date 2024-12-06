from django.utils.safestring import mark_safe
from .results import ZIPFileArchive, CSVFile
from .plot import Plot, SequencePlot
from . import battery_pouch_1d
from .fields import (
    FloatField,
    TableField,
    ChoiceField,
    FunctionField,
    MinValueValidator,
    MaxValueValidator,
    ValidationError,
)
import math
import numpy as np


# This classes are used internally, if it is resusable, it should be best moved into its own module
class _ReducedElectrode(battery_pouch_1d._Contact):

    # TODO decimal or float fields? correct decimal places? do we need new validator to exclude 0?

    class Meta:
        plots = {}

    # Reduced electrode section

    sigma_s = FloatField(label="Electric conductivity of particles [S&middot;m<sup>-1</sup>]",
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

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['M'] = 5
        data['R'] = 1.
        data['diffusivity'] = {'func': '', 'eval': {'x': [0., 1.,], 'y': [1., 1.,]}}
        data['eqm_potential'] = {'func': '', 'eval': {'x': [0., 1.,], 'y': [1., 1.,]}}
        data['bet'] = 1.
        data['E_act_Ds'] = 1.
        data['E_act_k0'] = 1.
        return data


class _Cell(battery_pouch_1d._Cell):

    class Meta(battery_pouch_1d._Cell.Meta):

        plots = {
            **battery_pouch_1d._Cell.Meta.plots,
            'r_dist': Plot(
                reqs=['r_dist'],  # TODO does not work if r_dist not in internal_data
                data=[{
                    'field': 'r_dist',
                    'type': 'Scatter',
                    'mode': 'lines+markers',
                    'fill': 'tozeroy',
                    'line_shape': 'vh',
                    'ycol': -1,
                }],
                layout={
                    'title': 'Particle size distribution',
                    'yaxis_title': 'Probability',
                    'xaxis_title': 'R (nm)',
                }
            ),
        }

    Ueq_c0 = FloatField(initial=3.42, label="Plateau voltage [V]",
                        help_text="",
                        validators=[MinValueValidator(0.)])

    r_dist = TableField(
        label="Particle size distribution",
        help_text=mark_safe(
            "Provide a two-column table (the first column "
            + "is the right boundary for a particle size bin in nanometers while the left boundary "
            + "is determined from the right boundary of the previous bin; left boundary of the first bin is <code>0</code>; "
            + "the second column is the probability for each bin)."),
        rows=6)

    def evaluate(self, validated_data, initial_data=None, fields=None):
        errors = {}
        try:
            validated_data = super().evaluate(validated_data, initial_data=initial_data, fields=fields)
        except ValidationError as exc:
            errors.update(exc.detail)

        # normalise r distribution
        norm = np.sum(validated_data['w_i'])
        prob = np.array(validated_data['w_i'])
        prob /= norm
        validated_data['w_i'] = prob.tolist()

        if np.any(prob < 0):
            errors.update({'r_dist': ValidationError('no probability can be negative!')})

        """
        validated_data['r_dist']['y'] = list(validated_data['w_i'])
        # if left-most boundary of distribution not defined, set to 0 (needed e.g. for plotting)
        if validated_data['r_dist']['y'][0] != 0:
            validated_data['r_dist']['x'].insert(0,0)
            validated_data['r_dist']['y'].insert(0,0)
        """

        if errors:
            raise ValidationError(errors)

        return validated_data

    def to_representation(self, instance):
        instance['r_dist'] = {
            'x': [val * 1e9 for val in instance['r_i']],  # scale back into [nm] used inside model
            'y': instance['w_i'],
        }
        representation = super().to_representation(instance)
        return representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        r_dist = data.pop('r_dist')
        data['r_i'] = [val * 1e-9 for val in r_dist['x']]  # [m]
        data['w_i'] = r_dist['y']
        return data


class Battery_Hysteresis_1D(battery_pouch_1d.Battery_Pouch_1D):

    label = 'Hysteresis'

    class Meta:

        plots = {
            **battery_pouch_1d.Battery_Model.Meta.plots,
            'cell.r_dist': Plot(),
            'anode.eqm_potential': battery_pouch_1d.Battery_Pouch_1D.Meta.plots['anode.eqm_potential'],
            'anode.diffusivity': battery_pouch_1d.Battery_Pouch_1D.Meta.plots['anode.diffusivity'],
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
                        'field': 'results.concentration_solid_anode_xrel_0_20',
                        'type': 'Line',
                        'line': {'color': '#33aaff', 'width': 1},
                        'name': 'x<sub>rel</sub>=0.20',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_anode_xrel_0_40',
                        'type': 'Line',
                        'line': {'color': '#ff0000', 'width': 3},
                        'name': 'x<sub>rel</sub>=0.40',
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_anode_xrel_0_60',
                        'type': 'Line',
                        'name': 'x<sub>rel</sub>=0.60',
                        'line': {'color': '#9900ff', 'width': 1},
                        'ycol': -1,
                    },
                    {
                        'field': 'results.concentration_solid_anode_xrel_0_80',
                        'type': 'Line',
                        'name': 'x<sub>rel</sub>=0.80',
                        'line': {'color': '#3300ff', 'width': 1},
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
                    'field': 'results.concentration_solid_anode_xrel_0_40',
                    'type': 'Line',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'Negative Particle Concentration (x<sub>rel</sub>=0.40)',
                    'yaxis_title': 'Concentration (mol/m<sup>3</sup>)',
                    'xaxis_title': 'r (μm)',
                }
            ),
            'results.anode.potential': battery_pouch_1d.Battery_Pouch_1D.Meta.plots['results.anode.potential'],
            'results.cathode.concentration_xrel_0_00': SequencePlot(
                data={
                    'field': 'results.concentration_solid_cathode_xrel_0_00',
                    'type': 'Line',
                    'xcol': 't(x_rel=0)',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'x = 0',
                    'yaxis_title': 'c<sub>avg</sub> (mol/m<sup>3</sup>)',
                    'xaxis_title': 't (s)',
                }
            ),
            'results.cathode.concentration_xrel_0_20': SequencePlot(
                data={
                    'field': 'results.concentration_solid_cathode_xrel_0_20',
                    'type': 'Line',
                    'xcol': 't(x_rel=0.2)',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'x = 1/5 L<sub>p</sub>',
                    'yaxis_title': 'c<sub>avg</sub> (mol/m<sup>3</sup>)',
                    'xaxis_title': 't (s)',
                }
            ),
            'results.cathode.concentration_xrel_0_40': SequencePlot(
                data={
                    'field': 'results.concentration_solid_cathode_xrel_0_40',
                    'type': 'Line',
                    'xcol': 't(x_rel=0.4)',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'x = 2/5 L<sub>p</sub>',
                    'yaxis_title': 'c<sub>avg</sub> (mol/m<sup>3</sup>)',
                    'xaxis_title': 't (s)',
                }
            ),
            'results.cathode.concentration_xrel_0_60': SequencePlot(
                data={
                    'field': 'results.concentration_solid_cathode_xrel_0_60',
                    'type': 'Line',
                    'xcol': 't(x_rel=0.6)',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'x = 3/5 L<sub>p</sub>',
                    'yaxis_title': 'c<sub>avg</sub> (mol/m<sup>3</sup>)',
                    'xaxis_title': 't (s)',
                }
            ),
            'results.cathode.concentration_xrel_0_80': SequencePlot(
                data={
                    'field': 'results.concentration_solid_cathode_xrel_0_80',
                    'type': 'Line',
                    'xcol': 't(x_rel=0.8)',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'x = 4/5 L<sub>p</sub>',
                    'yaxis_title': 'c<sub>avg</sub> (mol/m<sup>3</sup>)',
                    'xaxis_title': 't (s)',
                }
            ),
            'results.cathode.concentration_xrel_1_00': SequencePlot(
                data={
                    'field': 'results.concentration_solid_cathode_xrel_1_00',
                    'type': 'Line',
                    'xcol': 't(x_rel=1)',
                    'first': {'color': '#0077dd'},
                    'last': {'color': '#ff0000'},
                },
                layout={
                    'title': 'x = L<sub>p</sub>',
                    'yaxis_title': 'c<sub>avg</sub> (mol/m<sup>3</sup>)',
                    'xaxis_title': 't (s)',
                }
            ),
            'results.total_voltage_vs_capacity': Plot(
                data=[{
                    'field': 'results.total_voltage_vs_capacity',
                    'type': 'Line',
                }],
                layout={
                    'title': 'Total voltage vs integrated capacity',
                    'yaxis_title': 'U (V)',
                    'xaxis_title': 'capacity (Ah)',
                }
            ),
            'results.cathode.potential': battery_pouch_1d.Battery_Pouch_1D.Meta.plots['results.cathode.potential'],
            'results.cell.concentration': battery_pouch_1d.Battery_Pouch_1D.Meta.plots['results.cell.concentration'],
            'results.cell.potential': battery_pouch_1d.Battery_Pouch_1D.Meta.plots['results.cell.potential'],
        }

        results = ('data.zip', ZIPFileArchive, {
            'files': [
                *battery_pouch_1d.Battery_Model.Meta.results[2]['files'],
                ('concentration_liquid', 'concentration_liquid.dat', CSVFile, {}),
                ('potential_liquid', 'potential_liquid.dat', CSVFile, {}),
                ('potential_solid_anode', 'potential_solid_anode.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_00', 'concentration_solid_anode_xrel_0_00.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_20', 'concentration_solid_anode_xrel_0_20.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_40', 'concentration_solid_anode_xrel_0_40.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_60', 'concentration_solid_anode_xrel_0_60.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_0_80', 'concentration_solid_anode_xrel_0_80.dat', CSVFile, {}),
                ('concentration_solid_anode_xrel_1_00', 'concentration_solid_anode_xrel_1_00.dat', CSVFile, {}),
                ('potential_solid_cathode', 'potential_solid_cathode.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_00', 'concentration_solid_cathode_xrel_0_00.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_20', 'concentration_solid_cathode_xrel_0_20.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_40', 'concentration_solid_cathode_xrel_0_40.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_60', 'concentration_solid_cathode_xrel_0_60.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_0_80', 'concentration_solid_cathode_xrel_0_80.dat', CSVFile, {}),
                ('concentration_solid_cathode_xrel_1_00', 'concentration_solid_cathode_xrel_1_00.dat', CSVFile, {}),
                ('capacity_integrated', 'capacity_integrated.dat', CSVFile, {}),
                ('total_voltage_vs_capacity', 'total_voltage_vs_capacity.dat', CSVFile, {}),
            ]
        })

        class BPX_0_4:

            label = 'FV_Hyst'
            version = 0.4

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
                        "User-defined": {
                            'Plateau voltage [V]': params['cell.Ueq_c0'],
                            'Particle size distribution': {
                                'x': params['cell.r_i'],  # in [m] !
                                'y': params['cell.w_i'],
                            },
                            'Number of nodes in the electrolyte (Negative electrode)': params['anode.N'],
                            'Number of nodes in particles (Negative electrode)': params['anode.M'],
                            'Number of nodes in the electrolyte (Positive electrode)': params['cathode.N'],
                            'Number of nodes in the electrolyte (Separator)': params['separator.N'],
                            'Discretisation': params['discretisation'],
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
                            'Particle radius [m]': 1.,  # dummy
                            'Thickness [m]': params['cathode.L'],
                            'Diffusivity [m2.s-1]': '1',  # dummy
                            'OCP [V]': '1',  # dummy
                            'Conductivity [S.m-1]': params['cathode.sigma_s'],
                            'Surface area per unit volume [m-1]': 1.,  # dummy
                            'Porosity': params['cathode.el'],
                            'Transport efficiency': params['cathode.B'],
                            'Reaction rate constant [mol.m-2.s-1]': params['cathode.k0'] * (
                                math.sqrt(params['cell.c0']) * params['cathode.cmax']
                            ),
                            'Minimum stoichiometry': params['cathode.s_min'],
                            'Maximum stoichiometry': params['cathode.s_max'],
                            'Maximum concentration [mol.m-3]': params['cathode.cmax'],
                            'Diffusivity activation energy [J.mol-1]': 1.,  # dummy
                            'Reaction rate constant activation energy [J.mol-1]': 1.,  # dummy
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
                    'model': 'Battery_Hysteresis_1D',
                    'params.discretisation': data_['User-defined']['Discretisation'],
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
                    'params.cell.Ueq_c0': data_['User-defined']['Plateau voltage [V]'],
                    'params.cell.r_dist': TableField().to_representation({
                        'x': [value * 1e9 for value in data_['User-defined']['Particle size distribution']['x']],  # into [nm]
                        'y': data_['User-defined']['Particle size distribution']['y'],
                    }),
                    'params.cathode.N': data_['User-defined'].get('Number of nodes in the electrolyte (Positive electrode)', 30),
                    'params.cathode.L': data_['Positive electrode']['Thickness [m]'] * 1e6,
                    'params.cathode.sigma_s': data_['Positive electrode']['Conductivity [S.m-1]'],
                    'params.cathode.el': data_['Positive electrode']['Porosity'],
                    'params.cathode.B': data_['Positive electrode']['Transport efficiency'],
                    'params.cathode.s_min': data_['Positive electrode']['Minimum stoichiometry'],
                    'params.cathode.s_max': data_['Positive electrode']['Maximum stoichiometry'],
                    'params.cathode.cmax': data_['Positive electrode']['Maximum concentration [mol.m-3]'],
                    'params.anode.N': data_['User-defined'].get('Number of nodes in the electrolyte (Negative electrode)', 30),
                    'params.anode.M': data_['User-defined'].get('Number of nodes in particles (Negative electrode)', 30),
                    'params.anode.R': data_['Negative electrode']['Particle radius [m]'] * 1e6,
                    'params.anode.L': data_['Negative electrode']['Thickness [m]'] * 1e6,
                    'params.anode.diffusivity': FunctionField().to_representation(
                        FunctionField().to_internal_value(
                            {'func': data_['Negative electrode']['Diffusivity [m2.s-1]']}
                        )
                    ),
                    'params.anode.eqm_potential': FunctionField.Function(
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
                    'params.separator.N': data_['User-defined'].get('Number of nodes in the electrolyte (Separator)', 20),
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

        exports = {
            'bpx': {
                'default': 0.4,
                'description': 'BPX file (Battery only)',
                'version': {
                    0.4: BPX_0_4,
                }
            }
        }

    # TODO decimal or float fields? correct decimal places? do we need new validator to exclude 0?

    # Discretisation
    _DISCRETISATION_CHOICES = [
        ('FV', 'Finite Volumes (1st Order)'),
    ]
    discretisation = ChoiceField(
        label="Spatial discretisation method",
        help_text="Finite Volume discretisation is the most common method but it has only 1<sup>st</sup> "
        + "order of approximation. An alternative discretisation scheme uses Finite Elements in electrolyte "
        + "and Control Volumes in solid particles providing 2<sup>nd</sup> order of approximation in the "
        + "electrolyte and in the particles. Both approaches are conservative and therefore total amount "
        + "of lithium is conserved exactly within the battery cell.",
        choices=_DISCRETISATION_CHOICES, initial='FV')

    # Cell section
    cell = _Cell(label='Battery cell general parameters')

    # Electrode section
    cathode = _ReducedElectrode(
        label='Positive Electrode',
        initial={  # overloads initial set in fields
        })
