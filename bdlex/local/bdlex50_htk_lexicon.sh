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
 This script build an HTK formatted lexicon from the
 BDLex50 lexicon. It does not expand group of optional
 phonemes. For that use the run_bdlex50_expand_optionals.sh
 script.

 Parameters are:

   - input file        : BDLex50 lexicon without optional phonemes
   - output file       : name of the HTK outputed lexicon
   - phoneme set only  : 1 or 0 

"

die () {
    echo -e >&2 "$@"
    exit 1
}

#Parameter checking
[ "$#" -eq 3 ] || die "3 arguments required, $# provided\n\nUsage: $0 'BDLex50 lexicon' 'output lexicon name' 'phoneme set only'\n$usage"


cwd=`pwd`
scriptDir=`dirname $0`

bdlex50Lexicon=$1
outputLexicon=$2
phonemeSetOnly=$3

###########################
#Module
#

source bdlex50_module.sh

###########################
#Functions
#

function outputLexiconEntryAsHTK() { #@ usage: output one BDLex50 entry as HTK format.
                                     #         It groups nazalisation symbols with the
                                     #         previous characters.
	local g=$1 #Graphemes
	local p=$2 #Phonemes
	local temp
	local currentPhone
	
	[ $phonemeSetOnly -eq 1 ] || printf "%s   " "$g"

	#Loop through each phonemes
	while [ -n "$p" ]
	do
		temp=${p#?}             #remove first character
		char1=${p%"$temp"}      #extract first character

		[ $char1 == "(" ] && die "Illegal character: $1 $2"
		[ $char1 == "~" ] && die "First character cannot be a ~ $1 $2"

		#Ready for next character
		p=$temp

		if [ -n "$p" ]          #some phonemes left?
		then
		
			temp=${p#?}         #remove first character
			char2=${p%"$temp"}  #extract first character

			#The character is a nazalisation symbol
			if [ "$char2" == "~" ]
			then
				printf -v currentPhone " %s%s" "$char1" "$char2"
				phonemesSet[$currentPhone]=$currentPhone

				#Don't take nazalisation symbol as next letter
				p=$temp
			else
				printf -v currentPhone " %s" "$char1"
				phonemesSet[$char1]=$char1
			fi

		else
			printf -v currentPhone " %s" "$char1"
			phonemesSet[$char1]=$char1
		fi

		[ $phonemeSetOnly -eq 1 ] || printf "$currentPhone"

	done
	
	[ $phonemeSetOnly -eq 1 ] || printf "\n"	
}

###########################
#Main program
#

declare -A phonemesSet

while IFS=';' read graphemes phonemes remainder
do

	normaliseGraphemes $graphemes
	normaliseOthers $phonemes

	outputLexiconEntryAsHTK $_currentGraphemes $_currentPhonemes

done < $bdlex50Lexicon > $outputLexicon

echo ${phonemesSet[@]}

