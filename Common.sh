#!/bin/zsh (just for the editor)
#
# Copyright 2013 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, April 2013
#

# Allow SETSHELL
software=/idiap/resource/software
source $software/initfiles/shrc $software

# SETSHELLs
SETSHELL grid
SETSHELL phonetisaurus

# Check for ISS; add it to the path
if [ "$ISSROOT" = "" ]
then
    echo "Please \"SETSHELL iss\" or point \$ISSROOT to an ISS installation"
    exit 1
fi
path=( $ISSROOT/bin $path )
fpath=( $ISSROOT/lib/zsh $fpath )

# Functions that ISS provides
autoload chdir.sh

# Hack
export FILE_LIST=/dev/null
