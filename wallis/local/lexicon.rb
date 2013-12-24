#!/usr/bin/ruby
# -*- coding: utf-8 -*-
#
# Copyright 2013 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, August 2013
#

require "csv"

def usage()
  puts "Usage: lexicon.rb [options] file1.csv file2.csv ...
  -h       Prints this help
  -v n     Set verbosity to n
  -p file  Generate a pronunciation dictionary
"
end

# State variables
verbose = 0

# Loop over the command line
csvFile = []
while arg = ARGV.shift
  case arg
  when "-h"
    usage
    exit 0
  when "-v"
    verbose = ARGV.shift.to_i
  when "-p"
    pronDict = ARGV.shift
  else
    csvFile.push arg
  end
end

# Loop over each .csv on the command line
word={}
csvFile.each do |file|
  lex = CSV.read(file)
  puts "#{file} has #{lex.size} entries" if verbose > 0

  # Generate a word list from all the alternatives
  if pronDict
    lex.each do |r|
      r[1..-1].each do |w|
        next if !w
        if word[w] == nil
          word[w] = 1
        else
          word[w] += 1
        end
      end
    end
  end
end

# We need a pronunciation dictionary
if pronDict
  print "Got ", word.size, " words\n" if verbose > 0
  File.open(pronDict, "w") do |file|
    word.keys.sort.each do |w|
      # All phones are letters, hence lower case.  This means upper
      # case is OK for temporaries
      p = w.downcase
      p.tr!('ÄÜÖ', 'äüö')  # downcase only works on [A-Z]
      p.gsub!(/sch/, 'S')
      p.gsub!(/ch/, 'C')
      p.gsub!(/qu/, 'kw')
      p.gsub!(/c/, 'k')
      p.gsub!(/x/, 'ks')
      p = p.split('')
      p.delete("-")
      p.each do |q|
        # Put back the ones we messed up
        q.gsub!('S', 'sch')
        q.gsub!('C', 'ch')
        q.gsub!('Q', 'qu')

        # Get rid of umlauts
        q.gsub!('ä', 'ae')
        q.gsub!('ü', 'ue')
        q.gsub!('ö', 'oe')

        # Substitute ambiguous symbols
        q.gsub!('v', 'vf')
        q.gsub!('y', 'iy')
      end
      file.printf "%s\t%s\n", w, p.join(" ")
    end
  end
end
