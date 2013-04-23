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

# Phonetisaurus uses braces for its own format
grep -v '[{}]' cmudict_SPHINX.dct > dictionary.txt
export IN_DICT=dictionary.txt
create-phsaurus.sh
