import importlib
import copy
from dandeliion.client.apps.simulation.core import tasks
from dandeliion.client.apps.simulation.core import simulation as controller
from dandeliion.client.apps.simulation.core.models import model as model_controller
from dandeliion.client.config import DANDELIION_RESULTS_ENDPOINT
from . import models
from .connection import REST_API
from .. import DandeliionInterfaceException


class Simulation:

    _serializer = controller.Simulation
    _data = {}
    _results = None

    def __init__(self, data={}, xformat='bpx', endpoint_results=None):
        version = None
        if xformat:
            # parse xformat for version number if exists
            tmp = xformat.split("==")
            version = tmp[1] if len(tmp) > 1 else None
            xformat = tmp[0]
        if hasattr(data, 'read'):
            data = self._serializer.import_(data, xformat=xformat, version=version).data
        elif isinstance(data, str):
            with open(data, 'r') as param_file:
                data = self._serializer.import_(param_file, xformat=xformat, version=version).data
        if not isinstance(data, dict):
            raise ValueError(
                "'data' argument has to filename or file-like object"
                + " of a valid parameter file or a valid parameter dictionary"
            )
        if not data:
            data = {'agree': False}
        self._data = data
        if endpoint_results:
            self._endpoint_results = endpoint_results
        else:
            self._endpoint_results = DANDELIION_RESULTS_ENDPOINT

    @classmethod
    def get(cls, pk):
        return Simulation(data=cls._serializer(instance=pk).data)

    def reload(self, pk=None):
        pk = pk if pk else self.id
        self._data.pop('id', None)
        self.__init__(data=self._serializer(instance=pk).data)

    def to_dict(self):
        data = copy.deepcopy(self._data)
        for key, value in data.items():
            if isinstance(value, models.Model):
                data[key] = value.to_dict()
        return data

    def compute(self, blocking=True):
        # if id is set, assume that simulation run already exists, so simply reload data
        if self.id:
            self.reload(pk=self.id)
            return
        ser_ = self._serializer(data=self.to_dict())
        ser_.is_valid(raise_exception=True)
        instance = ser_.save()
        self.reload(pk=instance.id)
        # submit simulation
        if blocking:
            self.join()

    def cancel(self):
        pk = self._data.get('id', None)
        if pk:
            self._serializer(instance=pk).delete()

    def join(self):
        while True:
            if self.status in ['Q', 'R']:
                # block until task update signalled
                tasks.join(self)
                self.reload()
            else:
                # nothing to wait for
                return

    def to_bpx(self, version=None):
        if not self.id:
            raise DandeliionInterfaceException('Simulation needs to be saved/computed first')
        return self._serializer(instance=self.id).export(xformat='bpx', version=version, raw=False)

    def get_template(self):
        template_keys = ['job_name', 'description', 'params', 'model', 'shared']
        data = {key: value for key, value in self.to_dict().items() if key in template_keys}
        return Simulation(data=data)

    def __getattr__(self, key):
        if key == 'pk':
            key = 'id'  # get from controller.Meta?
        if key == "model":
            return self.get_model()
        if key == 'params':
            # prevent direct access to params since we cannot track edits to it
            raise AttributeError('params cannot be accessed directly. use model.params instead')
        if key in ['_serializer', '_data', '_available_plots', '_results', '_endpoint_results']:
            return self.__getattribute__(key)
        serializer = self._serializer(data={'model': self._data.get("model", None)})
        if key == "results":
            if not self._results:
                try:
                    raw = REST_API.client().http_request(
                        method='GET',
                        path=self.id,
                        endpoint=self._endpoint_results,
                    ).content
                    serializer.get_results(raw)  # parse result data
                    self._results = serializer.results
                except Exception as e:
                    raise DandeliionInterfaceException from e
            return self._results
        if key not in serializer._declared_fields:
            raise KeyError(f"'{key}' not found in object '{self.__class__.__name__}'")
        field = serializer._declared_fields[key]
        if field.write_only:
            raise AttributeError(f"'{key}' in object '{self.__class__.__name__}' is write-only")
        if key not in self._data:
            if isinstance(field, model_controller.Model):
                # create new derived Model class with serializer and instance of it
                self._data[key] = type(field.__class__.__name__, (models.Model, ), {"_serializer": field, })(
                    data=field.get_initial()
                )
            else:
                return None
        return self._data[key]

    def __setattr__(self, key, value):
        if key == 'pk':
            key = 'id'  # get from controller.Meta?
        if key in ['_results', '_endpoint_results']:
            return super().__setattr__(key, value)
        if self._data.get('id', None):
            # we do not allow to change submitted simulations, nor setting the pk manually
            # (unless user explicitly changes _data, in which case it's their responsibility;
            # this poses no risk since data is again validated on the server)
            raise AttributeError("write-protected attribute."
                                 + " If you loaded this simulation, create a template with "
                                 + "'get_template()' and modify this instead.")

        if key == 'model' and type(value) is not str:
            # parse the model object for values
            self.model = value.__class__.__name__
            self.params = value._data
            return

        if key in ['_serializer', '_data']:
            return super().__setattr__(key, value)
        serializer = self._serializer()
        if key not in serializer._declared_fields:
            raise KeyError(f"'{key}' not found in object '{self.__class__.__name__}'")
        field = serializer._declared_fields[key]
        if field.read_only:
            raise AttributeError(f"'{key}' in {self.__class__.__name__} is read-only")
        # check if value matches expectations
        # if field is Model
        if isinstance(field, model_controller.Model):
            # if value is Model
            if isinstance(value, models.Model):
                # check if correct Model is passed (i.e. with correct serializer inside)
                if type(value._serializer) is not type(field):
                    raise TypeError(
                        f"Wrong type! (Expected: {serializer._declared_fields[key].__name__} "
                        + "Found: {value._serializer.__name__})"
                    )
            else:
                # create new derived Model class with serializer and instance of it
                value = type(field.__class__.__name__, (models.Model, ), {"_serializer": field, })(data=value)
        else:
            # validate value for fields if not None
            try:
                if value:
                    field.run_validation(data=value)
            except Exception as exc:
                raise TypeError(f"Invalid value found! {exc}") from exc
        self._data[key] = value

    def get_model(self):
        if self._data.get("model", None) not in models.__all__:
            raise ValueError(
                "No valid model was set yet. Make sure to set it first to a valid value:",
                models.__all__
            )
        params = self._data.get("params", None)
        if not params or not isinstance(params, models.Model):
            model_name = self._data.get("model", None)
            if not model_name:
                return None
            params = self._data.get("params", {})
            # dynamically load model class and create model instance from data
            class_ = getattr(importlib.import_module(
                'dandeliion.client.apps.simulation.interfaces.python.models'
            ), model_name)
            self._data["params"] = class_(data=params)
        return self._data["params"]

    @property
    def _available_plots(self):
        serializer = self._serializer(data=self.to_dict())

        meta = getattr(self._serializer, 'Meta', None)
        avail_plots = set(getattr(meta, 'plots', []))

        for key, field in serializer._declared_fields.items():
            if key == 'params':
                key = 'model'
            if isinstance(field, model_controller.Model):
                avail_plots = avail_plots.union(set(['.'.join([key, name]) for name in field.Meta.plots]))
        return avail_plots

    def plot(self, name, output=None, layout=None):
        if name == '__all__':
            name = None
        if name:
            n, *n_ = name.split('.')
            if n != 'model':
                raise Exception('Invalid plot name:', name)
            name = '.'.join(n_)
        ser = self._serializer(data=self.to_dict())
        try:
            ser.results = self.results
        except DandeliionInterfaceException:
            pass  # in this case we simply ignore any errors from fetching results
        plots = ser.plot(name=name, output=output, layout=layout)
        if name:
            return plots[name]
        else:
            return plots

    def help(self):
        print("=" * len(self._serializer.__name__))
        print(self._serializer.__name__)
        print("=" * len(self._serializer.__name__))
        serializer = self._serializer()
        if serializer.help_text:
            print(serializer.help_text)
        print()
        print("Fields:")
        print("-------")
        for key, field in serializer._declared_fields.items():
            help_text = field.help_text if field.help_text else (
                field.label if field.label else field.__class__.__name__
            )
            print(f"     {key}\t-\t{help_text}")
        print()
        print("Plots:")
        print("-------")
        print(f"    {', '.join(self._available_plots)}")
