#!/bin/bash
if [ "$1" == "" ]
then
    echo "Usage: predict.sh <gameday>"
else
    orakel/orakel.py $1 2009 | ./main.py --predict $1
fi
