#!/usr/bin/env bash

coverage run --source regis -m unittest discover  -v . "*_test.py"
coverage html
open htmlcov/index.html