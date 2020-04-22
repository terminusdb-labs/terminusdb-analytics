#!/bin/bash

pip install terminus-client-python

./docker_stats.py terminusdb/terminus-server
./fetch_stars.py terminusdb/terminus-server

