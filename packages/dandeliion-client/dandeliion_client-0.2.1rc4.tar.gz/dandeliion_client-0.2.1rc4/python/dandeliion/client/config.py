from os import environ

DANDELIION_SERVER = environ.get('DANDELIION_SERVER', 'https://sim.dandeliion.com')
DANDELIION_SIMULATION_ENDPOINT = f'{DANDELIION_SERVER}/api/'
DANDELIION_RESULTS_ENDPOINT = f'{DANDELIION_SERVER}/results/'
DANDELIION_WEBSOCKET_ENDPOINT = (
    f'wss://{DANDELIION_SERVER.removeprefix("https://")}/ws' if DANDELIION_SERVER.startswith('https://')
    else f'ws://{DANDELIION_SERVER.removeprefix("http://")}/ws'
)
DANDELIION_AUTH_ENDPOINT = f'{DANDELIION_SERVER}/accounts/'
DANDELIION_CLIENT_ID = 'dandeliion_python_client'
