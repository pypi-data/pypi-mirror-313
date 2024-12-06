import importlib
import json
from dandeliion.client.tools.misc import flatten_dict, unflatten_dict


def get_models():
    from dandeliion.client.apps.simulation.core.models import __all__ as available_models

    models = {}
    for model in available_models:
        model_class = getattr(importlib.import_module('dandeliion.client.apps.simulation.core.models'),
                              model)
        if not hasattr(model_class.Meta, 'exports'):
            continue
        for version, handler in model_class.Meta.exports.get('bpx', {}).get('version', {}).items():
            if version not in models:
                models[version] = {handler.label: model_class}
            else:
                models[version][handler.label] = model_class
    return models


class BPX:

    @staticmethod
    def export(meta, params, version=None, raw=True):
        model = meta['model']
        params = flatten_dict(params)
        model_class = getattr(importlib.import_module('dandeliion.client.apps.simulation.core.models'),
                              model)
        if not version:
            version = model_class.Meta.exports['bpx']['default']
        BPXConverter = model_class.Meta.exports['bpx']['version'][version]

        bpx_out = BPXConverter.export(params=params, meta=meta)

        if raw:
            return 'application/bpx', json.dumps(bpx_out, ensure_ascii=False, indent=4)
        return bpx_out


    @staticmethod
    def import_(data):

        version_ = data['Header']['BPX']
        model_ = data['Header']['Model']
        models = get_models()
        if version_ not in models or model_ not in models[version_]:
            raise ValueError(f'Import failed. This combination of model [{model_}] '
                             f'and BPX version [{version_}] are not supported (yet).')
        BPXConverter = models[version_][model_].Meta.exports['bpx']['version'][version_]
        return unflatten_dict(BPXConverter.import_(data))
