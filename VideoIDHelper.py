from bs4 import BeautifulSoup
import re,requests
from datetime import datetime
def idExtractor(s):
    #URL?
    if isURL(s):
        return getIDfromURL(s)
    #Short URL?
    elif isShortURL(s):
        return getIDfromShortURL(s)
    #Assume ID
    else:
        return s

def playlistIdExtractor(s):
    #Direct Link
    if isPlaylistUrl(s):
        return getList(s)
    #Video from playlist
    elif isURL(s):
        return getList(s)
    #Video from playlist with short link
    elif isShortURL(s):
        return getList(s)
    #Assume ID
    else:
        return s

def channelExtractor(s):
    #Link to user
    if isChannelURL(s):
        #print('a')
        #print(getUserFromUrl(s))
        return getUserFromChannel(s)
    #Assume ID
    else:
        #print('c')
        return s

def userExtractor(s):
    #Link to user
    if isUserURL(s):
        #print('a')
        #print(getUserFromUrl(s))
        return getUserFromUrl(s)
    #Assume ID
    else:
        #print('c')
        return s

def isURL(s): 
    return (s.find("www.youtube.com") != -1)
def isShortURL(s):
    return (s.find("youtu.be") != -1)
def isPlaylistUrl(s):
    return (s.find("www.youtube.com/playlist") != -1)

def isChannelId(s):
    return ((s.find("UC") != -1 ) and (len(re.findall(r'UC[^&#\/]+',s)[0]) > 12 ))
def getChannelId(s):
    #return s[s.find("UC"):]
    try:
        return re.findall(r'UC[^&#\/]+',s)[0]
    except:
        return ""

def getUserFromUrl(s):
    splitUp=s.split('/')
    #print(splitUp[splitUp.index('user')+1])
    #print("GETTING USER:")
    #print(s)
    return splitUp[splitUp.index('user')+1]
def getUserFromChannel(s):
    splitUp=s.split('/')
    #print(splitUp[splitUp.index('user')+1])
    #print("GETTING USER:")
    #print(s)
    return splitUp[splitUp.index('channel')+1]

def isUserURL(s):
    return (s.find("www.youtube.com/user") != -1)


def isChannelURL(s):
    return (s.find("www.youtube.com/channel") != -1)

def getIDfromURL(s):
    try:
        return re.findall(r'v=[^&#]+',s)[0][2:]
    except:
        return None
    
def getIDfromShortURL(s):
    if(s.find("?")!=-1):
        return  s[ s.find("/", s.find("/")+2)+1 :  s.find("?")] 
    return  s[ s.find("/", s.find("/")+2)+1  :  ]

def getList(s):
    try:
        return re.findall(r'list=[^&#]+',s)[0][5:]
    except:
        return None
"""
def getPLList(s):
    try:
        s=s[s.find('/playlist')+10:]
        print(s)
        return re.findall(r'list=[^&#]+',s)[0][2:]
    except:
        return None
"""

def channelIDInvalid(id):
    if id.find('youtube.com') != -1 or id.find('youtu.be') != -1:
        return True
    r=requests.get("https://www.youtube.com/channel/{}".format(id))
    if r.status_code != 200 and r.status_code != 404:
        return False
    if r.text.find("empty-channel-banner") != -1:
        return True
    return False

def channelUnavailable(id):
    if id.find('youtube.com') != -1 or id.find('youtu.be') != -1:
        return True
    r=requests.get("https://www.youtube.com/user/{}".format(id))
    if r.status_code != 200 and r.status_code != 404:
        return False
    if r.text.find("empty-channel-banner") != -1:
        return True
    return False

"""
def videoReallyUnavailable(id):
    r=requests.get("http://youtu.be/{}".format(id))
    #print (r.status_code)
    if r.status_code == 404:
        return True
    if r.status_code == 200:
        if r.text.find("unavailable-message") != -1:
            return True
        return False
    return False
"""
def videoUnavailable(id):
    r=requests.get("http://youtu.be/{}".format(id))
    if r.status_code != 200:
        return False
    if r.text.find("watch-title") == -1:
        return True
    return False

def getVideoUser(id):
    r=requests.get("http://youtu.be/{}".format(id))
    if r.status_code != 200:
        return ""  
    pageText = r.text
    soup=BeautifulSoup(pageText,"html.parser")
    for link in soup.select(".yt-user-info > a"):
        #print("HERE YOU GO:\n"+link.decode_contents())
        return ("https://www.youtube.com/user/{}".format(link.decode_contents()))
    return ""

def getVideoDate(id):
    r=requests.get("http://youtu.be/{}".format(id))
    if r.status_code != 200:
        return ""
    pageText = r.text
    soup=BeautifulSoup(pageText,"html.parser")
    for link in soup.find_all("meta", itemprop="datePublished"):
        return(link.get('content'))
    return ""
#https://www.youtube.com/watch?v=HW-Jr4M4w90

def dateSearch(date,ids,start,end,getFirst):
    #print(date,start,end)
    if start==end:
        return start

    
    if start==end-1:
        if getFirst:
            return end
        return start
    
    #Query date if it fails return -1
    midIndex=start + int((end-start)/2)
    midQuery=getVideoDate(ids[midIndex])
    if midQuery=="":
        return -1
    midDate=dateConvert(midQuery)
    if getFirst:
        if date > midDate:
            return dateSearch(date,ids,start,midIndex,getFirst)
        else:
            return dateSearch(date,ids,midIndex,end,getFirst)
    if date >= midDate:
        return dateSearch(date,ids,start,midIndex,getFirst)
    else:
        return dateSearch(date,ids,midIndex,end,getFirst)
def dateConvert(s):
    y,m,d = map(int, s.split('-'))
    return datetime( y,m,d )