from unittest import TestCase
from unittest.mock import patch, call, MagicMock  # Mock, ANY
import json
import os
from pathlib import Path
import importlib
from dandeliion.client.apps.simulation.models import simulation as models
from dandeliion.client.apps.simulation.core.simulation import Simulation as SimulationController
from dandeliion.client.apps.simulation.core import models as simulation_models

TESTDATA_FILENAME = os.path.join(Path(os.path.dirname(__file__)).parent, 'example_data.json')


class TestSimulation(TestCase):

    @patch('dandeliion.client.apps.simulation.core.simulation.Simulation.Meta.model.get')
    def test_new(self, mock_get):
        '''Test creating simulation instances'''

        # first model-less simulation without user
        sim = SimulationController()
        print(sim._declared_fields['params'])
        self.assertIsInstance(
            sim._declared_fields['params'],
            models.fields.JSONField
        )
        self.assertIsNone(sim._owner)

        # check all existing models and add user
        for model_name in simulation_models.__all__:
            sim = SimulationController(data={'model': model_name})
            self.assertIsInstance(
                sim._declared_fields['params'],
                getattr(
                    importlib.import_module('dandeliion.client.apps.simulation.core.models'),
                    model_name
                )
            )

        # check for instance
        with open(TESTDATA_FILENAME) as f:
            data = json.load(f)
        instance_ = models.Simulation(raw=data)
        mock_get.return_value = instance_

        sim = SimulationController(instance='some_id')
        mock_get.assert_has_calls([call(pk='some_id'), call(pk='some_id')])
        self.assertIsInstance(
            sim._declared_fields['params'],
            getattr(
                importlib.import_module('dandeliion.client.apps.simulation.core.models'),
                instance_.model
            )
        )

    def test_init(self):
        '''Test initialising simulation instances'''

        # defaults
        sim = SimulationController()
        self.assertIsNone(sim._owner)

        # set user/owner
        sim = SimulationController(user='juser')
        self.assertEqual(sim._owner, 'juser')

    def test_run_validation(self):
        pass  # TODO

    @patch('dandeliion.client.apps.simulation.core.simulation.serializers.Serializer.to_internal_value')
    def test_to_internal_value(self, mock_internal):
        sim = SimulationController(user='some user')
        mock_internal.return_value = {'key1': 'value1', 'key2': 'value2'}
        data = sim.to_internal_value('something')
        mock_internal.assert_called_once_with('something')
        self.assertDictEqual(data, {'key1': 'value1', 'key2': 'value2', 'owner': 'some user'})

    @patch('dandeliion.client.apps.simulation.core.simulation.serializers.Serializer.to_representation')
    def test_to_representation(self, mock_repr):
        mock_repr.return_value = MagicMock()
        sim = SimulationController()
        repr = sim.to_representation(instance='some instance')
        mock_repr.assert_called_once_with('some instance')
        self.assertEqual(repr, mock_repr.return_value)

    @patch('dandeliion.client.apps.simulation.core.simulation.Simulation.Meta.model.get')
    @patch('dandeliion.client.apps.simulation.core.simulation.serializers.Serializer._declared_fields')
    def test_plot(self, mock_fields, mock_get):

        # check for instance
        with open(TESTDATA_FILENAME) as f:
            data = json.load(f)
        instance_ = models.Simulation(raw=data)
        mock_get.return_value = instance_

        sim = SimulationController(instance='123')
        mock_model = MagicMock()
        d = {'params': mock_model}
        mock_fields.__getitem__.side_effect = d.__getitem__
        sim.plot()
        mock_fields.__getitem__.assert_has_calls([call()])

    @patch('dandeliion.client.apps.simulation.core.simulation.Simulation.Meta.model.save')
    def test_save(self, mock_save):

        with open(TESTDATA_FILENAME) as f:
            data = json.load(f)

        sim = SimulationController(data=data)

        # without calling is_valid() first
        with self.assertRaises(AssertionError):
            sim.save()

        sim.is_valid()
        sim.save()

        # TODO mock_save.assert_called_once_with(**data)

    def test_delete(self):

        sim = SimulationController()
        sim.instance = MagicMock()

        sim.delete()
        sim.instance.delete.assert_called()
