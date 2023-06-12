import json, datetime, operator, os
import tkinter as tk
from io import open
from Classes.Artist import Artist
    
#Artist dictionary printing method, not used
def outputDictionary(artists: dict):
    #Sorting artists dictionary
    artists = sorted(artists.values(), key=operator.attrgetter('duration'), reverse=True)
    for artist in artists:
        if artist.count <= 5 or artist.duration < 3600000:
            continue
        else:
            print(artist)
    #[0:30]

#Forming the artists dictionary and collecting data
def formArtists(jsons: list, threshold: int = 5000) -> tuple[dict, datetime.datetime, datetime.datetime, int]:
    #Artist dictionary that contains artist objects
    artists = {}
    #Threshold is how many ms to have been streamed a song to be counted
    #Total duration of streamed songs, which were streamed longer than threshold variable
    duration = 0
    #Keeping count of jsons
    jsonCount = len(jsons)
    i = 0
    while (i < jsonCount):
        print("%d/%d" % (i+1, jsonCount))
        #Open the streaming history file from the script directory, encoding so cyrillic alphabets don't cause problems(?)
        with open(os.path.dirname(__file__) + './' + jsons[i], 'r', encoding="utf-8") as streamsJson:
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
                if artistName not in artists.keys():
                    artists[artistName] = Artist(artistName)

                if trackName not in artists[artistName].tracks.keys():
                    artists[artistName].addSong(trackName)
                
                try:
                    if songDuration > threshold:
                        artists[artistName].addSongCount(trackName)
                        artists[artistName].addDuration(songDuration)
                except KeyError:
                    print(trackName + " KeyError")

                duration += songDuration
            i += 1
    return artists,start,end,duration

def timeformat(start: datetime.datetime, end: datetime.datetime) -> datetime.datetime:
    startDateTime = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    endDateTime = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    timedelta = endDateTime - startDateTime
    return timedelta 

def guiMain():
    jsons = [name for name in os.listdir('.') if os.path.isfile(name) and ".json" in name]
    threshold = 60000 
    #If there is user input handling
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
    jsons = [name for name in os.listdir('.') if os.path.isfile(name) and "endsong" in name]
    threshold = 60000 
    #If there is user input handling
    if threshold == None:
        artists,start,end,duration = formArtists(jsons)
    else:
        artists,start,end,duration = formArtists(jsons, threshold)

    print(artists["Reverend Bizarre"])

if __name__ == "__main__":
    guiMain()
    #jsons = [name for name in os.listdir('.') if os.path.isfile(name) and ".json" in name]
    #jsonCount = len(jsons)

    
