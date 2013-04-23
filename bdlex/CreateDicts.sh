#!/bin/sh
#
# Copyright 2013 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, March 2013
#
cd local
tmp1=/dev/shm/bdlex1.tmp
tmp2=/dev/shm/bdlex2.tmp
tmp3=/dev/shm/bdlex3.tmp

echo Creating monolithic dictionary $tmp1
cat ../media/BDL50/?.B50.flx > $tmp1

if false
then
    # Shell-based method
    # Slow and leaves odd symbols ('.', '_') in the phone list
    echo Expanding optional phones to $tmp2
    ./bdlex50_expand_optionals.sh $tmp1 $tmp2

    echo Converting to HTK format
    sort -u $tmp2 > $tmp3
    ./bdlex50_htk_lexicon.sh $tmp3 dictionary.txt 0
else
    # Python based method
    ./bdlex50_htk_lexicon.py $tmp1 dictionary.txt
fi
rm -f $tmp1 $tmp2 $tmp3
