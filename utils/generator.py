import os.path
import os
import hashlib
import urlparse
import ast

class Generator():
    strlist = []
    def retrieveFile(self, file):
        self.strlist = []
        with open(file) as fp:
            for line in fp:
                # jobject = json.loads(line.strip())
                self.strlist.append(line.strip())
            fp.close()
        return self.strlist
    def generateGetScripts(self, url, fullRequest):
        dirLoc = "../results"
        if os.path.isdir(dirLoc) is not True:
            print "ya"
            os.mkdir(dirLoc)
        urlP = urlparse.urlparse(fullRequest)
        m = hashlib.md5()
        m.update(fullRequest)
        name = urlP.netloc+"_"+m.hexdigest()+".py"
        if os.path.isfile(name):
            print "File already exists. %s" % name
        else:
            os.chdir(dirLoc)
            outfile = open(name, 'w+')
            outfile.write("import webbrowser\n")
            outfile.write("url = \""+fullRequest+"\"\n")
            outfile.write("new = 2 #open in new window\n")
            outfile.write("webbrowser.open(url,new=new)")
            outfile.close()


def main():
    g = Generator()
    listOfReturns = g.retrieveFile("successfulResult.txt")
    for code in listOfReturns:
        tupleCode = ast.literal_eval(code)
        (url, vulerableCode, fullRequest) = tupleCode
        g.generateGetScripts(url, fullRequest)

if __name__ == '__main__':
    main()
