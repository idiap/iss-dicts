#!/bin/zsh
#
# Copyright 2013 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, April 2013
#
source ../Common.sh
chdir local

# Submit to a multithreading queue that has 4 threads (with max 8GB
# each) adding up to 32GB total.  We need the memory, not the threads.
export USE_GE=1
export GE_OPTIONS="-l q1dm -pe pe_mth 4"

rm -f job-file
export IN_DICT=dictionary.txt
create-phsaurus.sh
