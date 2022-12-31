# -*- coding: utf-8 -*-
"""
This library contains utility functions for reading a certain number of bytes 
from a binary file then converting that data into a string. This feature is 
needed to read records from persistent data files.

@author: Muhammad Nur Yanhaona
@email: nur.yanhaona@bracu.ac.bd
@copywrite: restricted
"""

# When one use a file to store many records of a single database relation then
# there must be a way to tell where a record ends in a file. Otherwise, if we
# start reading bytes from the file, we cannot stop reading. There are two ways
# to indicate record's ending. The common technique is to start a record with 
# an information about the length of the record. Then we can first read the 
# length first and then read as many bytes as the length suggest. This is the
# most versatile approach. Another common, but less versatile, approach is to 
# use a special string to mark the end of each record. So when reading, we keep
# reading bytes until we find the record separator. We will use this latter 
# approach for the current version of the database project. 
RECORD_SEPARATOR = "\n"

# Since database systems store files in the binary format, the reading must be
# done in that format also. the following utility function let the user open a 
# file in binary mode for reading
def openFile(filePath):
    f = open(filePath, 'rb')
    return f


# When one opens a file, there is a file cursor that points to the beginning.
# As we read more and more bytes, the cursor advances. So all files are read 
# like this from the start till the end (or as long as we are interested in 
# reading). So if we want to change this behavior, and want to read from any 
# arbitrary index, we have to move the file cursor to the start of the location
# from where we want to read. This function does that cursor moving.
def jumpToReadingOffset(offset, fileHandle):
    fileHandle.seek(offset)
    
    
# This function reads the specified number of bytes from the file from its 
# current read location. Use this function when you know how many bytes you 
# want to read and are sure that the file has at least that much data from its
# current read cursor location
def readBytes(byteCount, fileHandle):
    chunk = fileHandle.read(byteCount)
    return chunk

# This function reads as many bytes as possible starting from the current file
# read cursor position until record separator string is found. Using this 
# function is convenient when we do not keep track database record lengths else-
# where in the system and consequently, do not know how many bytes to read to
# complete reading a single record.
def readRecord(fileHandle):
    
    # first get the byte array for the record separator
    separatorArray = bytearray(RECORD_SEPARATOR.encode())
    
    # we will keep a list where we will put byte sequence that match the prefix
    # of separatorArray. If the prefix become equivalent to the whole record
    # separator then it means we found the record ending
    separatorMatcherList = []
    
    # the following buffer is for holding the bytes of the record we read
    recordBytes = []
    
    # keep reading one byte after another from the current position of the file
    # in a loop
    while True:
        # read a byte
        byte = readBytes(1, fileHandle)[0]
        # check if the byte match the byte of record separator in the current
        # index; if it match that character then add the byte in the growing 
        # list of separator matcher list; otherwise add everything we did not
        # put into recordBytes yet into that list
        byteIndex = len(separatorMatcherList)
        if byteIndex == 0 and byte == separatorArray[0]:
            separatorMatcherList.append(byte)
        elif byte == separatorArray[byteIndex]:
            separatorMatcherList.append(byte)
            if len(separatorMatcherList) == len(separatorArray):
                # this indicates that we are done reading the record
                break
        else:
           # the current bytes did not match the byte expected for the separator
           # hence, we should add everything in the separatorMatcher and the 
           # current byte to the record bytes
           recordBytes.extend(separatorMatcherList)
           recordBytes.append(byte)
           # reset the separator matcher
           separatorMatcherList.clear()
       
    return bytearray(recordBytes)
           
           
            

# The following routine is used to close an already open file. It is important
# that one close the file when it is no longer needed to save hardware resources.
def closeFile(fileHandle):
    fileHandle.close()
    
# This is a test function that reads bytes from a sample file in different ways.    
def testBinaryFileReading(pathToFile):
    
    # first we open the file
    file = openFile(pathToFile)
    
    # then test sequential readings to illustrate that as you invoke the 
    # readBytes function again and again, you get different contents
    print("Testing sequential reading of fixed number of bytes")
    for i in range(5):
        # reading four bytes of data each time
        chunk = readBytes(4, file)
        # reading returns a byte array; to print what we read, we need to convert
        # the chunk into a string
        string = chunk.decode()
        print(string)
        
    # then we test that we can read from arbitrary location by changing the 
    # file's read cursor position before reading
    print("Testing random index reading of fixed number of bytes")
    for i in range(5):
        # jumpt to an arbitrary offset
        jumpToReadingOffset(15 - i * 2, file)
        # read a fixed number of bytes and print them by converting to a string
        chunk = readBytes(4, file)
        string = chunk.decode()
        print(string)
        
    # then we test if the mechanism for reading records work correctly or not
    print("Testing reading a whole string format record")
    jumpToReadingOffset(0, file)
    for i in range(4):
        chunk = readRecord(file)
        string = chunk.decode()
        print(string)
        
    # we should close the file once we are done with our reading experiments
    closeFile(file)      
    
# invoking the test function
#testBinaryFileReading("C:\\Users\\User\\PycharmProjects\\CSE716_Project\\Data File")