#!/bin/bash
rm ./logs/*
export PYTHONPATH=../lib
python3 ./compileplats.py $1
