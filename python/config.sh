#!/bin/bash

source venv/bin/activate

export PYTHONHOME=$(pwd):$(pwd)/client_package:$(pwd)/server_package:$(pwd)/shared:$PYTHONHOME
