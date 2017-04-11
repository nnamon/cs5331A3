import json
import requests
from inspect import BlockFinder
import inspect

class Human():
    strlist = []
    jsonObj = {}
    lookfor = ""
    currentExploitCode = ""
    def retrieveFile(self, file):
        self.strlist = []
        with open(file) as fp:
            for line in fp:
                # jobject = json.loads(line.strip())
                self.strlist.append(line.strip())
            fp.close()
        return self.strlist

    def setObjToTest(self, jsonObj):
        self.jsonObj = jsonObj

    def insertCodeIntoObj(self, exploit):
        url = self.jsonObj.keys()
        parameters = self.jsonObj[url[0]][1]
        self.currentExploitCode = exploit
        for value in parameters:
            self.jsonObj[url[0]][1][value] = exploit
        return self.jsonObj

    def expectedResult(self, lookfor):
        self.lookfor = lookfor

    def buildAndSendGETRequest(self, package):
        url = package.keys()
        data = package[url[0]][1]
        data_str = "&".join("%s=%s" % (k,v) for k,v in data.items())

        result = requests.get(url[0], verify = False, params = data_str)
        if self.lookfor in result.content:
            return (url[0], self.currentExploitCode, result.url)

class FileGenerator():
    fileName = ""
    outfile = {}
    def setFileName(self, filename):
        self.fileName = filename
    def openFile(self):
        self.outfile = open(self.fileName, "a")
    def populateFile(self, tupleCode):
        self.outfile.write(str(tupleCode)+"\n")
    def closeFile(self):
        self.outfile.close()



def oneLineSetAndGo(injectionPointsFile, exploitCodesFile, expectedResultToSee):
    pq = Human()
    jsonObjstr = pq.retrieveFile(injectionPointsFile)
    exploitCode = pq.retrieveFile(exploitCodesFile)
    pq.expectedResult(expectedResultToSee)
    successfulResult = []
    for objstr in jsonObjstr:
        pq.setObjToTest(json.loads(objstr))
        for code in exploitCode:
            package = pq.insertCodeIntoObj(code)
            result = pq.buildAndSendGETRequest(package)
            if result is not None:
                successfulResult.append(result)
    fg = FileGenerator()
    fg.setFileName("successfulResult.txt")
    fg.openFile()
    for code in successfulResult:
        fg.populateFile(code)
    fg.closeFile()


def main():
    oneLineSetAndGo("../injectionPointsFile/test.txt", "../exploits/directoryTraversal.txt", "root")
    oneLineSetAndGo("../injectionPointsFile/test.txt", "../exploits/dataInjection.txt", "192.168.56.101")
    # response = requests.get("https://app3.com/js/script.js", verify = False)
    # result = response.content
    # for ch in ['\t','\n']:
    #     result = result.replace(ch, "")
    # test = inspect.getblock(result.split("\r"))
    # print response.content.rstrip("\n\t").split("\r")
    # print test
if __name__ == '__main__':
    main()
