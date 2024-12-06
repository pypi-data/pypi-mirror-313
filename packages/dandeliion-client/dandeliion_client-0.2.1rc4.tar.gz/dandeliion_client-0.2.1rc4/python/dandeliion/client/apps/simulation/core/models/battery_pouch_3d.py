from .battery_pouch_1d import Battery_Pouch_1D
from . import battery_pouch_1d
from .fields import (
    ChoiceField,
    IntegerField,
    FloatField,
    MinValueValidator,
    MaxValueValidator,
)
from .model import Model
from .plot import Plot
from .results import ZIPFileArchive, CSVFile, VTKPolyDataFile
from dandeliion.client.tools.misc import get_dict


# This class is used internally, if it is reusable, it should be best moved into its own module
class _CurrentCollector(Model):

    x0 = FloatField(initial=0.4, label="First relative X coordinate of current collector [Lx]",
                    validators=[MinValueValidator(0), MaxValueValidator(1)])
    x1 = FloatField(initial=0.6, label="Second relative X coordinate of current collector [Lx]",
                    validators=[MinValueValidator(0), MaxValueValidator(1)])
    len = FloatField(initial=15, label="Length of current collector (along Y axis) [mm]",
                     validators=[MinValueValidator(0)])

    _COLLECTOR_POSITION_CHOICES = [
        ('Top', 'Top'),
        ('Bottom', 'Bottom'),
    ]
    side = ChoiceField(choices=_COLLECTOR_POSITION_CHOICES, initial='Top',
                       label="Position of current collector")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['len'] *= 1e3  # scale back into [mm] used inside model
        return representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'len' in data and data['len']:
            data['len'] *= 1e-3  # [m]
        return data


class _Cell(battery_pouch_1d._Cell):

    # Extended Electrode section
    Nx = IntegerField(initial=1, label="Number of grid cells along X axis (width)",
                      validators=[MinValueValidator(1), MaxValueValidator(50)])
    Ny = IntegerField(initial=1, label="Number of grid cells along Y axis (length)",
                      validators=[MinValueValidator(1), MaxValueValidator(50)])
    Ncells = IntegerField(initial=1, label="Number of grid cells along Z axis (thickness)",
                          validators=[MinValueValidator(1), MaxValueValidator(50)])
    Lx = FloatField(initial=42.0, label="Battery width [mm]",
                    validators=[MinValueValidator(0)])
    Ly = FloatField(initial=140.0, label="Battery length [mm]",
                    validators=[MinValueValidator(0)])
    Lz = FloatField(initial=11.4, label="Battery thickness [mm]",
                    validators=[MinValueValidator(0)])
    kx = FloatField(initial=60.5, label="Thermal conductivity along X axis"
                    + " [W&middot;m<sup>-1</sup>&middot;K<sup>-1</sup>]",
                    validators=[MinValueValidator(0)])
    ky = FloatField(initial=60.5, label="Thermal conductivity along Y axis"
                    + " [W&middot;m<sup>-1</sup>&middot;K<sup>-1</sup>]",
                    validators=[MinValueValidator(0)])
    kz = FloatField(initial=0.914, label="Thermal conductivity along Z axis"
                    + " [W&middot;m<sup>-1</sup>&middot;K<sup>-1</sup>]",
                    validators=[MinValueValidator(0)])
    rho = FloatField(initial=2586.0, label="Lumped density [kg&middot;m<sup>-3</sup>]",
                     validators=[MinValueValidator(0)])
    Cp = FloatField(initial=1361.0, label="Lumped heat capacity [J&middot;kg<sup>-1</sup>&middot;K<sup>-1</sup>]",
                    validators=[MinValueValidator(0)])

    _BOUNDARY_CONDITION_CHOICES = [
        ('None', 'None'),
        ('Current Collectors', 'Current Collectors'),
        ('Side', 'Side'),
        ('Two Sides', 'Two Sides'),
        ('Zero Heat Source', 'Zero Heat Source'),
    ]
    TempBC = ChoiceField(choices=_BOUNDARY_CONDITION_CHOICES, initial='Current Collectors',
                         label="Boundary conditions for the temperature equation")

    CC1 = _CurrentCollector(label="Current Collector #1")
    CC2 = _CurrentCollector(label="Current Collector #2")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Lx'] *= 1e3  # scale back into [mm] used inside model
        representation['Ly'] *= 1e3  # scale back into [mm] used inside model
        representation['Lz'] *= 1e3  # scale back into [mm] used inside model
        return representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'Lx' in data and data['Lx']:
            data['Lx'] *= 1e-3  # [m]
        if 'Ly' in data and data['Ly']:
            data['Ly'] *= 1e-3  # [m]
        if 'Lz' in data and data['Lz']:
            data['Lz'] *= 1e-3  # [m]
        return data


class Battery_Pouch_3D(Battery_Pouch_1D):

    label = '3D Pouch Cell'

    class Meta:

        plots = {
            **Battery_Pouch_1D.Meta.plots,
            'results.temperature': Plot(
                data=[
                    {
                        'field': 'results.temperature_centre',
                        'type': 'Line',
                        'line': {'color': '#0077dd', 'width': 3},
                        'name': 'centre',
                    },
                    {
                        'field': 'results.temperature_average',
                        'type': 'Line',
                        'line': {'color': '#ff0000', 'width': 1},
                        'name': 'average',
                    }],
                layout={
                    'title': 'Temperature in the pouch cell',
                    'yaxis_title': 'Temperature (°C)',
                    'xaxis_title': 'time (s)',
                },
            ),
        }

        results = ('data.zip', ZIPFileArchive, {
            'files': [
                *Battery_Pouch_1D.Meta.results[2]['files'],
                ('temperature_average', 'temperature_average.dat', CSVFile, {}),
                ('temperature_centre', 'temperature_centre.dat', CSVFile, {}),
                ('model3D_anode', 'paraview_cc_0.vts', VTKPolyDataFile, {}),
                ('model3D_cathode', 'paraview_cc_1.vts', VTKPolyDataFile, {}),
                (None, r'.*\.vtr', VTKPolyDataFile, {}),
                (None, r'.*\.vts', VTKPolyDataFile, {}),
            ]
        })

    # Cell section
    cell = _Cell(label='Battery cell general parameters')

    # Discretisation
    _DISCRETISATION_CHOICES = [
        ('FECV', 'Finite Elements and Control Volumes (2nd Order)'),
    ]
    discretisation = ChoiceField(
        label="Spatial discretisation method",
        help_text="Finite Volume discretisation is the most common method but it has only 1<sup>st</sup> "
        + "order of approximation. An alternative discretisation scheme uses Finite Elements in electrolyte "
        + "and Control Volumes in solid particles providing 2<sup>nd</sup> order of approximation in the "
        + "electrolyte and in the particles. Both approaches are conservative and therefore total amount "
        + "of lithium is conserved exactly within the battery cell.",
        choices=_DISCRETISATION_CHOICES, initial='FECV')

    def get_meta(self, data):
        meta = super().get_meta(data)
        # N_eq = (2 * (a.N + s.N + c.N - 2) + (a.N + c.N) + a.N * a.M + c.N * c.M + 3) * Ncells * Nx * Ny + 2
        if meta['method'] == 'FECV':
            meta['dae']['total'] = ((meta['dae']['total'] - 1) * (
                get_dict(data, 'cell', 'Ncells', default=0)
                * get_dict(data, 'cell', 'Nx', default=0)
                * get_dict(data, 'cell', 'Ny', default=0)
            ) + 2)
        return meta
