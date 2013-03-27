#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Alexandre Nanchen"
__version__ = "Revision: 1.0"
__date__ = "Date: 2012/11/15"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "Python"


import os
import codecs

class Ioread:
    """Basic input output operations"""

    def __init__(self):
        pass

    #//////////////////////////////////////////////////////////////////////
    #Public members
    
    def readFileContentList(self, fullFilePath):
        """Take the path of the file to read and return its content."""

        fileContent = []

        try:
                        
            f = codecs.open(fullFilePath, 'r', 'utf-8')            
            fileContent = f.readlines()                                
            f.close()

        except IOError, ex:
            try:
                f.close()
            except Exception, e:
                pass

            raise ex
                    
        return self.removeNewLine(fileContent)


    def writeFileContent(self, fullFilePath, fileContent, openMode = 'w'):
        """Write a string to a file"""
                    
        try:
                  
            f = codecs.open(fullFilePath, openMode, 'utf-8')      
            f.write(fileContent)
            f.close()

        except IOError, ex:
            try:
                f.close()
            except Exception, e:
                pass

            raise ex        


    def removeNewLine(self, fileContent):
        """Remove trailing \n"""

        return ["%s" % line[:-1] for line in fileContent]

