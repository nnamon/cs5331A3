import json
import requests

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
        for value in parameters:
            self.jsonObj[url[0]][1][value] = exploit
        self.currentExploitCode = exploit
        return self.jsonObj

    def expectedResult(self, lookfor):
        self.lookfor = lookfor

    def buildAndSendGETRequest(self, package):
        url = package.keys()
        data = package[url[0]][1]
        data_str = "&".join("%s=%s" % (k,v) for k,v in data.items())
        result = requests.get(url[0], verify = False, params = data_str)
        if self.lookfor in result.content:
            return (url[0], self.currentExploitCode)

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
    print successfulResult

def main():
    oneLineSetAndGo("test.txt", "exploitCode.txt", "root")
if __name__ == '__main__':
    main()
