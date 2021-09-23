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
    #line = 0
    while (i < jsons):
        print("%d/%d" % (i, jsons-1))
        #Open the streaming history file from the script directory, encode it so cyrillic alphabets don't cause problems
        with open(os.path.dirname(__file__) + './endsong_%d.json' % (i), 'r', encoding="utf-8") as streamsJson:
            streams = json.load(streamsJson)
            if i == 0:
                start = streams[0]["ts"]
                end = streams[0]["ts"]
            
            for song in streams:
                date = song["ts"]
                if start > date:
                    start = date
                    
                if end < date:
                    end = date
                    
                artistName = song["master_metadata_album_artist_name"]
                songDuration = song["ms_played"]
                trackName = song["master_metadata_track_name"]
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
                        if songDuration > countAsListen:
                            artists[artistName].addSongCount(trackName)
                    except KeyError:
                        print(trackName + " KeyError")
                duration += songDuration
                #line += 1
            i += 1
            #line = 0
    return artists,start,end,duration

def timeformat(start, end):
    startDateTime = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    endDateTime = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    timedelta = endDateTime - startDateTime
    return timedelta 

def guiMain():
    jsons = len([name for name in os.listdir('.') if os.path.isfile(name) and "endsong" in name])
    threshold = 60000 
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



guiMain()


