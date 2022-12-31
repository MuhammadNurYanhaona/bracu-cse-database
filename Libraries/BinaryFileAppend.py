# This code illustrates how to open a binary file in append mode in Python
# so that one can add new things at the end of the file. If the file does
# not already exist then it creates the file first.
# @author: Muhammad Nur Yanhaona
# @email: nur.yanhaona@bracu.ac.bd
# @copywrite: protected

# since opening and closing a file over and over again is a costly operation,
# it is better to open the file and keep the file object in hand then do
# writing on the file through that object
def createOrOpenFileForAppend(pathToFile):
    # the second argument indicates we want to open the file for writing at the
    # end of it and we will do the writing in binary mode, which is much more
    # space efficient than writing on a text file.
    # here
    #   a: means appending to the end of the file
    #   +: means create the file if it does not exist
    #   b: means the file type is binary
    f = open(pathToFile, 'a+b')
    return f

# this function can be used to append a new content at the end of a binary file
# that has been opened already; the function returns the index in the file where
# the writing started. This index should be useful for indexing.
def appendToFile(fileHandle, content):

    # Determine the end byte-index of the file before writing. We will need this
    # index for indexing
    writingStartsAt = fileHandle.tell()

    if (isinstance(content, str)):
        # if the content is an string then we first have to encode it before
        # converting it into a binary array
        data = content.encode()
        binaryData = bytearray(data)
        fileHandle.write(binaryData)
    else:
        # for other data types, we first convert it to sting then write it to
        # the file
        strData = str(content)
        data = strData.encode()
        binaryData = bytearray(data)
        fileHandle.write(binaryData)

    return writingStartsAt

# one should always close a file when it is no longer needed
def closeFile(fileHandle):
    fileHandle.close()

# This is a test function that will open a file, do some writing, and then
# close it. This operation is repeated twice to show that file appending works
# properly
def testFileWriting(pathToFile):

    f = createOrOpenFileForAppend(pathToFile)
    messagesSet1 = ["Hello World Cup!", "I am unhappy.", "How are you?"]
    for message in messagesSet1:
        writingIndex = appendToFile(f, message)
        print(writingIndex)
    closeFile(f)

    f = createOrOpenFileForAppend(pathToFile)
    messagesSet2 = [256, 192, "How come?"]
    for message in messagesSet2:
        writingIndex = writingIndex = appendToFile(f, message)
        print(writingIndex)
    closeFile(f)

# Here we invoke the file writing test function with a path; change the path
# argument with a value appropriate for your computer
#testFileWriting("C:\\Users\\User\\PycharmProjects\\CSE716_Project\\Data File")