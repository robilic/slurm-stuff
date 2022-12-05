#!/bin/bash

if [ -z $1 ]
then
        echo "No job specified, listing all."
        squeue --states=R --format="%i %U %C %D" | sort -k3 -n
        exit 0
else
        echo "Checking job ${1}..."
        JOB_INFO=`squeue -j $1 -h --format="%i %U %C %D"`
        JOB_ID=`echo $JOB_INFO | awk '{ print $1 }'`
        USER_ID=`echo $JOB_INFO | awk '{ print $2 }'`
        CORE_COUNT=`echo $JOB_INFO | awk '{ print $3 }'`
        NODE_COUNT=`echo $JOB_INFO | awk '{ print $4 }'`
fi

JOB_HOSTS=`scontrol show hostnames $(squeue -j $JOB_ID --format="%N" --noheader)`

CPU_THRESHOLD=5
TOTAL_CPU=0

for h in $JOB_HOSTS; do
        # Get processes using greater than desired % of CPU
        CPU_COUNT=$(ssh $h "top -b -H -n 1 -u $USER_ID | tail -n +8 | awk '{ if (\$9 > $CPU_THRESHOLD) print \$9 }' | wc -l")
        TOTAL_CPU=$(($TOTAL_CPU + $CPU_COUNT))
done

echo "Found $TOTAL_CPU processors being utilized compared to $CORE_COUNT requested"
