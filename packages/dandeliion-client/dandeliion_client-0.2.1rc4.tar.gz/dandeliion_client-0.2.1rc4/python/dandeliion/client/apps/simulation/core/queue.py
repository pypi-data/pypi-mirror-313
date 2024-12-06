import copy
from .models.fields import serializers
from .simulation import Simulation, SimulationMixin
from ..models import queue as models


class Queue(SimulationMixin, serializers.Serializer):

    class Meta:
        model = models.Queue
        fields = '__all__'

    def __new__(cls, *args, **kwargs):
        # collect fields from model
        fields = copy.deepcopy(cls.Meta.model._declared_fields)
        class_ = type('Simulation',
                      (cls, ),
                      fields)
        return super().__new__(class_, *args, **kwargs)

    @classmethod
    def list(cls, pk=None, queue='__default__'):
        # remove pk if None (i.e. do not filter for pk)
        return cls.Meta.model.where(pk=pk, queue=queue)

    def cancel(self, pk):
        Simulation(instance=self.data['id']).delete()
