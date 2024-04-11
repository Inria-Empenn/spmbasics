#!/bin/bash
# finds the nifti file according to extension sorts alphabetically and prints shasums
# works on the given directory
# usage bash checksummer.sh
find . -type f -name "*.nii" -print0 | sort -z | xargs -r0 sha256sum > sha256SumOutput