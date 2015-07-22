#!/bin/bash

# Makes sure that bind9 isn't running for everyone.
sudo service bind9 stop
sudo python topo.py
