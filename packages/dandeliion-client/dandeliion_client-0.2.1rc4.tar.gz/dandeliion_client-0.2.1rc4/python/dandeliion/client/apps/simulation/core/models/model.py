from dandeliion.client.tools import plotting, misc
from collections import OrderedDict
from rest_framework.serializers import (
    Serializer,
    Mapping,
    empty,
    ValidationError,
)
import logging
logger = logging.getLogger(__name__)


class InvalidPlotError(Exception):
    pass


class NestedSerializerMixin:

    def get_initial(self, initial_data=empty):
        if hasattr(self, 'initial_data'):
            initial_data = self.initial_data
        if initial_data is not empty:
            # initial_data may not be a valid type
            if not isinstance(initial_data, Mapping):
                return OrderedDict()

            return OrderedDict([
                (field_name,
                 field.get_initial(field.get_value(initial_data))
                 if isinstance(field, NestedSerializerMixin)
                 else field.get_value(initial_data))
                for field_name, field in self.fields.items()
                # only populate nested serializers with initials if this is called by top serializer
                if ((hasattr(self, 'initial_data') and isinstance(field, NestedSerializerMixin))
                    or field.get_value(initial_data) is not empty)
                and not field.read_only
            ])

        return OrderedDict([
            (field.field_name, field.get_initial())
            for field in self.fields.values()
            if not field.read_only
        ])


class Model(NestedSerializerMixin, Serializer):

    # performs validation and evaluation of this serializer and all subfields of same type
    def evaluate(self, evaluated_data, initial_data=None, fields=None):

        # logger.info('EVALUATE', evaluated_data, initial_data, fields)

        # split field name (in case subfields are listed) and group them
        if fields:
            fields_ = {}
            for key in fields:
                key_, *sub_ = key.split('.')
                if key_ in fields_:
                    fields_[key_].append('.'.join(sub_))
                else:
                    fields_[key_] = ['.'.join(sub_)]
            fields = fields_

        errors = OrderedDict()
        for name, field in self._declared_fields.items():
            if (not fields or name in fields) and isinstance(field, Model):
                try:
                    evaluated_data[name] = field.evaluate(
                        evaluated_data[name],
                        initial_data.get(name, None) if initial_data else None,
                        fields[name] if fields else None
                    )
                except ValidationError as exc:
                    errors[name] = exc.detail

        if errors:
            raise ValidationError(errors)

        return evaluated_data

    # processes param (used to translate some db/param data back into model data
    # i.e. unit conversion, deserialization, etc.);
    # should be overloaded by inheriting classes (still calling the parent method!) where necessary
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data

    # this method adds default values where required
    # this can be overloaded to perform any required additional
    # transformations of the data
    def to_representation(self, instance):
        respresentation = super().to_representation(instance)
        return respresentation

    def plot(self, data, name=None, layout=None, output=None):

        # logger.info('PLOT', self.__class__, name, 'LAYOUT', layout)

        meta = getattr(self, 'Meta', None)
        available_plots = getattr(meta, 'plots', [])

        if not name:
            name = list(available_plots.keys())

        if isinstance(name, list):
            results = {}
            for item in name:
                try:
                    results.update(self.plot(data, item, layout=layout, output=output))
                except Exception:
                    pass  # ignore any plots with errors
            return misc.flatten_dict(results)

        layout = misc.update_dict(
            getattr(available_plots[name], 'layout', {}) if name in available_plots else {},
            layout if layout else {},
            inline=False
        )

        key_, *sub_ = name.split('.')
        # try to find it in nested model first (but overload layout with that of parent if exists)
        try:
            if isinstance(self._declared_fields.get(key_, None), Model):
                return misc.flatten_dict({
                    key_: self._declared_fields.get(key_).plot(
                        data[key_], name='.'.join(sub_), layout=layout, output=output)
                })
        except InvalidPlotError:
            pass
        except Exception:
            raise

        if name not in available_plots:
            raise InvalidPlotError('unknown plotting setup:', name)

        plot_cfg = available_plots[name]

        data_ = self.evaluate(
            data,
            fields=plot_cfg.get_datafields(default=[name])
        )
        data_ = plot_cfg.prepare_data(data_, default=[name])

        return {
            name: plotting.make_plot(
                data_,
                layout,
                output
            )
        }

    def get_meta(self, data):
        return {}

    def extract_results(self, raw):

        meta = getattr(self, 'Meta', None)
        filename, result_class, args = getattr(meta, 'results', ('data', 'ResultFile', {}))
        return result_class(raw, filename, args)
