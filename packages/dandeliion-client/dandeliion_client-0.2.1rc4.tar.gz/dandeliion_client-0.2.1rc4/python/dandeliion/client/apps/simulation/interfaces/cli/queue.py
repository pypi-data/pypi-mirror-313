import argparse
import json
import sys
from dandeliion.client.apps.simulation import Simulation, Queue
from .connection import connect


def submit():
    parser = argparse.ArgumentParser(description='Submit Dandeliion simulation.')
    parser.add_argument(
        'config',
        metavar='CONFIG_FILE',
        help='path to a simulation config file'
    )
    parser.add_argument(
        '--jobname',
        default=None,
        help='name/label for simulation job to be submitted'
    )
    parser.add_argument(
        '--queue',
        default=None,
        help='queue to submit to; overrides any queue settings in the config if present (default: None)'
    )
    parser.add_argument(
        '-c',
        '--credentials',
        metavar='CRED_FILE',
        default=None,
        help='path to a Dandeliion credential file'
    )
    parser.add_argument(
        '--agree',
        action='store_true'
    )

    args = parser.parse_args()

    try:
        connect(credentials=args.credentials)

        with open(args.config) as config_file:
            config = json.load(config_file)

        if args.queue:
            config['queue'] = args.queue

        sim = Simulation(config).get_template()
        if not sim.job_name:
            if not args.jobname:
                raise Exception('You have to provide a jobname either in the parameter file or as an argument')
            sim.job_name = args.jobname
        if not args.agree:
            print('Do you agree to the DandeLiion Cloud Platform\'s Terms of Service '
                  + '<https://simulation.dandeliion.com/tos/>?')
            answer = input(" yes or [no]? ")
            if not answer or answer.lower() not in ['y', 'yes']:
                raise Exception('Aborted submission due to lack of agreement of ToS')

        sim.agree = True
        Queue.submit(sim)
    except Exception as e:
        print('Submission FAILED!', str(e))
        return sys.exit(1)  # error code

    print(f"Simulation SUCCESSFULLY submitted (id: {sim.pk})")


def list():

    parser = argparse.ArgumentParser(description='Show Dandeliion simulation queue.')
    parser.add_argument(
        '--queue',
        default=None,
        help='specify queue to list (default: all)'
    )
    parser.add_argument(
        '--job',
        default=None,
        help='specify job to list (default: all)'
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
        print(f"Listing job(s) queued/running on {args.queue if args.queue else 'all queues'}")
        queue = Queue.list(
            queue=args.queue,
            pk=args.job
        )
        queue.reverse()
        print(queue)
    except Exception as e:
        print('Listing queue FAILED!', str(e))
        return sys.exit(1)  # error code


def cancel():

    parser = argparse.ArgumentParser(description='Cancel Dandeliion simulation.')
    parser.add_argument(
        'id',
        metavar='JOB_ID',
        help='simulation job id'
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
        Queue.cancel(sim)
    except Exception as e:
        print('Cancellation FAILED!', str(e))
        return sys.exit(1)  # error code

    print(f"Simulation successfully cancelled (#:{args.id})")
