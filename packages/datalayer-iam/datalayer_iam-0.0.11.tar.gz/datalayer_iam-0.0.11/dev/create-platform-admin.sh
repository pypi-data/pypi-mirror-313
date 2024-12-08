#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

export YELLOW='\x1b[33m'
export RESET='\x1b[0m'

echo
echo -e $YELLOW"Creating Platform Admin User in Solr collection $COLLECTION"$RESET
echo

USERNAME=$1
PASSWORD=$2

datalayer-iam create-platform-admin $USERNAME $PASSWORD

datalayer-iam list-users
