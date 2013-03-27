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

# This step is only necessary for the shell-based method
echo Expanding optional phones to $tmp2
./bdlex50_expand_optionals.sh $tmp1 $tmp2

echo Converting to HTK format as B50.dct
sort -u $tmp2 > $tmp3
./bdlex50_htk_lexicon.sh $tmp3 B50.dct
#./bdlex50_htk_lexicon.py $tmp1 B50.dct

rm -f $tmp1 $tmp2 $tmp3
