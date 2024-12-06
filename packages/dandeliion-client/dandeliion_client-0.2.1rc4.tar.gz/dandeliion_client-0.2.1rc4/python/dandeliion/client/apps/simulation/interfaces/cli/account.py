import argparse
import sys
from .connection import connect


def info():

    parser = argparse.ArgumentParser(description='Show account details')
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

        print("Account details")
        print("===============")
        print("<TODO>")

    except Exception as e:
        print('FAILED to fetch account details!', str(e))
        return sys.exit(1)  # error code
