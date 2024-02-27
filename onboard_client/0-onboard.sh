#!/bin/bash
rm ./logs/*
export PYTHONPATH=./lib
python3 ./onboard.py $1
