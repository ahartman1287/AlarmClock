#!/usr/bin/python

import time,sys, traceback
import datetime
import re,decimal
from Adafruit_7Segment import SevenSegment
import urllib2

from xml.dom.minidom import parseString

def ExtractQuotes(line):
    r= re.compile('([^ =]+) *= *("[^"]*"|[^ ]*)')

    d= {}
    for k, v in r.findall(line):
            if v[:1]=='"':
                 d[k]= v[1:-1]
            else:
                d[k]= decimal.Decimal(v)

    return d
def ParseTeamNames():
    #determine date to feed to API call
    today=datetime.date.today()
    year= today.year
    month = today.month
    day = today.day
    if month < 10:
        TodaysDate=str(year)+"/0"+str(month)+"/"+str(day)
    else:
        TodaysDate=str(year)+"/"+str(month)+"/"+str(day)

    #call to API and dump schedule information into xmlData
    URL="http://api.sportsdatallc.org/soccer-t2/wc/matches/"+TodaysDate+"/schedule.xml?api_key=mepmajrhpw8k362c7uuhsctd"
    file=urllib2.urlopen(URL)
    data = file.read()
    file.close()
    dom = parseString(data)
    xmlTag = dom.getElementsByTagName('matches')[0].toxml()
    xmlData=xmlTag.replace('<matches>','').replace('</tagName>','')

    #dump current schedule information to text file named schedule.txt
    FileToSave=open("schedule.txt","w")
    FileToSave.write(xmlData)
    FileToSave.close()
    NumberofGames=0
    NumberofMatches=0
    MatchId=[]
    with open ("schedule.txt") as f:
        for line in f:

            if line.startswith("    <match id"):
                MatchId.append(ExtractQuotes(line))
                NumberofMatches=NumberofMatches +1

            if line.startswith("      <home alias"):
                HomeArray=ExtractQuotes(line)
                HomeTeam=HomeArray['name']
                NumberofGames=NumberofGames + 0.5

            if line.startswith("      <away alias"):
                AwayArray=ExtractQuotes(line)
                AwayTeam=AwayArray['name']
                NumberofGames=NumberofGames + 0.5
                print  "Game #"+ str(NumberofGames)[:1]
                print "Home Team: "+ str(HomeTeam) + " VS  Away Team: " + str(AwayTeam) + "\n"


            if 'str' in line:
                break
    if NumberofGames >=1:
        try:
            GameSelect=int(raw_input("Please select game # to follow:"))
        except ValueError:
            print "Not a valid number!"
            sys.exit(0)
        if GameSelect > NumberofGames or GameSelect < 1:
                print "not a valid entry!"
        GetScores(MatchId[GameSelect-1])
    else:
        print "No games todays, sorry!"

def GetScores(MatchIdDictionary):

    print "Fetching scores..."
    MatchId= MatchIdDictionary['id']
    URLForMatch = "http://api.sportsdatallc.org/soccer-t2/wc/matches/"+str(MatchId)+"/boxscore.xml?api_key=mepmajrhpw8k362c7uuhsctd"
    file=urllib2.urlopen(URLForMatch)
    data = file.read()
    file.close()
    dom = parseString(data)
    xmlTag = dom.getElementsByTagName('matches')[0].toxml()
    xmlData=xmlTag.replace('<matches>','').replace('</tagName>','')

    FileToSave=open("GameXml.txt","w")
    FileToSave.write(xmlData)
    FileToSave.close()
    with open ("GameXml.txt") as f:
        for line in f:
            #print line
            if line.startswith("        <leg away_id"):
                MatchScore=ExtractQuotes(line)
                HomeScore=MatchScore['home_score']
                AwayScore=MatchScore['away_score']

    segment = SevenSegment(address=0x70)
# Continually update the time on a 4 char, 7-segment display
#while(True):
  #now = datetime.datetime.now()
  #hour = now.hour
  #minute = 61
  #second = 30
  # Set hours
  #segment.writeDigit(0, int(minute / 10))     # Tens
  #segment.writeDigit(1, minute % 10)          # Ones
  # Set minutes
  #segment.writeDigit(3, int(second / 10))   # Tens
  #segment.writeDigit(4, second % 10)        # Ones
  # Toggle color
  #segment.setColon(second % 2)              # Toggle colon at 1Hz
  # Toggle brightness
  #segment.setBrightLevel(second % 15)
  # Wait one second
  #time.sleep(1)

    segment.writeDigit(0,int(HomeScore)/10)
    segment.writeDigit(1,int(HomeScore) % 10)
    segment.writeDigit(3, int(AwayScore)/10)
    segment.writeDigit(4,int(AwayScore) % 10)


ParseTeamNames()

