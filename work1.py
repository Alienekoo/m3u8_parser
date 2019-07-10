import os
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

remove_empty_lines("m3files_8.txt")
a = 0
mylines, channel, listo, mylines2 = [], [], [], []
with open("m3files_8.txt", 'rt') as myfile:
    for line in myfile:
        mylines2.append(line)


for i in range(len(mylines2)):
    if mylines2[i].startswith(protocol.extinf):
        if mylines2[i + 1].startswith("http") and ".m3u8" in mylines2[i + 1]:
            mylines.append(mylines2[i])
            mylines.append(mylines2[i + 1])

print(mylines)
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

# listo should be 2 dimensional array.
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

