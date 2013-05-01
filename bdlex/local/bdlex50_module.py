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

import os, sys, re

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../common")

from ioread import Ioread

###########################
#Constants
#

graphemeCodes={u"e1" : u"é", "a2" : u"à", "e2" : u"è", "u2" : u"ù", "a3" : u"â", "e3" : u"ê", "i3" : u"î",
               "o3" : u"ô", "u3" : u"û", "a4" : u"ä", "e4" : u"ë", "i4" : u"ï", "u4" : u"ü", "c5" : u"ç" }

optionalCodes={"\(~\)" : ["~",""], ## vowel is optionally nasalised
               "\(j\)" : ["j",""], ##
               "\(t\)" : ["t", ""], ##
               "@"   : ["ax",""], ## optional schwa
               "\(6R\)": ["6R", "ER"], ## variants for english words
               "\(i\)" : ["i", ""],
               "\(tS\)": ["tS", "S"], ## e.g. in 'lunch'
               "\(s\)" : ["s", ""],
 			   "\(Ei\)": ["Ej", "Ei", "E", "e"], ## e.g. in 'baby'
               "\(kt\)": ["kt", "t", "k", ""], ## e.g. in suspect
               "\(k\)" : ["k",""],
               "\(au\)": ["ou","au","u"], ## e.g. in 'out'
               "\(d\)" : ["d", ""], ## very rare
               "\(l\)" : ["l", ""], ## quite rare, e.g. 'fusil'
               "\(f\)" : ["f", ""], ## quite rare, e.g. in 'cerf'; although maybe also in 'chef' in 'chef d'oeuvre'
			   "\(dZ\)": ["dZ", "Z"], ## because French pronounce 'g' and 'j' quite differently from other languages
               "\(x\)" : ["R", "Z"], ## fricative uvulaire, does not exist natively in French
               ## if you wish to keep uvular fricative, use this: "\(x\)" : ["x", "R", "Z"],
               "\(ai\)": ["aj", "ai", "i"], ## e.g. in 'bye'
               "\(g\)" : ["g", ""], ## e.g. in 'joug'
               "\(6n\)": ["6n", "En"],
               "\(b\)" : ["b", ""] }

###########################
#Functions
#

def normaliseGraphemes(cg):
	"""Substitute graphemes codes"""

	currentGraphemes = cg.lower()
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
    """Generate all possible variants of the pronunciation"""

    currentPhonemes = [cp]
    newt = True
    while newt:
        newt = False
        repl = []
        for w in currentPhonemes:
            # ugly hack to check whether the word needs expanding
            if len(re.split('[@(]', w)) == 1:
                if (not w in repl):
                  repl.append(w)
            else:
                for i in optionalCodes.keys():
                    for j in optionalCodes[i]:
                        newstr = re.sub(i, j, w)
                        if (newstr != w) and (not newstr in repl):
                            repl.append(newstr)
        if len(repl) > len(currentPhonemes):
            newt = True
            currentPhonemes = repl
    # restore schwas in a rather ugly way
    for i in range(len(repl)):
        repl[i] = repl[i].replace('ax', '@')
    return repl


def removeOptionalPhonemes((cp, liaison)):
	"""Substitute optional phoneme code"""

	currentPhonemes = cp
	optionCode = ""

	for c in optionalCodes.keys():
		optionCode = optionalCodes[c]
		currentPhonemes = currentPhonemes.replace(c, optionCode)

	return currentPhonemes
