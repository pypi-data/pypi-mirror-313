# DandeLiion python client

## Installing client (from source)

After downloading/cloning the source code, run the following in the root folder:
```bash
pip install .
```
If you want to change the default server, the client connects to, you have to update the respective URLs in `python/dandeliion/client/config.py`

## creating/managing credentials file
While it is possible to enter a username and password for authentication to connect to the server (has to be done for every python session/CLI command), you
can also create and then use a credentials file by running the following command on the CLI
```bash
dandeliion-connect
```
and enter the requested information when asked to. This creates a credentials file that can then be used for a more convenient way to authenticate within a python script
or during a CLI command execution (if you select the default location, it will automatically pick up the file, otherwise you will have to point the command to the file you want to
use using the `-c` argument.

## running tests
All tests and linting can be run through `tox` with (makes an isolated python environment for testing):
```bash
tox
```

Or run in your local python environment with:
```bash
pytest
```

Or locally with coverage:
```bash
coverage run -m pytest
coverage report
```

## Running the client

### python module
Please check the Jupyter notebook in `examples/example.ipynb` for an overview on how to interact with the dandeliion services using the python module.

### Command-line interface
The following commands currently exists on the CLI:
| command        | description         |
| --------------- |----------------|
| dandeliion-connect | creates/updates credential file |
| dandeliion-account | shows details of current account |
| dandeliion-queue   | lists queue on server     |
| dandeliion-submit | submits new simulation run    |
| dandeliion-cancel | cancels a requested simulation run     |
| dandeliion-results | downloads results for a simulation |
| dandeliion-export | exports BPX parameters for a simulation |

For more details on their syntax/available arguments, please use their `-h` argument to access this information. Additionally, an example (bash) script can be found at `examples/example.sh`.
