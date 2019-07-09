# import iso8601
import datetime
import urllib
import urllib.request
import http
import re
from typing import Any, Union, Tuple, Dict
import protocol
from pprint import pprint

class M3dict:
    # returns a dictionary and input is a m3u8 link.
    m3url: object
    status: Union[bool, Tuple[str, Any]]

    def __init__(self, m3url, look_up_set,  metad: object = None):
        self.dict = {}
        self.m3url = m3url
        self.url = str(m3url.rpartition('/')[0])
        self.metad = metad
        self.look_up_set = set(look_up_set)
        self.requrl = None

    # for m3u8 files
    def verifyurl(self) -> object:
        try:
            self.requrl = urllib.request.urlopen(self.m3url)
            return "works1"
        except (urllib.error.HTTPError, urllib.error.URLError, http.client.HTTPException) as e:
            if "HTTPError" in str(e):
                return "Cant open the url. HTTPError ", e.status, datetime.datetime.now()
            else:
                return "Cant open the page because the page can not be reached. Error ", datetime.datetime.now()
    # for .ts files
    def verifyurlo(self, urlo: object) -> object:
        """

        :type url: object
        """
        try:

            var = urllib.request.urlopen(urlo)
            return "works1"
        except (urllib.error.HTTPError, urllib.error.URLError, http.client.HTTPException, ValueError) as e:
            if "HTTPError" in str(e):
                return "Cant open the url. HTTPError ", e.status
            else:
                return "Cant open the page because the can not be reached. Error "

    def urlopen(self):
        if self.verifyurl() == "works1":
            f = self.requrl
            myfile = f.read()
            myfiles = myfile.decode("utf8")
            return myfiles
        else:
            return self.verifyurl()

    def getfiles(self):
        if "Error" not in self.urlopen():
            mylineso = self.urlopen()
            if protocol.extinf in mylineso:
                # ts file so do the .ts file reading


                if protocol.ext_x_key in mylineso:
                    if "METHOD=NONE" in mylineso:
                        # this file has no key so normal .ts file reading
                        tslist = self.tsread(mylineso)
                    else:
                        # it has key so different ts file reading with key
                        tslist = self.tskeyread(mylineso)
                else:
                    # just a .ts file reading
                    tslist = self.tsread(mylineso)

                self.dict = {}
                self.dict["tslist"] = tslist
                self.dict["metadata"] = self.metad
                return self.dict

            elif protocol.ext_x_stream_inf in mylineso:
                # m3u8 file so do the .m3u8 file reading
                # just stream files reading


                dicto = self.m3_stream(mylineso)
                self.dict[self.m3url] = {}
                self.dict = dicto
                return self.dict
            else:
                # print('check again1 ' + self.m3url)
                return "Empty_Page", datetime.datetime.now()
        else:
            # print("Error")
            return self.verifyurl()

    def tsread(self, mylineso):
        # returns a list of tuples
        print("I entered a ts file")
        mylines = []
        mylines = list(map(str.strip, mylineso.split('\n')))
        ts = []
        for i in range(len(mylines)):
            if mylines[i].startswith(protocol.extinf):
                if mylines[i + 1].startswith("http"):
                    pass
                elif mylines[i + 1].startswith(".."):
                    mylines[i + 1] = self.url + mylines[i + 1].replace("../..", '')
                else:
                    mylines[i + 1] = self.url + '/' + mylines[i + 1]
                status = self.verifyurlo(mylines[i + 1])
                time = datetime.datetime.now()
                # print(status)
                ts.append((mylines[i + 1], time, status))
        return ts

    def tskeyread(self, mylineso):
        # returns a list of tuples
        mylines = []
        mylines = list(map(str.strip, mylineso.split('\n')))
        mylines = self.remove_line(mylines, protocol.ext_x_program_date_time)
        ts = []
        for i in range(len(mylines)):
            if mylines[i].startswith(protocol.ext_x_key):
                key = mylines[i].replace(protocol.ext_x_key, '')
                if mylines[i + 2].startswith("http"):
                    pass
                elif mylines[i + 2].startswith(".."):
                    mylines[i + 2] = self.url + mylines[i + 2].replace("../..", '')
                else:
                    mylines[i + 2] = self.url + '/' + mylines[i + 2]
                status = self.verifyurlo(mylines[i + 2])
                ts.append((mylines[i + 2], key, datetime.datetime.now(), status))
        return ts

    def m3_stream(self, mylineso):
        # returns a dictionary
        mylines = []
        dicta = {}
        mylines = list(map(str.strip, mylineso.split('\n')))
        print("Im at this m3 " + self.m3url)
        for i in range(len(mylines)):
            if mylines[i].startswith(protocol.ext_x_stream_inf):
                metadata = mylines[i].replace(protocol.ext_x_stream_inf, '').rstrip().split(",")
                # print("Im also at this m3 " + self.m3url)
                if mylines[i + 1].startswith("http"):
                    pass
                elif mylines[i + 1].startswith(".."):
                    mylines[i + 1] = self.url + mylines[i + 1].replace("../..", '')
                else:
                    mylines[i + 1] = self.url + '/' + mylines[i + 1]
                # print("I built m3u8 urls too  " + mylines[i + 1])
                if mylines[i + 1] not in self.look_up_set:
                    Fire = M3dict(mylines[i + 1], metadata)
                    dicta[mylines[i + 1]] = Fire.getfiles()
            else:
                # skipping audio files for now
                pass
        return dicta

    def remove_line(self, mylinesa, pattern):
        # input: list of lines and the pattern to be searched and removed
        i = 0
        pattern = re.compile(pattern)
        for line in mylinesa:
            if pattern.match(line):
                mylinesa.remove(line)
            i += 1
        return mylinesa

    def convertdot(self, d):
        new = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.convertdot(v)
            new[k.replace('.', '__DOT__')] = v
        return new