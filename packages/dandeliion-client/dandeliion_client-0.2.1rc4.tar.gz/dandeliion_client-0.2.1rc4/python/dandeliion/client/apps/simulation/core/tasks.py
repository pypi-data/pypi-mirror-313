import threading

from ..interfaces.websockets import SimulationUpdateWebSocketClient
from ..interfaces.authentication import HTTPAuthenticator
client = None

cond_join = {}


def join(simulation):
    if not client:
        SimulationUpdateWebSocketClient.connect(connector=HTTPAuthenticator.client(), on_update=task_update_signal_hook)

    if simulation.pk not in cond_join:
        cond_join[simulation.pk] = threading.Condition()
        SimulationUpdateWebSocketClient.client().subscribe(simulation.pk)
    with cond_join[simulation.pk]:
        cond_join[simulation.pk].wait()


def task_update_signal_hook(updates):
    for sim in updates:
        pk = sim['id']
        with cond_join[pk]:
            cond_join[pk].notify_all()
