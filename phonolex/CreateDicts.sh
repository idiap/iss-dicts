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
htkDict=dictionary.txt
htkDict6=dictionary-6.txt

echo "Converting to UTF8"
iconv --from-code=ISO-8859-1 --to-code=UTF-8 $sourceDict > $sourceConv

echo "Preparing $htkDict"
./prepare_phonolex.py $sourceConv $tempDict
cat $tempDict | sort | uniq > $htkDict
echo "Dictionary $htkDict: done."

echo "Preparing $htkDict6 (include diphthongs ending in 6)"
./prepare_phonolex.py $sourceConv $tempDict -6
cat $tempDict | sort | uniq > $htkDict6
echo "Dictionary $htkDict6: done."
rm $sourceConv $tempDict 
