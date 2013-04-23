ISS scripts for dictionary maintenance
======================================

These scripts are sufficient to convert the distributed forms of
dictionaries into forms useful for our tools (notably HTK and ISS).
Once a dictionary is in a standard form, the generic tools in ISS can
be used to manipulate it further.

Instructions:

1. Run ./CreateLinks.sh
   - This will link the media directories in each directory

Then for each dictionary that you need, cd <directory> and:

2. Run ./CreateDicts.sh
   - Converts the native dictionary format to something more standard

3. Run ./CreatePSaurus.sh
   - This will run phonitisaurus to generate an FST for the dictionary

Note that phonetisaurus FST creation (rather, the alignment stage) can
use up a lot of memory, so it may be necessary to run it in the grid.

--
Phil Garner, March 2013
