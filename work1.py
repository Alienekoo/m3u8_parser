import os
import work2
import pymongo
import re
import protocol
from pprint import pprint

# This file takes in a .txt file of list of m3u8's and their data. It makes a dictionary of it which contains channel name, group title, m3u8 URLs, child m3u8 URLs(if any), .ts URLs.
# It uploads the dictionary to pymongo DataBase

# remove empty lines in the file
def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)


# remove any pattern in the file
'''def remove_ABCs(mylinesa, pattern1):
    pattern = re.compile(pattern1)
    for line in mylinesa:
        if pattern.match(line):
            mylinesa.remove(line)
    return mylinesa
    def remove_different(mylinesa):
    it = iter(mylinesa)
    for i in it:
        a = i
        b = next(it)
        if a.startswith("#EXTINF") and b.endswith("m3u8"):
           pass
        else:
            mylinesa.remove(a)
            mylinesa.remove(b)

    return mylinesa '''

# takes in a nested list : [[channel, group title, m3u8 URL], ...] that is extracted from the text file.
# Processes the list and outputs a dictionary : {channel : {grpup title : m3u8 URl : {child m3u8 URLs : {'tslist' : [.ts files], 'metadata' :[]}, ..}, ..}, ..}
def dicty(array1):
    new_dict = {}
    for m in range(len(array1)):
        if new_dict.get(array1[m][0]) == None:
            new_dict[array1[m][0]] = {}
            new_dict[array1[m][0]][array1[m][1]] = {}
            new_dict[array1[m][0]][array1[m][1]][array1[m][2]] = {}
        elif new_dict.get(array1[m][0]) != None:
            if new_dict.get(array1[m][0], {}).get(array1[m][1]) == None:
                new_dict[array1[m][0]][array1[m][1]] = {}
                new_dict[array1[m][0]][array1[m][1]][array1[m][2]] = {}
            else:
                # print("test", new_dict[array1[m][0]][array1[m][1]])
                pass
        else:
            print("check again")

    for cha, grpt in new_dict.items():
        for gt, m3 in grpt.items():
            for m31, m32 in m3.items():
                # print(new_dict[cha][gt])
                # print(m32)
                dicta = work2.M3dict(m31, set(), 0)
                new_dict[cha][gt][m31] = dicta.getfiles()
                print(m31)

    return new_dict

# main code

remove_empty_lines("m3files_12.txt")
a = 0
# reads the text file and saves all the lines in a list

mylines, channel, listo, mylines2 = [], [], [], []
with open("m3files_12.txt", 'rt') as myfile:
    for line in myfile:
        mylines2.append(line)
# filters m3u8 files and the info relate to it
for i in range(len(mylines2)):
    if mylines2[i].startswith(protocol.extinf):
        if mylines2[i + 1].startswith("http") and ".m3u8" in mylines2[i + 1]:
            mylines.append(mylines2[i])
            mylines.append(mylines2[i + 1])


# checks if the format is correct and reads the lines in the list and collects all the data like channel name, group title and m3u8 URL.
# saves the collected data into a nested list. => listo
if mylines != []:
    for i in range(len(mylines)):
        if mylines[i].startswith("#EXTINF:"):
            y = mylines[i].split("group-title=", 1)[1]
            # z = re.findall(r'"(.*?)"', y)
            grp = y.rstrip()
            ch = grp.split(",", 1)[1]
            m3u = mylines[i + 1].rstrip()
            # print(ch)
            # print(ch, grp, m3u)
            array2 = [ch, grp, m3u]
            listo.append(array2)
        elif mylines[i].startswith("http") or mylines[i].startswith("rtmp") or mylines[i].startswith("mms") or mylines[i].startswith("rtsp"):
            pass
       # else:
       #     channel.append(mylines[i])
        #    a += 1
else:

    print("Incorrect File format ")

    '''grp = "default"
    i = 0
    while (i < len(mylines)):
        if not mylines[i].startswith("http"):
            ch = mylines[i].rstrip()
            i += 1
        array2 = []
        m3u = mylines[i].rstrip()
        array2 = [ch, grp, m3u]
        listo.append(array2)
        i += 1'''
# using the deficnition
m3u8l = dicty(listo)

# converting all the keys of the dictionary to confirm into pymongo's format: "." to "_DOT_"
# uploads the converted dictionary to the pymongo database
if m3u8l != {}:
    def convertdot(d):
        new = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = convertdot(v)
            new[k.replace('.', '__DOT__')] = v
        return new


    m3u8d = convertdot(m3u8l)
    print(m3u8d)

    myclient = pymongo.MongoClient("mongodb://192.168.5.157:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["m3u8_files"]
    x = mycol.insert_one(m3u8d)

