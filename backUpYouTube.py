import requests,json,sys,re,os
from datetime import datetime

from VideoIDHelper import *

from bs4 import BeautifulSoup


def makeRequest(partialURL,parameter,ID):
	pars = {"parameter" : ID}
	return requests.get(partialURL, params=pars)
def makeRequestWithoutParameter(URL):
	return requests.get(URL)

def backUpAnnotations(ID):
	return makeRequestWithoutParameter("http://web.archive.org/save/https://www.youtube.com/annotations_invideo?video_id={}".format(ID))
def snapShotPage(ID):
	return makeRequest("http://web.archive.org/save/https://www.youtube.com/watch","v",ID)

def annotationsBackedUp(ID):
	return makeRequestWithoutParameter("http://archive.org/wayback/available?url=https://www.youtube.com/annotations_invideo?video_id={}".format(ID))
def snapShotTaken(ID):
	return makeRequestWithoutParameter("http://archive.org/wayback/available?url=https://www.youtube.com/watch?v={}".format(ID))


def main():
	first = True
	argument = ""
	print( "Hello today is: " + str(datetime.now().month) + "/" + str(datetime.now().day))
	#print( "Remember that we have time until: " + "1/15" + "for Annotations and Credits; and until " + "1/31" +" for Episodes (presumably PST 0:00) " )
	print( "Remember that we have time until: " + "1/15" + "for the Annotations (presumably PST 0:00) " )
	while first or argument == "":
		#argument ="horse"
		argument = input("Type in a URL to video or its ID: ")
		
		if argument == "":
			print("Program Terminated")
			break

		else:
			vID = idExtractor(argument)
			try:
				r = snapShotTaken(vID)
				#print("Snapshot Taken: " + str(r.status_code))
				#print(r.json())
				if 'closest' not in r.json()["archived_snapshots"]:
					r2=snapShotPage(vID)
					print("Snapshot Status Code:{}".format(str(r2.status_code)))
				else:
					print("Snapshot found!")
				r = annotationsBackedUp(vID)
				#print("Snapshot Taken: " + str(r.status_code))
				if 'closest' not in r.json()["archived_snapshots"]:
					r2=backUpAnnotations(vID)
					print("Annotations Backup Status Code:{}".format(str(r2.status_code)))
				else:
					print("Annotations found!")
			except Exception as e:
				print(e)
			print("done")
	


if __name__== "__main__":
	main()