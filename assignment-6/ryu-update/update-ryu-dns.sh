#!/bin/bash

if [ -z $1 ]; then
  echo "Usage: update-ryu-dns.sh [location of Ryu]"
  exit
fi

cp dns.py $1/ryu/lib/packet/dns.py
cp test_dns.py $1/ryu/tests/unit/packet/test_dns.py

# Saved a backup of __init__.py, just in case.
sed -i.bak 's/)/, dns)/' $1/ryu/lib/packet/__init__.py

