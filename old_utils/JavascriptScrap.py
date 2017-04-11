import urlparse
import requests
import scrapy
import json
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class JavascriptScrap(BaseSpider):
    name = "jsSpider"
    start_urls = [
        "https://app3.com/",
        "https://app1.com/",
        "https://app5.com/",
        "https://app7.com/",
    ]
    def verifyAbsolutePath(self, path):
        return bool(urlparse.urlparse(path).netloc)

    def scrapJavascript(self, res, urlPath):
        # javascriptList = res.xpath("//script/@src").extract()
        finalJavascriptList = []
        javascriptList = res
        for src in javascriptList:
            if self.verifyAbsolutePath(src):
                finalJavascriptList.append(src)
            else:
                finalJavascriptList.append(urlPath+src)
        return finalJavascriptList

    def extractEndPointsFromJavascript(self, url, host):
        meth = url.split(",")
        meth[1] = meth[1].strip(" \"\'\n\t\r")
        components={}
        if self.verifyAbsolutePath(meth[1]):
            components = urlparse.urlparse(meth[1])

        else:
            components = urlparse.urlparse(host+meth[1])
        parameters = urlparse.parse_qs(components.query)
        result = {components.scheme+"://"+components.netloc+components.path:[{"type":"GET"}, parameters]}
        parsed = json.dumps(result)
        with open("test.txt", "a") as outfile:
            json.dump(result, outfile)
            outfile.write("\n")
            outfile.close()

    def connectToJavaScriptSrc(self, src, host):
        r = requests.get(src, verify = False)
        bodyList = r.content.split("\r")
        print src
        for index, content in enumerate(bodyList):
            endpoint = ""
            if "client.open" in content:
                if ");" not in content:
                    # print content.strip()+bodyList[index+1].strip()
                    endpoint = content.strip()+bodyList[index+1].strip(" ").strip(");")
                    # print endpoint
                else:
                    # print content
                    endpoint = content.strip(");")
                    # print endpoint
                self.extractEndPointsFromJavascript(endpoint, host)

    def javascriptStart(self, response):
        jsList = response.xpath("//script/@src").extract()
        print jsList
        thislist = self.scrapJavascript(jsList, response.url);
        for urlSrc in thislist:
            self.connectToJavaScriptSrc(urlSrc, response.url)

    def parse(self, response):
        self.javascriptStart(response)
