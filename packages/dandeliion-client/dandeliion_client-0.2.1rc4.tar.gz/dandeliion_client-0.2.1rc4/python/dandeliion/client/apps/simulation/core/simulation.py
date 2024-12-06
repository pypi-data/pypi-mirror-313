from .models.model import NestedSerializerMixin, Model
from ..models import simulation as models
from .models import fields
from .models.fields import serializers
from .models.export import BPX
import copy
import importlib
import json


class SimulationMixin:

    status_display = fields.CharField(
        source='get_status_display',
        read_only=True
    )
    model_display = fields.CharField(
        source='get_model_display',
        read_only=True
    )

    t_final = fields.CharField(
        source='meta.t_final',
        default='<NA>',
        read_only=True
    )

    owner = fields.CharField(
        source='owner.username',
        allow_null=True,
        read_only=True
    )

    # the following fields are added to exclude fields from updates via serializers

    # Timestamps
    time_submitted = fields.DateTimeField(label="Submission date", required=False, read_only=True)
    time_started = fields.DateTimeField(label="Start date", required=False, read_only=True)
    time_completed = fields.DateTimeField(label="Completion date", required=False, read_only=True)

    # Reason of stop
    stop_message = fields.TextField(label="Reason for stopping", required=False, read_only=True)

    class Meta:
        fields = (
            'status_display',
            'model_display',
            't_final',
        )


class SimulationBase(SimulationMixin, NestedSerializerMixin):

    params = None
    results = None

    def run_validation(self, data=serializers.empty):

        errors = {}
        try:
            value = super().run_validation(data)
            model = value.get('model', None)
            if not model:
                raise serializers.ValidationError({'model': ['No model selected']})
        except serializers.ValidationError as exc:
            errors.update(exc.detail)
            value = None  # TODO any way to do validation of equations without successful validation of serializer?

        # fetch original data if exists
        if self.instance:
            initial_data = self.instance.params
        else:
            initial_data = None
        # validate & evaluate
        if value:
            try:
                if isinstance(self._declared_fields['params'], Model):
                    value['params'] = self._declared_fields['params'].evaluate(
                        value['params'],
                        initial_data=initial_data
                    )
                    value['meta'] = self._declared_fields['params'].get_meta(value['params'])
            except serializers.ValidationError as exc:
                if 'params' in errors:
                    errors['params'].update(exc.detail)
                else:
                    errors['params'] = exc.detail

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['owner'] = self._owner
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def plot(self, name=None, output=None, layout=None, raise_exception=True):
        if hasattr(self, 'instance') and self.instance:
            data = self.instance.params
        else:
            self.is_valid(raise_exception=raise_exception)
            data = self.validated_data['params']
        data['results'] = self.results    # TODO make sure that results is loaded if needed
        return self._declared_fields['params'].plot(
            data=data,
            name=name,
            layout=layout,
            output=output
        )

    def save(self):
        self.instance = None  # never update, only create new
        super().save()
        return self.instance

    def delete(self, *args, **kwargs):
        self.instance.delete()

    def get_results(self, raw, key=None):
        if not self.results:
            self.results = self._declared_fields['params'].extract_results(raw)
        return self.results.raw(key)

    @classmethod
    def import_(cls, data=None, xformat: str = None, *args, **kwargs):
        if not xformat:
            # currently only cover default versions for import if available
            available_xformats = []

            # format available formats as (id, display name, comma separated string of expected file types)
            available_xformats.append(('dandeliion', 'DandeLiion parameter file', '.json'))
            available_xformats.append(('bpx', 'BPX file (Battery only)', '.json'))

            return available_xformats
        elif xformat.lower() == 'dandeliion':
            return cls(internal_values=json.load(data), *args, **kwargs)
        elif xformat.lower() == 'bpx':
            ret = cls(data=BPX.import_(data=json.load(data)), *args, **kwargs)
            ret.is_valid()
            return ret
        else:
            raise NotImplementedError('This format is not supported (yet):', xformat)

    def export(self, xformat: str = None, version=None, filename=None, raw=True, raise_exception=True):
        if hasattr(self, 'instance') and self.instance:
            params = self.instance.params
            model = self.instance.model
        else:
            self.is_valid(raise_exception=raise_exception)
            params = self.validated_data['params']
            model = self.validated_data['model']

        if not xformat:
            # currently only cover default versions for export if available
            available_xformats = []

            available_xformats.append(('dandeliion', 'DandeLiion parameter file'))
            if hasattr(self._declared_fields['params'].Meta, 'exports'):
                for xformat_, value in self._declared_fields['params'].Meta.exports.items():
                    available_xformats.append(
                        (xformat_,
                         value['description'] if 'description' in value else xformat_)
                    )
                    pass
            return available_xformats

        if xformat.lower() == 'bpx':
            if raw:
                if not filename:
                    filename = 'parameters.json'
                return filename, *BPX.export(
                    meta={
                        'model': model,
                        'job_name': self.instance.job_name,
                        'description': self.instance.description,
                    },
                    params=params,
                    raw=raw
                )
            else:
                return BPX.export(
                    meta={
                        'model': model,
                        'job_name': self.instance.job_name,
                        'description': self.instance.description,
                    },
                    params=params,
                    raw=raw
                )
        else:
            if raise_exception:
                raise NotImplementedError(
                    'The requested export format and/or version is not '
                    + f'supported (yet): {xformat}=={version}'
                )
            return None


class Simulation(SimulationBase, serializers.Serializer):

    class Meta:
        model = models.Simulation
        fields = '__all__'

    def __new__(cls, *args, **kwargs):
        # collect fields from model
        fields = copy.deepcopy(cls.Meta.model._declared_fields)

        if kwargs.get('instance', None):
            instance_ = cls.Meta.model.get(pk=kwargs['instance'])
            model_name = instance_.model
        elif kwargs.get('data', None) and kwargs['data'].get('model', None):
            model_name = kwargs['data']['model']
        else:
            model_name = None

        if model_name:
            # get battery model serializer by name and create instance
            Model_ = getattr(importlib.import_module('dandeliion.client.apps.simulation.core.models'),
                             model_name)(label='Battery Model')
            fields['params'] = Model_

        class_ = type('Simulation',
                      (cls, ),
                      fields)
        return super().__new__(class_, *args, **kwargs)

    def __init__(self, *args, user=None, **kwargs):
        self._owner = user
        if kwargs.get('instance', None):
            kwargs['instance'] = self.Meta.model.get(pk=kwargs['instance'])
        super().__init__(*args, **kwargs)

    @property
    def data(self):
        if hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
            msg = (
                'When a serializer is passed a `data` keyword argument you '
                'must call `.is_valid()` before attempting to access the '
                'serialized `.data` representation.\n'
                'You should either call `.is_valid()` first, '
                'or access `.initial_data` instead.'
            )
            raise AssertionError(msg)

        if not hasattr(self, '_data'):
            if self.instance is not None and not getattr(self, '_errors', None):
                # first assign everything to data (to preserve read-only values dropped by to_internal)
                self._data = self.instance._raw
                # since data stored as represenation remote model translate all non-readable values
                self._data.update(self.to_representation(self.to_internal_value(self.instance._raw)))
            elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.validated_data)
            else:
                self._data = self.get_initial()
        return self._data

    def save(self, **kwargs):
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        # using representation instead of validated_data since remote model stores in repr
        validated_data = {**self.to_representation(self.validated_data), **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    def create(self, validated_data):
        ModelClass = self.Meta.model
        instance = ModelClass(validated_data)
        instance.save()
        return instance
