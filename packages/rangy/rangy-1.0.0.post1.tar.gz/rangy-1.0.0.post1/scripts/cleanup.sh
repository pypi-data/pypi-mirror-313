#! /usr/bin/env shell
# deletes all empty directories in the current directory``
find . -type d -empty -delete
# removes python cache files
find . -name __pycache__ -type d -exec rm -r {} +