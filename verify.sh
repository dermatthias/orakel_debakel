#!/bin/bash
if [ "$1" == "" ]
then
    echo "Usage: verify.sh <gameday>"
else
    orakel/orakel.py $1 2009 | ./main.py --verify $1
fi
