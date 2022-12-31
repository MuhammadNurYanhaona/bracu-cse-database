# -*- coding: utf-8 -*-
"""
This library contains code to convert a database record into a string and to 
retrieve a record in its original format from the string representation. This 
facility is useful for storing records in files and retrieving them from those 
files. 

@author: Dr. Muhammad Nur Yanhaona
@email: nur.yanhaona@bracu.ac.bd
@copywrite: restricted
"""

# this package is needed to support date and time type attributes in database
# records
from datetime import datetime
from datetime import date

# This is a constant that is used as the separator for attributes in the string
# representation of a database record
ATTRIBUTE_SEPARATOR = '||||'

# The formats for storing a date and time object as a string
DATE_STRING_FORMAT = '%m/%d/%Y'
TIME_STRING_FORMAT = '%m/%d/%Y %H:%M:%S'

# This function converts a database record given as a Python list object into a 
# string object. 
def stringifyRecord(record):
    
    # this checking ensure that we do not convert non-list objects that cannot
    # be a database record into strings
    if not isinstance(record, list):
        print('Record type given for string conversion: ' + str(type(record)))
        raise TypeError("Only a list can be a database record.")
    
    
    # generate a list of string from the list of attributes of the record
    strList = []
    for attribute in record:
        # date and times object needs careful handling; we can convert other 
        # attributes to string quite easily
        if isinstance(attribute, datetime):
            strList.append(attribute.strftime(TIME_STRING_FORMAT))
        elif isinstance(attribute, date):
            strList.append(attribute.strftime(DATE_STRING_FORMAT))
        else:    
            strList.append(str(attribute))
        
    # then concate the list of string attributes using the attribute separator
    return ATTRIBUTE_SEPARATOR.join(strList)

# This function reconstructs a database record from string representation to 
# its original list form. Since we need to know the original attribute types 
# to convert string to those attributes, this function takes the string form of
# the record and a list representing the attribute types.
# Note that, currently the system only support string, int, float, and datetime
# for attribute types
def retrieveRecordFromString(strRecord, typeInfoList):
    
    # initiate an empty record object as list
    record = []
    # separate the individual string attribute parts from the string record
    strList = strRecord.split(ATTRIBUTE_SEPARATOR)
    
    # if the number of strings in the list of string is not the same as the 
    # number of attributes in the typeInfoList then the original string cannot
    # be generated from the desired record type; so we throw an error then
    if len(strList) != len(typeInfoList):
        print('String has only ' + str(len(strList)) + ' attributes')
        print('The record expect ' + str(len(typeInfoList)) + ' attributes')
        raise TypeError("The object did not match the record type.")
        
    # iterate over the string attributes and convert them to proper attribute
    # types to reconstruct the record
    index = 0
    for strAttr in strList:
        attrType = typeInfoList[index]
        if attrType is str:
            record.append(strAttr)
        elif attrType is int:
            record.append(int(strAttr))            
        elif attrType is float:
            record.append(float(strAttr))
        elif attrType is datetime:
            record.append(datetime.strptime(strAttr, TIME_STRING_FORMAT))
        elif attrType is date:
            record.append(datetime.strptime(strAttr, DATE_STRING_FORMAT).date())    
        else:
            raise TypeError('Unsupported attribute type: ' + str(attrType))
        index = index + 1    
            
    # return the reconstructed record
    return record        
        

# This is a tester function that checks if string conversion of a database
# record works properly
def testStringConversion():
    
    # create a record and convert it into a string
    birthDate = datetime.strptime('12/16/1971', DATE_STRING_FORMAT).date()
    startTime = datetime.strptime('01/31/2022 05:10:19', TIME_STRING_FORMAT)
    record1 = [2025067, 'John Doe', 16.789, 'Dhaka', birthDate, startTime]
    strRecord = stringifyRecord(record1)
    print("String representation of the record is as follows \n" + strRecord)
    
    # reconstruct another record from the string
    typeList = [int, str, float, str, date, datetime]
    record2 = retrieveRecordFromString(strRecord, typeList)
    
    # check if the two records are the same
    for attr1, attr2 in zip(record1, record2):
        if (attr1 != attr2):
            print("Test fail: Reconstructed attribute didn't match the original")
            print(attr1)
            print(attr2)
            

# invoking the test function
testStringConversion()