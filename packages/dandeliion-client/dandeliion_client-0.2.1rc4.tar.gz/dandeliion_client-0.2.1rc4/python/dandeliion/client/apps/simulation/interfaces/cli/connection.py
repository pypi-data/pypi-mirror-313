from ..http_requests import REST_API
from dandeliion.client.config import DANDELIION_SERVER
import argparse
import json
import sys
import os
from os import path


def login():

    parser = argparse.ArgumentParser(description='Connect to Dandeliion server')
    parser.add_argument(
        '-u',
        '--username',
        help='Dandellion username'
    )
    parser.add_argument(
        '-p',
        '--password',
        default=None,
        help='Dandellion password'
    )
    parser.add_argument(
        '-c',
        '--credentials',
        metavar='CRED_FILE',
        default=None,
        help='path to a Dandeliion credential file'
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true'
    )
    args = parser.parse_args()

    try:
        if args.password:
            credentials = {
                'username': args.username,
                'password': args.password,
            }
            auth_type = 'password'
        else:
            credentials = {}
            auth_type = 'interactive'

        print(f'Connecting to {DANDELIION_SERVER}...')
        client = REST_API.connect(auth_type=auth_type, credentials=credentials)

        cred_filename = args.credentials if args.credentials else os.environ.get('DANDELIION_CREDENTIALS', None)
        if not cred_filename:
            raise Exception('You must provide the location for the credential file either as an argument'
                            + ' or in the environment variable DANDELIION_CREDENTIALS.')
        if path.exists(cred_filename) and not args.force:
            print(f"File '{cred_filename}' already exists!\n")
            answer = input("Do you want to replace it with the new credential file? yes or [no]? ")
            if not answer or answer.lower() not in ['y', 'yes']:
                raise Exception('Aborted Login and original credential file was not replaced')
        print('Writing/updating credential file... '
              + f'(Make sure that the folder where the credential file is stored [{cred_filename}] '
              + 'is only readable by yourself!)')
        with open(cred_filename, "w") as cred_file:
            json.dump({
                'username': client._connector._credentials['username'],
                'token': client._connector._get_token(),
            }, cred_file)
        print(f"Login SUCCESSFUL! Logged in as user '{client._connector._credentials['username']}'.")

    except Exception as e:
        print('Login FAILED!', str(e))
        sys.exit(1)


def connect(credentials=None):

    cred_filename = credentials if credentials else os.environ.get('DANDELIION_CREDENTIALS', None)

    if cred_filename:
        with open(cred_filename) as cred_file:
            credentials = json.load(cred_file)
            auth_type = 'import'
    else:
        credentials = None
        auth_type = None

    REST_API.connect(auth_type=auth_type, credentials=credentials)
