import os
import work2
import pymongo
import re
import protocol
from pprint import pprint
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


remove_empty_lines("m3files_4.txt")
a = 0
mylines, channel, listo, mylines2 = [], [], [], []
with open("m3files_4.txt", 'rt') as myfile:
    for line in myfile:
        mylines2.append(line)

# extract m3u8 links only. (flexible)
for i in range(len(mylines2)):
    if mylines2[i].startswith(protocol.extinf):
        if mylines2[i + 1].startswith("http") and ".m3u8" in mylines2[i + 1]:
            mylines.append(mylines2[i + 1])

if mylines != []:
    for i in range(len(mylines)):
        grp = "default_grp%d" %(i)
        ch = "default_ch%d" %(i)
        m3u = mylines[i].rstrip()
        # print(ch)
        # print(ch, grp, m3u)
        array2 = [ch, grp, m3u]
        listo.append(array2)
else:

    print("Incorrect File format ")

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

m3u8l = dicty(listo)
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
