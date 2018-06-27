#!/bin/bash
# set n to 1
n=0

while [ $n -le 3600 ]
do
	date >> ps_out.txt
	ps aux | sort -nrk 4 | head -10 >> ps_out.txt
	n=$((n+1))
	sleep 1
done
