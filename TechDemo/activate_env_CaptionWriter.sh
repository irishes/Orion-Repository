#!/bin/sh
_CONDA_ROOT=$CONDA_PREFIX
. "$_CONDA_ROOT/etc/profile.d/conda.sh" || return $?
_conda_activate "$@"
python3 ISSS.py
