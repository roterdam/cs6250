#!/bin/bash


# First, push the bind configuration file where it belongs
sudo mv /etc/bind/named.conf.options /etc/bind/named.conf.options.orig
sudo cp bind/* /etc/bind/

# Second, update ryu installation.
pushd ryu-update
./update-ryu-dns.sh /home/mininet/pyretic/pyretic/vendor/ryu
popd
