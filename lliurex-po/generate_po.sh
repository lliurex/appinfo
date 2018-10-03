#!/bin/bash

PYTHON_FILES="../src/*.py"

mkdir -p appinfo/

xgettext $PYTHON_FILES -o appinfo/appinfo.pot
