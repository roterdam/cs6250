#!/bin/bash

#if [ -z $1 ]; then
#    echo "Usage: run-firewall.sh <firewall config file>"
#    exit
#fi

PYTHONPATH=/home/mininet/pyretic:/home/mininet/mininet:/home/mininet/pox:/home/mininet/pyretic/pyretic/vendor/ryu
cp dns_amplification_prevention.py ~/pyretic/pyretic/modules
cp pyretic_switch.py ~/pyretic/pyretic/modules
cp firewall.py ~/pyretic/pyretic/modules
cp dns_firewall.py ~/pyretic/pyretic/modules
pushd ~/pyretic
python pyretic.py -m p0 pyretic.modules.dns_amplification_prevention
popd
