#!/usr/bin/env bash

if [ -n "$PY_STAGED" ];
then
	flake8 $PY_STAGED
  isort --check-only --diff --recursive $PY_STAGED
fi
