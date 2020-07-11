#!/usr/bin/env bash

if [ -n "$PY_STAGED" ];
then
	make test
fi
