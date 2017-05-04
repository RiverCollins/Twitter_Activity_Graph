#!/usr/bin/python3
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import tweepy
import json
import datetime
import sys

#Tokens for auth
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

#Using auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def Graph(List):
	Data = []
	yLabel = []
	for stuff in range(24):
		yLabel.append(str(stuff))
	for items in range(len(List)):
		Data.append(List[items])

	y_pos = np.arange(len(yLabel))
	plt.bar(y_pos, Data, align="center", alpha=0.5)
	plt.xticks(y_pos, yLabel)
	plt.show()

def OrderTime(List):
	Times = {}
	for index in range(24):
		Times[index] = 0
	for items in range(len(List)):
		Times[List[items]] = Times[List[items]] + 1
	return(Times)

#Converts UTC Tweet Time to Local Time of Tweet using the 'utc_offset' Field
def ConvertTime(TweetTimeUTC, UTCOffSet):
	#Parse TweetTimeUTC
	Time = TweetTimeUTC.split(":")
	#Converts each Time component to Int
	Sec = int(Time[2])
	Min = int(Time[1])
	Hour = int(Time[0])
	if(UTCOffSet == None):
		UTCOffSet = 1
	else:
		UTCOffSet = int(UTCOffSet)
	#Convert time to seconds
	Min = Min * 60
	Hour = Hour * 3600
	TimeSec = Sec + Min + Hour
	LocalTime = TimeSec + UTCOffSet
	LocalTime = str(datetime.timedelta(seconds=LocalTime))
	if(len(LocalTime) > 9):
		LocalTime = LocalTime.split()
		#print(str(LocalTime[2]) + "---After Offset")
		return(LocalTime[2])
	else:
		#print(str(LocalTime) + "---After Offset")
		return(LocalTime)

def Main(argv):
	user_name = sys.argv[1]
	ListOfTimes = []
	for tweet in tweepy.Cursor(api.user_timeline, id = user_name).items(160):
	        FullTweet = (tweet._json)
        	Created_Date = FullTweet["created_at"]
        	Created_Date = Created_Date.split()
        	Time =  Created_Date[3]
		#print(str(Time) + "---Before Offset")
        	Time = ConvertTime(Time, FullTweet["user"]["utc_offset"])
		Time = Time.split(":")
		Time = int(Time[0])
		ListOfTimes.append(Time)
	List = OrderTime(ListOfTimes)
	Graph(List)

if __name__ == "__main__":
	Main(sys.argv[1:])
