#!/bin/bash

cpulimit --path /usr/bin/python3.8 --limit 600 --background

/usr/bin/python3.8 /app/run.py