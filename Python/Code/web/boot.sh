#! /usr/bin/env bash

gunicorn_django --workers=1 --log-level=info --bind 0.0.0.0:10001
