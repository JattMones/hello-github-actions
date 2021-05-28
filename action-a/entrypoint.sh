#!/bin/sh -l

sh -c "echo action-a & workflow created by $INPUT_MY_NAME"
sh -c "pytest"
