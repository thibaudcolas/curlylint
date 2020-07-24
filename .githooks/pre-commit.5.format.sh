#!/usr/bin/env bash
# Format and re-stage fully staged files only.

if [ -n "$PRETTIER_FULLY_STAGED" ];
then
  npx prettier --write $PRETTIER_FULLY_STAGED
  git add $PRETTIER_FULLY_STAGED
fi

if [ -n "$PRETTIER_STAGED" ];
then
  npx prettier --check $PRETTIER_STAGED
fi

if [ -n "$PY_FULLY_STAGED" ];
then
  black $PY_FULLY_STAGED
  git add $PY_FULLY_STAGED
fi

if [ -n "$PY_STAGED" ];
then
	black --check $PY_STAGED
fi
