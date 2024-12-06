from tabulate import tabulate
from dandeliion.client.apps.simulation.core import queue as controller
from .simulation import Simulation


class Queue(list):

    _serializer = controller.Queue
    _print_fields = ['id', 'job_name', 'status', 'time_submitted', 'time_started', 'time_completed']

    @classmethod
    def list(cls, pk=None, queue='__default__'):
        return cls([Simulation(data=resp) for resp in cls._serializer.list(pk=pk, queue=queue)])

    @classmethod
    def submit(cls, simulation):
        if simulation.pk:
            raise ValueError('cannot submit that has already run')
        simulation.compute(blocking=False)

    @classmethod
    def cancel(cls, pk):
        Simulation.get(pk=pk).cancel()

    def __str__(self):
        data = [[getattr(item, key, '') for key in self._print_fields] for item in self]
        serializer = self._serializer()
        headers = []
        for key in self._print_fields:
            label = serializer._declared_fields.get(key).label
            headers.append(label.upper() if label else key)
        return tabulate(data, headers=headers)

    @classmethod
    def help(cls):
        str_ = 'Queue'
        print("=" * len(str_))
        print(str_)
        print("=" * len(str_))
        serializer = cls._serializer()
        print()
        print("Fields:")
        print("-------")
        for key, field in serializer._declared_fields.items():
            help_text = field.help_text if field.help_text else (
                field.label if field.label else field.__class__.__name__
            )
            print(f"     {key}\t-\t{help_text}")
