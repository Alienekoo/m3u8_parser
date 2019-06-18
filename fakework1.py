import os
import os
import work2
import pymongo
import re


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
def remove_ABCs(mylinesa):
    i = 0
    pattern = re.compile("^[A-Z]\)\.$")
    for line in mylinesa:
        if pattern.match(line):
            mylinesa.remove(line)
        i+=1

remove_empty_lines("m3files_1.txt")
a = 0
mylines, channel, listo = [], [], []
with open("m3files_1.txt", 'rt') as myfile:
    for line in myfile:
        mylines.append(line)
remove_ABCs(mylines)
if "#EXTINF:-1" in mylines[1]:
    for i in range(len(mylines)):
        if mylines[i].startswith("#EXTINF:-1"):
            y = mylines[i].split("group-title=", 1)[1]
            # z = re.findall(r'"(.*?)"', y)
            grp = y.rstrip()
            ch = channel[a - 1].rstrip()
            m3u = mylines[i + 1].rstrip()
            # print(ch)
            # print(ch, grp, m3u)
            array2 = []
            array2 = [ch, grp, m3u]
            listo.append(array2)
        elif mylines[i].startswith("http"):
            pass
        else:
            channel.append(mylines[i])
            a += 1
else:
    grp = "default"
    i = 0
    while(i<len(mylines)):
        if not mylines[i].startswith("http"):
            ch = mylines[i].rstrip()
            i += 1
        array2 = []
        m3u = mylines[i].rstrip()
        array2 = [ch, grp, m3u]
        listo.append(array2)
        i += 1

print(listo)