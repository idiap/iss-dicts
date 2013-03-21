#!/bin/sh
#
# Copyright 2013 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, March 2013
#
data=/idiap/resource/database
[ ! -e cmudict/media ]  && ln -sf $data/cmudict/media cmudict/media
[ ! -e phonolex/media ] && ln -sf $data/phonolex phonolex/media
[ ! -e bdlex/media ]    && ln -sf $data/bdlex bdlex/media
