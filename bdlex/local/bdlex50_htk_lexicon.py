#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Alexandre Nanchen"
__version__ = "Revision: 1.0"
__date__ = "Date: 2012/11/15"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "Python"


usage="""
 This script expand optional phonemes from a BDLex50
 lexicon file. Optional phonemes are a sequence of phonemes
 enclosed with parentheses.

 i.e. (i), (6R)

 Parameters are:

   - input file name: BDLex50 lexicon file
   - output file name: where to output

"""

import sys
import os

from bdlex50_module import *

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../common")

from ioread import Ioread

###########################
#Constants
#

SEPARATOR = ";"
GRAPHEMEINDEX = 0
PHONEMEINDEX = 1
LIAISONINDEX = 2

###########################
#Implementation
#
def readLexicon(fileName):
	"""Read BDLex50 lexicon."""

	io = Ioread()
	lines = io.readFileContentList(fileName)

	lexicon={}

	for line in lines:
		splitLine = line.split(SEPARATOR)
		lexicon[splitLine[GRAPHEMEINDEX]] = (splitLine[PHONEMEINDEX].rstrip(), splitLine[LIAISONINDEX].rstrip())

	return lexicon


def expandOptional(lexicon):
    """Optional phonemes characters are expanded.
    """
    lines=[]

    for g, (p, l) in lexicon.iteritems():
        #print p, l
        pExpanded = expandOptionalPhonemes(p + l)
        pRemoved = expandOptionalPhonemes(p)
        #print pExpanded, pRemoved
        for i in range(len(pExpanded)):
            lines.append("%s%s%s" %(g, SEPARATOR, pExpanded[i]))

        for i in range(len(pRemoved)):
            if not pRemoved[i] in pExpanded:
                lines.append("%s%s%s" %(g, SEPARATOR, pRemoved[i]))

    return lines


def normalizeAndFormatAsHTK(lines):
    """Different normalization and format.
    """
    
    for i, gp in enumerate(lines):
        
        g, p = gp.split(SEPARATOR)
        
        normGraphemes = normaliseGraphemes(g)
        normPhonemes = normaliseOthers(p)
        
        htkPhonemes = getPhonemesEntryAsHTK(normPhonemes)
        htkPhonemes = postProcessPhonemes(htkPhonemes)

        lines[i] = "%s\t%s" % (normGraphemes, htkPhonemes)

phonemeFix={u"h ":u"", u"r" : u"R", u"E~":u"e~"}

def postProcessPhonemes(phonemes):
    """ Correct the pronunciation by converting
        phones which are obviously a mistake."""
    # This is not the most efficient way, but short and clear
    for i in phonemeFix.keys():
        phonemes = phonemes.replace(i, phonemeFix[i])
    return phonemes

def getPhonemesEntryAsHTK(phonemes):
	"""Output one BDLex50 entry as HTK format.
	   It groups nazalisation symbols with the
	   previous characters.

	   arguments:
			- g: graphemes
			- p: phonemes
	"""

	#String are immutables
	p = phonemes
	htkPhonemes = ""

	#Loop through each phonemes
	#No spaces between phonemes
	while len(p) > 0:

		char1 = p[0]

		if char1 == "(" or char1 == "~":
			print "Illegal character: %s for %s and %s." % (char1, p, phonemes)
			exit(1)

		#Ready for next character
		p = p[1:]

		if len(p) > 0:

			char2 = p[0]

			if char2 == "~":
				htkPhonemes += " %s%s" %(char1, char2)

				#Ready for next character
				p = p[1:]
			else:
				htkPhonemes += " %s" % char1
		else:
			htkPhonemes += " %s" % char1

	return htkPhonemes.strip()


def outputLexicon(lines, outputName):
	"""Final htk formatted lexicon is outputed.
	"""

	strContent = "\n".join(lines)
	strContent += "\n"

	io = Ioread()
	io.writeFileContent(outputName, strContent)


###########################
#Main program
#

if __name__ == "__main__":

	if len(sys.argv) != 3:

		print usage
		print "    usage: %s 'BDLex50 lexicon file' 'output file name' " % sys.argv[0]
		print ""
		sys.exit(0)


    #Get arguments
	bdlex50Lexicon = sys.argv[1]
	outputFileName = sys.argv[2]

	print "    Read blex50 lexicon..."

	#Read original BDLex 50 lexicon as
	#a dictionary
	lexicon = readLexicon(bdlex50Lexicon)

	print "    Expand optional pronunciations..."

	#Expand optional phonemes
	#Return list of lines with graphemes-phonemes
	lines = expandOptional(lexicon)

	print "    Format as htk..."

	#Additional processing is done
	normalizeAndFormatAsHTK(lines)

	print "    Output htk formatted bdl50 lexicon..."

	#Output final htk formatted lexicon
	outputLexicon(lines, outputFileName)
