#!/bin/bash
#
# This script installs packages to nodes in bulk. You can install to vis,
# cpu, gpu, or all nodes. List packages to install after the node type.
#
# Usage:
#
# $ ./builk_install.sh vis|gpu|cpu|all [ packagename ... ]
#

nodes=""
packages=`echo $@ | sed 's/[^ ]* *//'`

# gather all the nodes based on the type selected
if [[ $1 =~ ^(vis|all)$ ]]
then
  nodes="$nodes `sinfo -h -p interactive -N -o '%N' | tr '\n' ' '`"
fi

if [[ $1 =~ ^(gpu|all)$ ]]
then
  nodes="$nodes `sinfo -h -p gpu -N -o '%N' | tr '\n' ' '`"
fi

if [[ $1 =~ ^(cpu|all)$ ]]
then
  nodes="$nodes `sinfo -h -p batch -N -o '%N' | tr '\n' ' '`"
fi

# do the installs
for n in $nodes
do
  ssh $n yum install -y $packages
done
