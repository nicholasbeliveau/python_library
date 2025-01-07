#!/bin/bash

CUR_DIR=$(dirname "$0")

if [ ! -d "${CUR_DIR}/venv" ] ; then
  ## Setup virtual environment
  python3 -m venv "${CUR_DIR}/venv"
  . "${CUR_DIR}/venv/bin/activate"
  pip3 install -r "pandas"
else
  . "${CUR_DIR}/venv/bin/activate"
fi

"${CUR_DIR}/nypa_preprocessing.py" "$@"
