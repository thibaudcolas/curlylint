#!/usr/bin/env bash

if [ -n "$PY_STAGED" ];
then
	flake8 $PY_STAGED
  mypy $PY_STAGED
fi
