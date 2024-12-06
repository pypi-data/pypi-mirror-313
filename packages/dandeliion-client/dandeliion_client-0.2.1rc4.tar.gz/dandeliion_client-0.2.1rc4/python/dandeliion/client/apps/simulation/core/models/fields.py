import io
import json
import numpy as np
from rest_framework import serializers  # noqa: F401
from rest_framework.serializers import (  # noqa: F401
    Serializer,
    Field,
    ValidationError,
)
from rest_framework.fields import (  # noqa: F401
    UUIDField,
    EmailField,
    JSONField,
    BooleanField,
    CharField,
    DictField,
    IntegerField,
    ChoiceField,
    SerializerMethodField,
    DateTimeField,
)
from rest_framework import fields
from dandeliion.client.tools import evaluation as ev

sz = 12
md = 8  # Max number of digits


class MinValueValidator:
    def __init__(self, minimum, exclusive=False):
        self.minimum = minimum
        self.exclusive = exclusive

    def __call__(self, value):
        if self.exclusive and value <= self.minimum:
            message = 'This field must be strictly larger than %d.' % self.minimum
            raise ValidationError(message)
        elif value < self.minimum:
            message = 'This field must be at least %d.' % self.minimum
            raise ValidationError(message)


class MaxValueValidator:
    def __init__(self, maximum, exclusive=False):
        self.maximum = maximum
        self.exclusive = exclusive

    def __call__(self, value):
        if self.exclusive and value >= self.maximum:
            message = 'This field must be strictly less than %d.' % self.maximum
            raise ValidationError(message)
        elif value > self.maximum:
            message = 'This field must be at most %d.' % self.maximum
            raise ValidationError(message)


class FloatField(fields.FloatField):

    def __init__(self, *args, **kwargs):
        style = kwargs.get('style', {})
        style['input_type'] = 'text'
        kwargs['style'] = style
        super().__init__(*args, **kwargs)


class TextField(fields.CharField):

    def __init__(self, *args, rows=1, **kwargs):
        style = kwargs.get('style', {})
        style['rows'] = rows
        if 'base_template' not in style:
            style['base_template'] = 'textarea.html'
        kwargs['style'] = style
        super().__init__(*args, **kwargs)


class TableField(fields.Field):

    def __init__(self, *args, rows=1, **kwargs):
        style = kwargs.get('style', {})
        style['rows'] = rows
        if 'base_template' not in style:
            style['base_template'] = 'list_field.html'
        kwargs['style'] = style
        super().__init__(*args, **kwargs)

    class Table(dict):
        def __str__(self):
            return '\n'.join([f'{x}\t{y}' for x, y in zip(self['x'], self['y'])])

    def to_internal_value(self, data):
        if isinstance(data, dict):
            return dict(data)  # if data is instance of subclass of dict e.g. Table
        elif isinstance(data, float):
            return data  # if already float simply return it
        elif isinstance(data, int):
            return float(data)
        # convert str into dict
        try:
            tmp = np.loadtxt(io.StringIO(data))
            dim = len(tmp.shape)
            if dim == 0:
                return tmp.tolist()
            elif (dim == 1) and (tmp.shape[0] == 2):
                x = [tmp[0]]
                y = [tmp[1]]
                return {'x': x, 'y': y}
            elif (dim == 2) and (tmp.shape[1] == 2):
                x = tmp[:, 0].tolist()
                y = tmp[:, 1].tolist()
                return {'x': x, 'y': y}
        except Exception:
            pass

        message = 'This must be either a single value or a two column list' \
            + ' (delimited by whitespaces) without column titles'
        raise ValidationError(message)

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return self.Table(instance)
        else:
            return instance


