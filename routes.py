from doctest import OutputChecker
import json
import os.path

#Defines Route Information
class route_:
    def __init__(self, dir, busses, data):
        self.dir = dir
        self.busses = int(busses)
        self.data = data

    def get_dir(self):
        return self.dir

    def get_busses(self):
        return self.busses

    def get_data(self):
        return self.data

    def set_busses(self, busses):
        self.busses = int(busses)

    def set_dir(self, dir):
        self.dir = dir

    def set_data(self, data):
        self.data = data

#Specifies Directory Information For Data File
def define_directory(obj):
    obj.set_dir(input("Please Specify The File Directory Containing Data: "))
    if not os.path.isfile(obj.get_dir()):
        print ("INVALID - File/Directory Does Not Exist")
        return define_directory()

#Removes Spaces From Provided Dictionary
def strip_spaces(list):
    routeDataList = []
    count = 0
    for i in list:
        i = i.rstrip("\n")
        i = i.split(",")
        try:
            i[0] = i[0].replace(" ", "")
        except:
            i[0] = ""

        try:
            i[1] = i[1].replace(" ", "")
        except:
            i[1] = ""
            
        routeDataList.insert(count, i[0] + "," + i[1])
        count += 1
    return routeDataList

#This Function Will Remove Every Duplicate After The First Key Found Within The Provided Dictionary - Note May Cause Inconsistency If Not Known
def strip_duplicate_keys(output):
    rList = []
    dups = []
    for i in range(0, len(output)):
        for key,value in output[i].items():
            if key == 'route_number':
                try:
                    rList.index(value)
                    dups.append("route_number: {}, happy_ratio: {}".format(value, output[i].get('happy_ratio')))
                except:
                    rList.append(value)

    for i in range(0, len(rList)):
        rList[i] = rList[i] + "," + output[i].get('happy_ratio')   
    
    print("WARN - Please Note We Have Removed The Following Duplicate Entries From The Provided Data - If This Is An Issue Please Ammend The Text File And Restart The Application")
    for i in dups:
        print(i)

    return rList

def strip_empty_keys(output):
    delete = []
    empty = []

    for i in range(0, len(output)):
        found = False
        for key,value in output[i].items():
            if key == "" or value == "":
                found = True
                delete.append(i)
        if found == True:
            empty.append("route_number: {}, happy_ratio: {}".format(value, output[i].get('happy_ratio')))
        
    removed = 0
    for i in delete:
        del output[i-removed]
        removed += 1     

    print("WARN - Please Note We Have Removed The Following Duplicate Entries From The Provided Data - If This Is An Issue Please Ammend The Text File And Restart The Application")
    for i in empty:
        print(i)
                   
    return output


def create_dictionary(list):
    routeDataList = []
    count = 0
    for i in list:
        s = i.split(",")
        dict = {'route_number' : s[0], 'happy_ratio' : s[1]}
        routeDataList.insert(count, dict)
        count += 1
    return routeDataList

def test_print_data(list, sStr):
    print()
    for i in list:
        print(sStr + ":{}".format(i))
    print()

def read_route_data(obj):
    with open(obj.get_dir(), 'r') as reader:
        lines = reader.readlines()
        routedataList = create_dictionary(strip_spaces(lines))
        #test_print_data(routedataList, "Spaces")
        routedataList = strip_empty_keys(routedataList)
        #test_print_data(routedataList, "Empty")
        routedataList = create_dictionary(strip_duplicate_keys(routedataList))
        #test_print_data(routedataList, "Duplicate")
        obj.set_data(sort_route_data(routedataList))

def detect_data_errors(data):
    def errors_(data):
        #print("Error Detected")
        pass

    print(data)
    
    #print("Route Number: {}".format(data[0]))
    #print("Happy Ratio: {}".format(data[1]))
    if data[0].isnumeric():
        pass
    else:
        errors_(data[0])


    if data[1].isnumeric():
        pass
    else:
        errors_(data[1])

    return True

def sort_route_data(data):
    #FIX
    return sorted(data, key=lambda k: k['happy_ratio'])

def define_assigned_busses(obj):
    busses = input("Please Specify The Number Of Routes You Would Like To Assign A Bus To: ")
    print()

    if busses.startswith("-") and busses[1:].isdigit():
        print("INVALID - Please Enter A Positive Integer Above 0")
        return define_assigned_busses()
    elif not busses.isnumeric():
        print("INVALID - Please Enter A Value Containing Integers") 
        return define_assigned_busses()
    else:
        if int(busses) > len(obj.get_data()):
            print("INVALID - Please Enter A Value Lower Or Equal To The Number Of Routes ({})".format(len(obj.get_data()))) 
            return define_assigned_busses()
        else:
            obj.set_busses(busses)    

def print_ratios(route):
    print("You Should Add busses To The Following Routes:")
    for i in range(0, route.get_busses()):
        print("#{}: ".format(i+1) + route.get_data()[i]["route_number"])
    print()

def repeat_():
    boo = input("Would You Like To Repeat With The Same Route (Y/N):")
    if boo.isnumeric() or not boo == "Y" or not boo == "y" or not boo == "N" or not boo == "n":
        print("INVALID - Please Enter Y Or N Only")
        return repeat_()
    else:
        print()    
        return boo

def main_(obj):
    if not obj:
        obj = route_(None, 0, None)
        define_directory(obj)
        read_route_data(obj)
        define_assigned_busses(obj)
        print_ratios(obj)
    else:
        define_assigned_busses(obj)
        print_ratios(obj)

    dec = repeat_()

    if dec == "Y":
        return main_(obj)
    else:
        return main_(None)

main_(None)
