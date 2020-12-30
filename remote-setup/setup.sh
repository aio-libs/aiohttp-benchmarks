#!/usr/bin/env bash

set -x
set -e
sudo apt-get update

sudo apt-get install -y software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install -y postgresql-client postgresql postgresql-contrib postgresql-server-dev-all

sudo apt-get install -y python3-pip python3-dev python3-psycopg2 virtualenv
THIS_DIR=`dirname "$0"`

for PYV in 7 8 9
do
    sudo apt-get install -y python3.${PYV} python3.${PYV}-dev
    if [ ! -d ~/env3${PYV} ]; then
      virtualenv -p /usr/bin/python3.${PYV} ~/env3${PYV}
    fi
    ~/env3${PYV}/bin/python -m pip install -r ${THIS_DIR}/requirements.txt
done

export PGPASSWORD=benchmarks
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$PGPASSWORD';"
psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS hello_world"
psql -h localhost -U postgres -c "CREATE DATABASE hello_world"
psql -h localhost -U postgres -d hello_world -f ${THIS_DIR}/data.sql

cp ${THIS_DIR}/serve.py ~/