class FunctionField(fields.CharField, TableField, Serializer):

    def __init__(self, *args, with_derivative=False, with_integral=False, **kwargs):
        style = kwargs.get('style', {})
        if 'base_template' not in style:
            style['base_template'] = 'function.html'
        kwargs['style'] = style
        super().__init__(*args, **kwargs)

        self._with_derivative = with_derivative
        self._with_integral = with_integral

    class Function(dict):
        def __getattr__(self, key):
            if key in ['func', 'eval', 'derivative_eval', 'integral_eval']:
                return self[key] if key in self else None
            return super().__getattr__(key)

        def __repr__(self):
            return self['func'].__repr__()

        def __str__(self):
            return self['func'].__str__()

    def get_value(self, dictionary):
        ret = super().get_value(dictionary)

        if not isinstance(ret, dict):  # e.g. if empty field
            return ret
        if 'eval' in ret and isinstance(ret['eval'], str):
            ret['eval'] = json.loads(ret['eval'])
        if 'derivative_eval' in ret and isinstance(ret['derivative_eval'], str):
            ret['derivative_eval'] = json.loads(ret['derivative_eval'])
        if 'integral_eval' in ret and isinstance(ret['integral_eval'], str):
            ret['integral_eval'] = json.loads(ret['integral_eval'])
        return ret

    def to_representation(self, instance):
        representation = self.Function()
        representation['func'] = ev.deserialize(instance['func'])
        representation['_func'] = instance['func']
        if isinstance(representation['func'], dict):  # is table
            representation['func'] = TableField.to_representation(self, representation['func'])
        if 'eval' in instance:
            representation['eval'] = instance['eval']
        if self._with_derivative and 'derivative_eval' in instance:
            representation['derivative_eval'] = instance['derivative_eval']
        if self._with_integral and 'integral_eval' in instance:
            representation['integral_eval'] = instance['integral_eval']
        return representation

    def to_internal_value(self, data):
        instance = {}
        # check if provided data is just func data
        if not isinstance(data, dict) or 'func' not in data:
            func = data
        else:
            func = data['func']

        try:
            # check if data is table
            func = TableField.to_internal_value(self, func)
        except Exception:
            pass  # nothing to do, just store callable / eqn as it is
        instance['func'] = ev.serialize(func)

        # if function has been changed, we are not storing old eval data
        if '_func' not in data or instance['func'].strip() != data['_func'].strip():
            # print('ignoring outdated eval data')
            return instance

        if 'eval' in data:
            if not isinstance(data['eval'], dict):
                instance['eval'] = json.loads(data['eval'])
            else:
                instance['eval'] = data['eval']

        if self._with_derivative and 'derivative_eval' in data:
            if not isinstance(data['derivative_eval'], dict):
                instance['derivative_eval'] = json.loads(data['derivative_eval'])
            else:
                instance['derivative_eval'] = data['derivative_eval']
        if self._with_integral and 'integral_eval' in data:
            if not isinstance(data['integral_eval'], dict):
                instance['integral_eval'] = json.loads(data['integral_eval'])
            else:
                instance['integral_eval'] = data['integral_eval']
        return instance

    def evaluate(self, validated_data, lower, upper, steps, initial_data=None, force_eval=False):

        force_eval = force_eval or not initial_data
        func_ = validated_data.get('func', None)
        eval_ = validated_data.get('eval', None)
        eval_deriv = validated_data.get('derivative_eval', None)
        eval_integral = validated_data.get('integral_eval', None)
        if eval_:
            try:
                ev.validate_data(data=eval_,
                                 lower=lower, upper=upper)
                if self._with_derivative:
                    ev.validate_data(data={'x': eval_['x'],
                                           'y': eval_deriv['y']},
                                     lower=lower, upper=upper)
                if self._with_integral:
                    ev.validate_data(data={'x': eval_['x'],
                                           'y': eval_integral['y']},
                                     lower=lower, upper=upper)
            except Exception:
                # raise ValidationError(f"Invalid evaluated data: {e}") from e
                eval_ = None
        # else:  # no (or outdated) eval in validated_data
        if not eval_:
            if not func_:
                # try to recover function and evaluation from initial data
                if not initial_data:
                    raise ValidationError("no function/data provided!")
                else:
                    validated_data['func'] = initial_data.get('func', None)
                    # remark: func may be missing in initial data if func is private/hidden, but then eval has to exist
                # (re-)evaluate if necessary
            if force_eval or (initial_data and func_ != initial_data.get('func', None)):
                try:
                    validated_data['eval'] = dict(zip(
                        ['x', 'y'],
                        ev.evaluate_function(
                            func=ev.deserialize(func_),
                            lower=lower, upper=upper, steps=steps)))
                    if self._with_derivative:
                        validated_data['derivative_eval'] = dict(zip(
                            ['x', 'y'],
                            ev.evaluate_div_function(
                                func=ev.deserialize(func_),
                                lower=lower, upper=upper, steps=steps)))
                    if self._with_integral:
                        validated_data['integral_eval'] = dict(zip(
                            ['x', 'y'],
                            ev.evaluate_int_function(
                                func=(validated_data['eqm_potential_eval']['x'],
                                      validated_data['eqm_potential_eval']['y']))))

                except Exception as e:
                    raise ValidationError(f"{e}") from e
            else:
                # assuming here that initial data is valid (func is allowed to be missing/hidden)
                validated_data['func'] = initial_data.get('func', None)
                validated_data['eval'] = initial_data['eval']
                if self._with_derivative:
                    validated_data['derivative_eval'] = initial_data['derivative_eval']
                if self._with_integral:
                    validated_data['integral_eval'] = initial_data['integral_eval']

        return validated_data


class ListField(fields.Field):

    def __init__(self, *args, rows=1, **kwargs):
        style = kwargs.get('style', {})
        style['rows'] = rows
        style['base_template'] = 'list_field.html'
        kwargs['style'] = style
        super().__init__(*args, **kwargs)

    class List(list):
        def __str__(self):
            return "\n".join(map(str, self))

    def to_internal_value(self, data):
        try:
            if isinstance(data, list):
                return list(data)
            data = np.loadtxt(io.StringIO(data)).tolist()
            if not isinstance(data, list):  # in case it's a single float
                data = [data]
            return data

        except Exception:
            message = 'This must be a list of values (delimited by whitespaces)' \
                + ' or a column of values'
            raise ValidationError(message)

    def to_representation(self, instance):
        return self.List(instance)
