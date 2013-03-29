#!/bin/zsh
#
# Copyright 2011 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Milos Cernak, November 2012
#   Phil Garner, March 2013
#
cd local

phonolexdict=../media
sourceDict=$phonolexdict/phonolex
sourceConv=phonolex.utf8.txt
tempDict=phonolex.temp
htkDict=phonolex.dct
htkDict6=phonolex-6.dct

echo "Converting to UTF8"
iconv --from-code=ISO-8859-1 --to-code=UTF-8 $sourceDict > $sourceConv

echo "Preparing phonolex"
./prepare_phonolex.py $sourceConv $tempDict
cat $tempDict | sort | uniq > $htkDict
echo "Dictionary $htkDict: done."

echo "Preparing phonolex-6"
./prepare_phonolex.py $sourceConv $tempDict -6
cat $tempDict | sort | uniq > $htkDict6
echo "Dictionary $htkDict-6: done."
rm $sourceConv $tempDict 
