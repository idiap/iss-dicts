#!/usr/bin/env bash

#
# Copyright 2012 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Alexandre Nanchen, December 2012
#

# Common constants and functions to build an HTK lexicon from the
# BDLex50 lexicon.
 

###########################
#Constants
#

declare -A graphemeCodes=( [e1]="é" [a2]="à" [e2]="è" [u2]="ù" [a3]="â" [e3]="ê" [i3]="î" 
                           [o3]="ô" [u3]="û" [a4]="ä" [e4]="ë" [i4]="ï" [u4]="ü" [c5]="ç" )

declare -A optionalCodes=( [(j)]="" [(t)]="" [(6R)]="" [(i)]="" [(tS)]="" [(s)]="" [(ei)]="" 
						   [(Ei)]="" [(kt)]="" [(k)]="" [(au)]="" [(d)]="" [(l)]="" [(f)]="" 
						   [(dZ)]="" [(x)]="" [(ai)]="" [(g)]="" [(6n)]="" [(b)]="" )

###########################
#Globals
#

_currentGraphemes=""
_currentPhonemes=""


###########################
#Functions
#

function normaliseGraphemes() { #@ usage: substitute graphemesCodes

	_currentGraphemes=$1
	local utf8

	for c in ${!graphemeCodes[@]}
	do
		utf8=${graphemeCodes[$c]}
		_currentGraphemes=${_currentGraphemes//$c/$utf8}		
	done
}

function normaliseOthers() { #@ usage: substitute * and "

	_currentPhonemes=$1
	_currentPhonemes=${_currentPhonemes//\*/}
	_currentPhonemes=${_currentPhonemes//\"/}				
}

function removeOptionalPhonemes() { #@ usage: substitute optional phonemeCode

	_currentPhonemes=$1	
	local optionCode

	for c in ${!optionalCodes[@]}
	do
		optionCode=${optionalCodes[$c]}
		_currentPhonemes=${_currentPhonemes//$c/$optionCode}		
	done		
}

function expandOptionalPhonemes() { #@ usage: remove the optional parentheses

	_currentPhonemes=$1	
	_currentPhonemes=${_currentPhonemes//(/}
	_currentPhonemes=${_currentPhonemes//)/}
}

