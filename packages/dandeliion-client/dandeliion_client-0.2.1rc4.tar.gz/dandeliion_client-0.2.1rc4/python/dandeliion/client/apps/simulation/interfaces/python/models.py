import copy
from dandeliion.client.apps.simulation.core import models
from dandeliion.client.apps.simulation.core.models import model as controller


class Model:

    _serializer = None
    _parent = None

    def __init__(self, data={}, parent=None):
        self._data = {}
        self._parent = parent
        # set data values manually (to get validated in __setattr__)
        for key, value in data.items():
            self.__setattr__(key, value)

    def __getitem__(self, key):
        if key not in self._serializer._declared_fields:
            raise KeyError(f"'{key}' not found in object '{self.__class__.__name__}'")
        field = self._serializer._declared_fields[key]
        if field.write_only:
            raise AttributeError(f"'{key}' in object '{self.__class__.__name__}' is write-only")
        if key not in self._data:
            if isinstance(field, controller.Model):
                # create new derived Model class with serializer and instance of it
                self._data[key] = type(field.__class__.__name__, (Model, ), {"_serializer": field, })(
                    data=field.get_initial()
                )
            else:
                return None
        return self._data[key]

    def __getattr__(self, key):
        if key in ['_serializer', '_data', '_parent']:
            return self.__getattribute__(key)
        if key in ['label']:
            return getattr(self._serializer, key)
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(exc) from exc

    def __setattr__(self, key, value):
        if key in ['_serializer', '_data', '_parent']:
            return super().__setattr__(key, value)
        if key not in self._serializer._declared_fields:
            print(f"WARNING. '{key}' not found in object '{self.__class__.__name__}'. Ignoring it.")
            return
            # raise KeyError(f"'{key}' not found in object '{self.__class__.__name__}'")
        field = self._serializer._declared_fields[key]
        if field.read_only:
            raise AttributeError(f"'{key}' in {self.__class__.__name__} is read-only")
        # check if value matches expectations
        # if field is Model
        if isinstance(field, controller.Model):
            # if value is Model
            if isinstance(value, Model):
                # check if correct Model is passed (i.e. with correct serializer inside)
                if type(value._serializer) is not type(field):
                    raise TypeError(
                        f"Wrong type! (Expected: {self._serializer._declared_fields[key].__name__} "
                        + "Found: {value._serializer.__name__})"
                    )
            else:
                # create new derived Model class with serializer and instance of it
                value = type(field.__class__.__name__, (Model, ), {"_serializer": field, })(data=value)
        else:
            # validate value for fields if not None
            try:
                if value:
                    field.run_validation(data=value)
            except Exception as exc:
                raise TypeError(f"Invalid value found! {exc}") from exc
        self._data[key] = value

    def __iter__(self):
        return self._data.__iter__()

    @classmethod
    @property
    def _available_plots(cls):
        meta = getattr(cls._serializer, 'Meta', None)
        avail_plots = set(getattr(meta, 'plots', []))

        for key, field in cls._serializer._declared_fields.items():
            if isinstance(field, controller.Model):
                meta = getattr(field, 'Meta', None)
                avail_plots_ = set(getattr(meta, 'plots', []))
                avail_plots = avail_plots.union(set(['.'.join([key, name]) for name in avail_plots_]))
        return avail_plots

    @classmethod
    def help(cls):
        print("=" * len(cls._serializer.__class__.__name__))
        print(cls._serializer.__class__.__name__)
        print("=" * len(cls._serializer.__class__.__name__))
        if cls._serializer.help_text:
            print(cls._serializer.help_text)
        print()
        print("Fields:")
        print("-------")
        for key, field in cls._serializer._declared_fields.items():
            help_text = field.help_text if field.help_text else (
                field.label if field.label else field.__class__.__name__
            )
            print(f"     {key}\t-\t{help_text}")
        print()
        print("Plots:")
        print("-------")
        print(f"    {', '.join(cls._available_plots)}")

    def to_dict(self):
        data = copy.deepcopy(self._data)
        for key, value in data.items():
            if isinstance(value, Model):
                data[key] = value.to_dict()
        return data

    def plot(self, name=None, layout=None, output=None):
        # first validate/evaluate data
        ser_ = self._serializer
        try:
            data = ser_.run_validation(data=self.to_dict())
        except Exception as exc:
            raise ValueError(f"Something went wrong while preparing the data to plot: {exc}")
        return ser_.plot(data=data, name=name, layout=layout, output=output)


__all__ = models.__all__

# create end-user Models used in client
for name in __all__:
    globals()[name] = type(name, (Model, ), {"_serializer": getattr(models, name)(), })
