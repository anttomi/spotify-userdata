import json, datetime, operator, os
import tkinter as tk
from io import open

class Artist:
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.duration = 0
        self.tracks = {}

    def addCount(self):
        self.count += 1

    def addDuration(self, duration):
        self.duration += duration

    def getDurationHours(self):
        return self.duration/1000/60/60
        
    def addSong(self, track):
        self.tracks[track] = 1

    def addSongCount(self, track):
        self.tracks[track] += 1

    def getSortedList(self):
        songs = self.tracks
        return sorted(songs.items(), key=lambda x: int(x[1]), reverse=True)
    
    def getMostPlayedSong(self):
        songs = self.tracks
        songs = sorted(songs.items(), key=lambda x: int(x[1]), reverse=True)
        return songs[0]

    def __str__(self):
        return "\n%s \nTimes Played: %s \nDuration: " % (self.name, self.count) + '{:.2f}'.format((self.duration/1000)/60/60) + "\nMost Played Song: " + str(self.getMostPlayedSong()) +"\n"


#Artist dictionary printing method
def outputDictionary(artists):
    #Sorting artists dictionary
    artists = sorted(artists.values(), key=operator.attrgetter('duration'), reverse=True)
    for artist in artists:
        if artist.count <= 5 or artist.duration < 3600000:
            continue
        else:
            print(artist)
    #[0:30]


#Forming the artists dictionary and collecting data
def formArtists(jsons, threshold=5000):
    #Temp artist names list for easier structure in main
    artistNames = []
    #Artist dictionary that contains artist objects
    artists = {}
    #How many ms to have been streamed a song to be counted
    countAsListen = threshold
    #Total duration of streamed songs, which were streamed more than countAsListen threshold variable
    duration = 0
    #Keeping count of jsons
    i = 0
    while (i < jsons):
        #Open the streaming history file from the script directory, encode it so cyrillic alphabets doesn't cause problems
        with open(os.path.dirname(__file__) + './StreamingHistory%d.json' % (i), 'r', encoding="utf-8") as streamsJson:
            streams = json.load(streamsJson)
            #Set date of first and last stream
            if i == 0:
                start = streams[0]["endTime"]
            if i == jsons-1:
                end = streams[len(streams)-1]["endTime"]
            for song in streams:
                artistName = song["artistName"]
                songDuration = song["msPlayed"]
                trackName = song["trackName"]
                #if artist not created, then create an artist object and a first stream
                if artistName not in artistNames:
                    artistNames.append(artistName)
                    artists[artistName] = Artist(artistName)
                    if songDuration > countAsListen:
                        artists[artistName].addCount()
                        artists[artistName].addDuration(songDuration)
                else:
                    #if artist already created, add a playcount to it if song duration exceeds the threshold
                    if songDuration > countAsListen:
                        artists[artistName].addCount()
                        artists[artistName].addDuration(songDuration)

                if trackName not in artists[artistName].tracks:
                    artists[artistName].addSong(trackName)
                else:
                    try:
                        artists[artistName].addSongCount(trackName)
                    except KeyError:
                        print(trackName + " KeyError")
                duration += songDuration
            i += 1
    return artists,start,end,duration

def timeformat(start, end):
    startDateTime = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M')
    endDateTime = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M')
    timedelta = endDateTime - startDateTime
    return timedelta 

def guiMain():
    jsons = len([name for name in os.listdir('.') if os.path.isfile(name) and "StreamingHistory" in name])
    threshold = 5000
    if threshold == None:
        artists,start,end,duration = formArtists(jsons)
    else:
        artists,start,end,duration = formArtists(jsons, threshold)

    window = tk.Tk()
    timedelta = timeformat(start, end)
    label = tk.Label(text="Streams are between %s hours (%s - %s)\nHours streamed: " % (timedelta, start, end) +
        '{:.2f}'.format((duration/1000)/60/60))
    label.pack()
    artists = sorted(artists.values(), key=operator.attrgetter('duration'))
    textbox = tk.Text()
    textbox.pack()
    for artist in artists:
        textbox.insert(1.0, artist)
    tk.mainloop()

def main():
    while True:
        #Global variables
        #How many iterations
        
        #Dynamic script path
        #Threshold for counting a listen
        #try:
         #   t = int(input("Input threshold for counting (seconds, default 5s): "))*1000
        #except ValueError as ve:
        #    t = None
        #finally:
        #    threshold = t
        #Artists is a dictionary of artist objects
        #Start is datetime of the first stream
        #End is datetime of the latest stream
        #Duration is total duration listened
        
        #Time formatting for timedelta maths
        #print("Now displaying artists that only have over 1 hour in playtime\n")
        #print("Streams are between %s \nHours: " % (timedelta) +
        #'{:.2f}'.format((duration/1000)/60/60) + " tuntia")
        #print("Artist count: " + str(len(artists)))
        #outputDictionary(artists)
        #done = input("Press enter to exit, otherwise continue\n")
        #if (done == ""):
        break



guiMain()


