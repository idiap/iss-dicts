#!/usr/bin/env bash

#
# Copyright 2012 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Alexandre Nanchen, December 2012
#

usage="\n
 This script expand optional phonemes from a BDLex50
 lexicon file. Optional phonemes are a sequence of phonemes
 enclosed with parentheses.

 i.e. (i), (6R)

 Parameters are:

   - input file name: BDLex50 lexicon file
   - output file name: where to output
   
"

die () {
    echo -e >&2 "$@"
    exit 1
}

#Parameter checking
[ "$#" -eq 2 ] || die "2 arguments required, $# provided\n\nUsage: $0 'input file name' 'output file name'\n$usage"


cwd=`pwd`
scriptDir=`dirname $0`

bdlex50Lexicon=$1
outputFileName=$2

###########################
#Constants
#

source bdlex50_module.sh


###########################
#Main program
#

while IFS=';' read graphemes phonemes remainder
do
	#We keep the optional phonemes
	expandOptionalPhonemes $phonemes
	
	printf "%s;%s;%s\n" "$graphemes" "$_currentPhonemes" "$remainder"

	removeOptionalPhonemes $phonemes

	#Another pronunciation without optional phonemes
	if [ $phonemes != $_currentPhonemes ]
	then	
		printf "%s;%s;%s\n" "$graphemes" "$_currentPhonemes" "$remainder"
	fi

done < $bdlex50Lexicon > $outputFileName

