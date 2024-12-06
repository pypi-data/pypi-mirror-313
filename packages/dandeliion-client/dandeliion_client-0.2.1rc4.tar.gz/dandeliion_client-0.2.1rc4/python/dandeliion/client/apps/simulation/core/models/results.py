import zipfile
import csv
import os
import io
import pathlib
import re
import json

import dandeliion.client.tools.vtk as vtk
from .export import BPX


class ResultFile:

    mime_type = 'application/octet-stream'

    def __init__(self, raw, filename, args={}):

        self._raw = raw
        self.filename = filename
        self.mime_type = args.get('mime_type', self.mime_type)  # overriding default mime

    def raw(self):
        return self.filename, self.mime_type, self._raw


class ZIPFileArchive(ResultFile):

    mime_type = 'application/zip'

    def __init__(self, raw, filename, args={}):
        super().__init__(raw, filename)
        # check if valid zipfile
        if not zipfile.is_zipfile(io.BytesIO(self._raw)):
            raise ValueError('Not a valid zipfile!')
        self._loaded = False
        files = args.get('files', [])
        self._paths = {filepath: x for label, filepath, *x in files if label is not None}
        self._patterns = {filepath: x for label, filepath, *x in files if label is None}
        self._files = {label: x for label, *x in files if label is not None}

    def raw(self, filepath=None):
        if not filepath:
            return super().raw()

        if not self._loaded:
            self.load()
        filename = os.path.basename(filepath)
        raw = self._instance.read(filepath)
        result_class = ResultFile
        args = {}

        if filepath in self._paths:
            result_class, args = self._paths[filepath]
        else:
            for pattern in self._patterns:
                if re.match(pattern, filepath):
                    result_class, args = self._patterns[pattern]
                    break

        return result_class(io.BytesIO(raw), filename, args).raw()

    def load(self):
        self._instance = zipfile.ZipFile(io.BytesIO(self._raw))
        self._loaded = True

    def __del__(self):
        if self._loaded:
            self._instance.close()

    def __getitem__(self, key):

        if key is None:
            raise IndexError('None is invalid key')
        if not self._loaded:
            self.load()
        filepath, result_class, args = self._files[key]
        raw = self._instance.read(filepath)
        filename = os.path.basename(filepath)

        return result_class(io.BytesIO(raw), filename, args)

    def __getattr__(self, key):

        if key in self._files:
            return self[key]

        return super().__getattribute__(key)


class CSVFile(ResultFile, dict):

    mime_type = 'text/csv'

    def __init__(self, raw, filename, args={}):
        ResultFile.__init__(self, raw, filename)
        self.has_header = args.get('has_header', True)
        self.columns = args.get('columns', {})
        self.delimiter = args.get('delimiter', '\t')
        # self.is_loaded = False
        self.load()  # TODO switch to lazy loading?

    def load(self):
        fp = io.TextIOWrapper(self._raw)
        data = list(csv.reader(fp, delimiter=self.delimiter))
        fp.detach()  # prevents TextIOWrapper from closing raw stream
        self._raw.seek(0)  # resets raw stream

        if not self.columns and not self.has_header:
            raise AttributeError("Either file has to have header or 'columns' has to be specified")
        if self.has_header:
            columns = data.pop(0)
        if self.columns:
            columns = self.columns

        data = list(map(list, zip(*data)))
        for i in range(len(columns)):
            self.__setitem__(columns[i], list(map(float, data[i])))

        self.loaded = True


class VTKPolyDataFile(ResultFile):

    mime_type = 'text/plain'

    def __init__(self, raw, filename, args={}):
        raw = self.convert(raw, pathlib.Path(filename).suffix)
        ResultFile.__init__(self, raw, filename)

    @staticmethod
    def convert(raw, dtype):
        if dtype == '.vtp':  # nothing to do
            return raw
        if dtype == '.vtr':
            return io.BytesIO(
                vtk.convertRectilinear2PolyData(
                    raw.read().decode()
                ).encode()
            )
        if dtype == '.vts':
            return io.BytesIO(
                vtk.convertStructuredGrid2PolyData(
                    raw.read().decode()
                ).encode()
            )
        raise NotImplementedError(f'Support for {dtype} not implemented yet!')


class JSONFile(ResultFile, dict):

    mime_type = 'application/json'

    def __init__(self, raw, filename, args={}):
        ResultFile.__init__(self, raw, filename)
        # self.is_loaded = False
        self.load()  # TODO switch to lazy loading?

    def load(self):
        fp = io.TextIOWrapper(self._raw)
        data = json.load(fp)
        fp.detach()  # prevents TextIOWrapper from closing raw stream
        self._raw.seek(0)  # resets raw stream
        self.clear()  # to be safe, if function called manually
        self.update(data)
        self.loaded = True


class TextFile(ResultFile):

    mime_type = 'text/plain'

    def __init__(self, raw, filename, args={}):
        ResultFile.__init__(self, raw, filename)
        # self.is_loaded = False
        self.load()  # TODO switch to lazy loading?

    def load(self):
        fp = io.TextIOWrapper(self._raw)
        self.data = fp.read()
        fp.detach()  # prevents TextIOWrapper from closing raw stream
        self._raw.seek(0)  # resets raw stream
        self.loaded = True

    def __repr__(self):
        return self.data


class BPXFile(JSONFile):

    mime_type = 'application/bpx'

    def __init__(self, filename, raw, args={}):
        raw = self.convert(raw)
        super.__init__(self, raw, filename)

    @staticmethod
    def convert(raw):
        fp = io.TextIOWrapper(raw)
        data = json.load(fp)
        fp.detach()  # prevents TextIOWrapper from closing raw stream
        raw.seek(0)  # resets raw stream
        return io.BytesIO(BPX.export(meta={'model': data['model']}, params=data['params']))
