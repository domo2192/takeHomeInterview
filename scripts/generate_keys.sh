#!/bin/bash

echo "Generating SSH keys for legacy system communication..."

mkdir -p local-server/ssh_keys
mkdir -p remote-server-1/ssh_keys

ssh-keygen -t rsa -b 2048 -f local-server/ssh_keys/id_rsa -N "" -C "system-stability-challenge"

cp local-server/ssh_keys/id_rsa.pub remote-server-1/ssh_keys/

chmod 600 local-server/ssh_keys/id_rsa
chmod 644 local-server/ssh_keys/id_rsa.pub
chmod 644 remote-server-1/ssh_keys/id_rsa.pub

echo "SSH keys generated and copied successfully!"
echo ""
echo "Files created:"
echo "  local-server/ssh_keys/id_rsa"
echo "  local-server/ssh_keys/id_rsa.pub"
echo "  remote-server-1/ssh_keys/id_rsa.pub"