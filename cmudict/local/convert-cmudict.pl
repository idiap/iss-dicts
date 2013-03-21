#!/usr/bin/perl -w
#
# Copyright 2010 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, October 2010
#

#
# Convert cmudict to HTK format
#
use strict;

# In and out files
my $sourceDict = "../media/sphinxdict/cmudict_SPHINX_40";
my $targetDict = "cmudict_SPHINX.dct";

# Read in the source line by line
my @target = ();
open(SOURCE, "$sourceDict")  || die "$!";
while (<SOURCE>)
{
    # Remove the trailing newline
    chomp;

    # Get rid of the numbered pronunciations
    s/^(\S+)\(\d+\)/$1/;
    push(@target, $_);
}
close SOURCE;

# Write to the target file sorted (without escapes)
open(TARGET, ">$targetDict") || die "$!";
for my $line (sort(@target))
{
    print TARGET "$line\n";
}
close TARGET;
