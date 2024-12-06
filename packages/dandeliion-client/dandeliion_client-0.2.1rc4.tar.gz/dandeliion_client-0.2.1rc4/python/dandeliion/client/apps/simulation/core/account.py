from ..model import Simulation


class Account:  # TODO rewrite to have instances representing different accounts?

    _user_id = None

    @classmethod
    def set(cls, user_id):
        cls._user_id = user_id

    @classmethod
    def load(cls, simulation_id, copy=False):
        sim = Simulation.get(simulation_id)
        if copy:
            sim.pk = None
        return sim

    @classmethod
    def export(cls, simulation_id):
        pass  # TODO return bytestream of simulation config/data

    @classmethod
    def info(cls):
        # TODO query account info from server (RESTful API?)
        result = {}
        return result

    @classmethod
    def list(cls):
        # query simulation list from server
        return Simulation.where(user_id=cls.user_id)

    def __str__(self):
        return f"{self.info()}\n-------------\n{self.list()}"
