#!/bin/bash

if [ -z $1 ]; then
  echo "Usage: run.sh [static-forwarding|learning-switch]"
  exit
fi

cp $1.py helpers.py ~/pyretic/pyretic/modules
pushd ~/pyretic
python pyretic.py -m p0 pyretic.modules.$1
popd
