#!/usr/bin/env bash

# first connect and create credentials
export DANDELIION_CREDENTIALS=./my_creds
dandeliion-connect

# get list of existing simulations and take id of latest/last one
sim_id=`dandeliion-queue | tail -n 1 | awk '{print $1}'`
echo "Found latest simulation (id:${sim_id})"

# export the parameters as a BPX file
dandeliion-export ${sim_id} -o test_bpx.json

# fetch result file and extract dandeliion parameter file
dandeliion-results ${sim_id} -o data.zip
unzip -p data.zip parameters.json > test_parameters

# submit a new simulation using these parameters
dandeliion-submit ./test_parameters --jobname='CLI submission' --agree
