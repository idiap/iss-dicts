#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Alexandre Nanchen"
__version__ = "Revision: 1.0"
__date__ = "Date: 2012/11/15"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "Python"


usage="""
 Helper functions to process BDlex50 lexicon.

"""

import os, sys

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../common")

from ioread import Ioread

###########################
#Constants
#

graphemeCodes={u"e1" : u"é", "a2" : u"à", "e2" : u"è", "u2" : u"ù", "a3" : u"â", "e3" : u"ê", "i3" : u"î", 
               "o3" : u"ô", "u3" : u"û", "a4" : u"ä", "e4" : u"ë", "i4" : u"ï", "u4" : u"ü", "c5" : u"ç" }

optionalCodes={"(j)" : "", "(t)" : "", "(6R)" : "", "(i)" : "", "(tS)" : "", "(s)" : "", "(ei)" : "", 
 			   "(Ei)" : "", "(kt)" : "", "(k)" : "", "(au)" : "", "(d)" : "", "(l)" : "", "(f)" : "", 
			   "(dZ)" : "", "(x)" : "", "(ai)" : "", "(g)" : "", "(6n)" : "", "(b)" : "" }

###########################
#Functions
#

def normaliseGraphemes(cg):
	"""Substitute graphemes codes"""

	currentGraphemes = cg
	utf8 = ""

	for c in graphemeCodes.keys():
		utf8 = graphemeCodes[c]
		currentGraphemes = currentGraphemes.replace(c, utf8)		

	return currentGraphemes


def normaliseOthers(cp):
	"""Substitute * and " """

	currentPhonemes = cp
	currentPhonemes = currentPhonemes.replace("*","")
	currentPhonemes = currentPhonemes.replace('"','')				

	return currentPhonemes


def expandOptionalPhonemes(cp): 
	"""Remove the optional parentheses"""

	currentPhonemes = cp
	currentPhonemes = currentPhonemes.replace("(","")
	currentPhonemes = currentPhonemes.replace(")","")

	return currentPhonemes


def removeOptionalPhonemes(cp): 
	"""Substitute optional phoneme code"""

	currentPhonemes = cp
	optionCode = ""

	for c in optionalCodes.keys():
		optionCode = optionalCodes[c]
		currentPhonemes = currentPhonemes.replace(c, optionCode)		

	return currentPhonemes


