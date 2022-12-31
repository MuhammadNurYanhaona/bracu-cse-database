import Libraries.BinaryFileRead as BinaryFileRead
import Libraries.RecordToStringConvert as RecordToStringConvert
from datetime import date, datetime
from collections import namedtuple
import Libraries.BinaryFileAppend as BinaryFileAppend

ObjectType = namedtuple('ObjectType', ['name', 'datatype'])

def check_record(record):
    record = record.split(",")
    if len(record) == len(object_type[default_object_type]):
        for i, j in enumerate(record):
            if isinstance(object_type[default_object_type][i].datatype, int):
                record[i] = int(j, default=0)
            elif isinstance(object_type[default_object_type][i].datatype, date):
                record[i] = datetime.strptime(j, '%m/%d/%Y').date()
        return {"Data": RecordToStringConvert.stringifyRecord(record), "Param": True}
    else:
        return {"Param": False}

def search_record(search_type, search_value):
    file = BinaryFileRead.openFile("Storage//Data File")
    type_list = []
    for i in object_type[default_object_type]:
        type_list.append(i[1])
    line = file.readline()
    found = False
    while line:
        record = RecordToStringConvert.retrieveRecordFromString(line.decode(), type_list)
        if search_type == "ID":
            search_value = int(search_value)
            if record[0] == search_value:
                found = True
                break
        elif search_type == "Name":
            if record[1] == search_value:
                found = True
                break
        line = file.readline()
    file.close()
    if found:
        result = ''
        for i, j in enumerate(record):
            if isinstance(j, int):
                j = str(j)
            if isinstance(j, date):
                j = j.strftime('%m/%d/%Y')
            if i == 0:
                result = j
            else:
                result += ',' + j
        print(result)
    else:
        print("Record not found...")

default_object_type = "students"

object_type = {
    "students": [
        ObjectType("ID", int),
        ObjectType("Name", str),
        ObjectType("BirthDate", date),
        ObjectType("Address", str)
    ]
}

exit_command = "E"

while True:
    print("Enter 'R' to read records, 'W' to write records, 'S' to search for a record, or 'E' to exit:")
    option = input()

    if option == "E":
        print("Exited")
        break

    elif option == "R":
        file = BinaryFileRead.openFile("Storage//Data File")
        type_list = [obj.datatype for obj in object_type[default_object_type]]
        line = file.readline()
        while line:
            record = RecordToStringConvert.retrieveRecordFromString(line.decode(), type_list)
            result = ''
            for i, j in enumerate(record):
                if isinstance(j, int):
                    j = str(j)
                if isinstance(j, date):
                    j = j.strftime('%m/%d/%Y')
                if i == 0:
                    result = j
                else:
                    result += ',' + j
            print(result)
            line = file.readline()
        file.close()

    elif option == "W":
        file = BinaryFileAppend.createOrOpenFileForAppend("Storage//Data File")
        while True:
            data_input = input("Input a record or type E to Exit from write mode: \n")
            if data_input == exit_command:
                print("Exiting write mode.")
                break
            flag = check_record(data_input)
            if flag["Param"] != True:
                print("Something wrong! Try Again. Format is: int,str,date,str")
            else:
                BinaryFileAppend.appendToFile(file, '\n'.join([flag["Data"], '']))
        file.close()

    elif option == "S":
        print("Type 'ID' or 'Name' to search by:")
        search_type = input()
        print("Enter the value to search for:")
        search_value = input()
        search_record(search_type, search_value)

    else:
        print("Invalid option. Try again.")
