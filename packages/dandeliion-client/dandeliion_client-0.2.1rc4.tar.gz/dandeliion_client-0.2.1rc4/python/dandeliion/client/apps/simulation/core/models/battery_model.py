from django.utils.safestring import mark_safe
from .fields import (
    FloatField,
    ListField,
    TableField,
    ChoiceField,
    FunctionField,
    MinValueValidator,
    MaxValueValidator,
    ValidationError,
)
from .model import Model
from .plot import Plot
from .results import ZIPFileArchive, JSONFile, TextFile, CSVFile


class _Cell(Model):

    class Meta:

        plots = {
            'conductivity': Plot(
                reqs=['conductivity'],
                data=[
                    {
                        'field': 'conductivity.eval',
                        'type': 'Line',
                    }
                ],
                layout={
                    'title': 'Conductivity in the electrolyte',
                    'yaxis_title': 'κ (S/m)',
                    'xaxis_title': 'Li concentration (mol/m<sup>3</sup>)',
                }
            ),
            'diffusivity': Plot(
                reqs=['diffusivity'],
                data=[
                    {
                        'field': 'diffusivity.eval',
                        'type': 'Line',
                    }
                ],
                layout={
                    'title': 'Diffusivity in the electrolyte',
                    'yaxis_title': 'D (m<sup>2</sup>/s)',
                    'xaxis_title': 'Li concentration (mol/m<sup>3</sup>)',
                    'yaxis_type': 'log',
                }
            )
        }

    conductivity_init = "0.1297 * power(x, 3.0) - 2.51 * power(x, 1.5) + 3.329 * x"
    diffusivity_init = "(8.794e-11 * x * x - 3.972e-10 * x + 4.862e-10) * 1e4"

    A = FloatField(label="Electrode cross-sectional area [m<sup>2</sup>]",
                   validators=[MinValueValidator(0)], required=True)
    T0 = FloatField(initial=298.15, label="Constant absolute temperature [K]",
                    validators=[MinValueValidator(0), MaxValueValidator(1000)])
    T_ref = FloatField(initial=298.15,
                       label="Reference temperature for the Arrhenius temperature dependence [K]",
                       validators=[MinValueValidator(0), MaxValueValidator(1000)])
    E_act_diff = FloatField(initial=0,
                            label="Activation energy for diffusivity in electrolyte "
                            + "[J&middot;mol<sup>-1</sup>]",
                            validators=[MinValueValidator(0)])
    E_act_cond = FloatField(initial=0,
                            label="Activation energy for conductivity in electrolyte "
                            + "[J&middot;mol<sup>-1</sup>]",
                            validators=[MinValueValidator(0)])
    tplus = FloatField(initial=0.26, label="Cation transference number of the electrolyte",
                       validators=[MinValueValidator(0), MaxValueValidator(1)])
    c0 = FloatField(initial=1000,
                    label="Initial concentration of Li ions in the electrolyte [mol&middot;m<sup>-3</sup>]",
                    validators=[MinValueValidator(0)])

    V_min = FloatField(initial=2.5, label="Minimum allowed voltage (optional) [V]",
                       required=False, validators=[MinValueValidator(0)])
    V_max = FloatField(initial=4.2, label="Maximum allowed voltage (optional) [V]",
                       required=False, validators=[MinValueValidator(0)])
    t_max = FloatField(initial=3600, label="Maximum charge/discharge time [s]",
                       validators=[MinValueValidator(0)])

    current = TableField(
        label="Charge/discharge current [A]",
        help_text=mark_safe(
            "For constant current, type a single value (for example, <code>-0.015</code>). "
            + "Positive values correspond to cell charging where the anode is lithiating and the "
            + "cathode is delithiating. "
            + "Negative values correspond to discharge. "
            + "For time-varying currents, provide a two-column table (the first column "
            + "is the time in seconds, the second column is the current in Amperes). "
            + "The table can be copied and pasted into the field directly from a spreadsheet "
            + "(e.g. MS Excel). The values between the points will be linearly interpolated."),
        rows=10)

    conductivity = FunctionField(
        initial=conductivity_init, label="Conductivity of the electrolyte [S&middot;m<sup>-1</sup>]",
        help_text="Enter conductivity (S/m) at the reference temperature as a function of Li concentration "
        + "<code>x</code> (mol&middot;m<sup>-3</sup>) or provide a constant value. "
        + "For square root use <code>sqrt()</code>, exponential function is "
        + "<code>exp()</code>, x<sup>y</sup> is <code>power(x,y)</code>.",
        max_length=1024,
        rows=4,
        allow_blank=True,
        required=False
    )

    diffusivity = FunctionField(
        initial=diffusivity_init, label="Diffusivity of the electrolyte, [m<sup>2</sup>&middot;s<sup>-1</sup>]",
        help_text="Enter diffusivity (m<sup>2</sup>/s) at the reference temperature "
        + "as a function of Li concentration <code>x</code> (mol&middot;m<sup>-3</sup>) or provide a constant value. "
        + "For square root use <code>sqrt()</code>, exponential function is "
        + "<code>exp()</code>, x<sup>y</sup> is <code>power(x,y)</code>.",
        max_length=1024,
        rows=4,
        allow_blank=True,
        required=False
    )

    t_output = ListField(
        label="User-defined times for output [s]",
        help_text="Provide a list (for example, <code>1000 2000 3000</code>) of the time points "
        + "for the output data files and plotting. "
        + "If empty, secondary variables (e.g. concentrations, potentials) will be written "
        + "and plotted for the initial and the final time step only.",
        rows=4,
        required=False)

    def evaluate(self, validated_data, initial_data=None, fields=None):
        errors = {}
        try:
            validated_data = super().evaluate(validated_data, initial_data=initial_data, fields=fields)
        except ValidationError as exc:
            errors.update(exc.detail)

        # clean up current table if necessary
        try:
            if not fields or 'current' in fields:
                try:
                    if isinstance(validated_data['current'], dict):
                        # first sort the table by time and get time and current column as lists
                        t, current = map(list,
                                         zip(*sorted(
                                             zip(validated_data['current']['x'],
                                                 validated_data['current']['y'])
                                         )))
                        i = 0
                        imax = len(t) - 2
                        while i < imax:
                            # remove identical intermediate points (not necessary for linear interpolation)
                            if current[i] == current[i + 1] == current[i + 2]:
                                t.pop(i + 1)
                                current.pop(i + 1)
                                imax -= 1
                            else:
                                i += 1
                        # write back cleaned & sorted result
                        validated_data['current'] = {'x': t, 'y': current}

                except Exception as e:
                    raise ValidationError(f"Invalid data: {e}") from e
        except ValidationError as exc:
            errors.update({'current': exc.detail})

        # evaluate diffusivity
        need_eval = not initial_data or validated_data['c0'] != initial_data['c0']

        fct_fields = {
            'diffusivity': {'lower': 0,
                            'upper': 2 * validated_data['c0'],
                            'steps': 10001,
                            'force_eval': need_eval},
            'conductivity': {'lower': 0,
                             'upper': 2 * validated_data['c0'],
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
        return representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data


class Battery_Model(Model):

    class Meta:
        plots = {
            'cell.diffusivity': Plot(),
            'cell.conductivity': Plot(),
            'results.total_current': Plot(
                data=[{
                    'field': 'results.total_current',
                    'type': 'Line',
                    'line': {'color': '#FF5F1F', 'width': 2},
                }],
                layout={
                    'title': 'Total current',
                    'yaxis_title': 'I (A)',
                    'xaxis_title': 'time (s)',
                }
            ),
            'results.total_voltage': Plot(
                data=[{
                    'field': 'results.total_voltage',
                    'type': 'Line',
                }],
                layout={
                    'title': 'Total voltage',
                    'yaxis_title': 'U (V)',
                    'xaxis_title': 'time (s)',
                }
            ),
        }
        results = ('data.zip', ZIPFileArchive, {
            'files': [
                ('logs', 'log.txt', TextFile, {}),
                ('parameters', 'parameters.json', JSONFile, {}),
                ('total_current', 'total_current.dat', CSVFile, {}),
                ('total_voltage', 'total_voltage.dat', CSVFile, {}),
            ]
        })

    # Discretisation
    _DISCRETISATION_CHOICES = [
        ('FV', 'Finite Volumes (1st Order)'),
        ('FECV', 'Finite Elements and Control Volumes (2nd Order)'),
    ]
    discretisation = ChoiceField(
        label="Spatial discretisation method",
        help_text="Finite Volume discretisation is the most common method but it has only 1<sup>st</sup> "
        + "order of approximation. An alternative discretisation scheme uses Finite Elements in electrolyte "
        + "and Control Volumes in solid particles providing 2<sup>nd</sup> order of approximation in the "
        + "electrolyte and in the particles. Both approaches are conservative and therefore total amount "
        + "of lithium is conserved exactly within the battery cell.",
        choices=_DISCRETISATION_CHOICES, initial='FV')

    # Simulation section
    dt_max = FloatField(label="Maximum time step [s]",
                        help_text="(optional) This option is recommended if you have a time-varying current; "
                        + "you can restrict the timestep to be finer than the resolution in the current demand.",
                        required=False,
                        validators=[MinValueValidator(0.05), MaxValueValidator(100)])

    t_final = FloatField(initial=0, label="Final simulation time [s]",
                         required=False, validators=[MinValueValidator(0)])

    # Cell section
    cell = _Cell(label='Battery cell general parameters')
