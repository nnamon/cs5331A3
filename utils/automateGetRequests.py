from scrapy.http import FormRequest
import json
import urllib
import requests

class Human():
    strlist = []
    jsonObj = {}
    def retrieveFile(self, file):
        self.strlist = []
        with open(file) as fp:
            for line in fp:
                # jobject = json.loads(line.strip())
                self.strlist.append(line.strip())
            fp.close()
        return self.strlist

    def setObjToTest(self, jsonObj):
        # print type(jsonObj), jsonObj
        self.jsonObj = jsonObj
    def insertCodeIntoObj(self, exploit):
        url = self.jsonObj.keys()
        parameters = self.jsonObj[url[0]][1]
        for value in parameters:
            self.jsonObj[url[0]][1][value] = exploit
        return self.jsonObj

    def buildAndSendGETRequest(self, package):
        url = package.keys()
        data = package[url[0]][1]
        data_str = "&".join("%s=%s" % (k,v) for k,v in data.items())
        print data_str
        result = requests.get(url[0], verify = False, params = data_str)
        # method = package[url[0]][0]
        # result = urllib.urlopen(url[0], data)
        if "root" in result.content:
            print result.content

def main():
    pq = Human()
    jsonObjstr = pq.retrieveFile("test.txt")
    exploitCode = pq.retrieveFile("exploitCode.txt")
    for objstr in jsonObjstr:
        pq.setObjToTest(json.loads(objstr))
        for code in exploitCode:
            package = pq.insertCodeIntoObj(code)
            print package
            pq.buildAndSendGETRequest(package)

if __name__ == '__main__':
    main()
