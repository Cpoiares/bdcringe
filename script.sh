#!/bin/bash
set -e
SCRIPT=`basename ${BASH_SOURCE[0]}`

if [[ "$1" == 'help' ]]; then
  echo -e "Basic usage: ./$SCRIPT init"\\n
elif [[ "$1" == 'init' ]]; then
  docker run --name bd -p 5432:5432 -d postgres:alpine
  sleep 5
  psql -h localhost -p 5432 -U postgres -f script.sql
elif [[ "$1" == 'new' ]]; then
  docker run --name bd -p 5432:5432 -d postgres:alpine
elif [[ "$1" == 'start' ]]; then
  docker start bd
elif [[ "$1" == 'rm' ]]; then
  docker stop bd && docker rm bd
elif [[ "$1" == 'stop' ]]; then
  docker stop bd
fi
