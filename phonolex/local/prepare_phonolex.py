#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Copyright 2012 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# This script post-process phonolex dictionary for further usage in ASR
#
# Author(s):
#   Milos Cernak, November 2012
#   Alexandros Lazaridis, March 2012
#   Phil Garner, March 2012
#

import os, sys, re, string

nargs = len(sys.argv)
if nargs < 3:
  print "usage: %s phonolex.orig phonolex.htk.txt" % os.path.basename(sys.argv[0])
  sys.exit()

input = open(sys.argv[1], 'r')
phtrain = open(sys.argv[2], 'w')

# -6 (diph = True) means "join distinct phones into 14 new
# diphthongs".  Normally we don't want this as it's worse for ASR, but
# it may be necessary for TTS.
diph = False
if nargs > 3 and sys.argv[3] == '-6':
  diph = True

phoneset=['@','2','2:','6','9','a','a~','a~:','a:','aI','aU','b','C','d','e','e~','e:','E','E~','E~:','E:','f','g','h','i','i:','I','j','k','l','m','n','N','o','o~','o~:','o:','O','O:','OY','p','Q','r','R','s','S','t', 'ts', 'tS', 'pf','u','u:','U','v','x','y','y:','Y','z','Z']

if diph:
  phoneset += ['aU6', 'aI6', 'i:6', 'y:6', 'u:6', 'I6', 'U6', 'e:6', '2:6', 'o:6', 'E6', 'E:6', '96', 'O6', 'a6', 'a:6']

def conformPhoneset(i):
  retVal=0
  for p in phoneset:
    if i == p:
      retVal=1

  return retVal


word=''
i=1
try:
  for line in input:
    # 1st line: word
    if i == 1:
      # convert umlauts
      line = line.replace("\"a", "ä")
      line = line.replace("\"o", "ö")
      line = line.replace("\"u", "ü")
      line = line.replace("\"A", "ä")
      line = line.replace("\"O", "ö")
      line = line.replace("\"U", "ü")
      #remove morfeme boundary marker
      line = line.replace("+","")
      #remove spelling symbol '$'
      line = line.replace("$","")
      #remove non-spelling letter symbol '/'
      line = line.replace("/","")
      #remove symbol '"'
      line = line.replace("\"","")
      text = line.lower()

      word=text.strip()
      i=2
    elif i == 2:
      # 2nd line: metadata
      i=3
    elif i== 3:
      # 3rd line: transcription
      #remove morfeme boundary marker
      line = line.replace("+","")
      #remove compound boundary marker
      line = line.replace("#","")
      #remove primary and secondary stress
      line = line.replace("\"","")
      line = line.replace("\'","")
      #split
      phonemes = ""
      for ph in line.strip():
        phonemes += ph + " "
      # correct transcription
      phonemes = phonemes.replace(" :",":")
      phonemes = phonemes.replace(" ~","~")
      phonemes = phonemes.replace("a I","aI")
      phonemes = phonemes.replace("a U","aU")
      phonemes = phonemes.replace("O Y","OY")
      phonemes = phonemes.replace("W","w")
      phonemes = phonemes.replace("O~","o~")
      phonemes = phonemes.replace("D","d")
      phonemes = phonemes.replace("T","t")
      phonemes = phonemes.replace("o:~","o~:")
      phonemes = phonemes.replace("::",":")
      phonemes = phonemes.replace("I:","i:")
      phonemes = phonemes.replace("L","l")
      phonemes = phonemes.replace("p f","pf")
      phonemes = phonemes.replace("t s","ts")
      phonemes = phonemes.replace("t S","tS")
      if diph:
        phonemes = phonemes.replace("i: 6","i:6")
        phonemes = phonemes.replace("y: 6","y:6")
        phonemes = phonemes.replace("u: 6","u:6")
        phonemes = phonemes.replace("I 6","I6")
        phonemes = phonemes.replace("U 6","U6")
        phonemes = phonemes.replace("e: 6","e:6")
        phonemes = phonemes.replace("2: 6","2:6")
        phonemes = phonemes.replace("o: 6","o:6")
        phonemes = phonemes.replace("E 6","E6")
        phonemes = phonemes.replace("E: 6","E:6")
        phonemes = phonemes.replace("9 6","96")
        phonemes = phonemes.replace("O 6","O6")
        phonemes = phonemes.replace("a 6","a6")
        phonemes = phonemes.replace("a: 6","a:6")
        phonemes = phonemes.replace("aU6","a U6")
        phonemes = phonemes.replace("aI6","a I6")
      phonemes = phonemes.replace("G","g")

      writeout=0
      if word != "":
        if not re.search(r"[\<|\#]",word):
          phns=phonemes.split()
          filtered_phns=[i for i in phns if conformPhoneset(i)]
          if len(phns) == len(filtered_phns):
            phtrain.write(word+'\t'+phonemes+'\n')
          else:
            print "Skipping the entry [%s]: does not conform the allowed phoneset" % phonemes
        else:
            print "Skipping the word [%s]: contains special characters" % word

      i=4
    else:
      # i == 4
      # 4th line: star or other pronunciations
      if line.strip() == "*":
        i=1

finally:
  input.close()
  phtrain.close()
