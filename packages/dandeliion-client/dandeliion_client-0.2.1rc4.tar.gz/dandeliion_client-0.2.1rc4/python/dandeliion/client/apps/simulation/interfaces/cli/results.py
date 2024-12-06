import argparse
import sys
from dandeliion.client.apps.simulation import Simulation
from .connection import connect


def download():

    parser = argparse.ArgumentParser(description='Export results of Dandeliion simulation.')
    parser.add_argument(
        'id',
        metavar='JOB_ID',
        help='simulation job id'
    )
    parser.add_argument(
        '-o',
        '--outfile',
        metavar='OUT_FILE',
        help='output file',
        default=None,
    )
    parser.add_argument(
        '-c',
        '--credentials',
        metavar='CRED_FILE',
        default=None,
        help='path to a Dandeliion credential file'
    )

    args = parser.parse_args()

    try:
        connect(credentials=args.credentials)
        sim = Simulation.get(pk=args.id)
        outfile, mime, data = sim.results.raw()
        if args.outfile:
            outfile = args.outfile
        with open(outfile, 'wb') as fb:
            fb.write(data)
    except Exception as e:
        print(f'Something went wrong while fetching/writing results: {e}')
        sys.exit(1)

    print(f'Simulation results written to {outfile}')
