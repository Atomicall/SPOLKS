#!/bin/bash

#source venv/bin/activate

export PYTHONPATH=$(pwd):$(pwd)/client_package:$(pwd)/server_package:$(pwd)/shared:$PYTHONPATH
