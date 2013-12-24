#!/bin/zsh
#
# Copyright 2013 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, November 2013
#
source ../Common.sh
chdir local

csvDir=~/walliserdeutsch/dict

./lexicon.rb -p dictionary.txt $csvDir/*.csv
dict-man.rb -p phones.txt dictionary.txt
