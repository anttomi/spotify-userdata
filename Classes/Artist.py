class Artist:
    def __init__(self, name):
        self.name = name
        self.duration = 0
        self.tracks = {}

    def addDuration(self, duration):
        self.duration += duration

    def getDurationHours(self):
        return self.duration/1000/60/60
        
    def addSong(self, track):
        self.tracks[track] = 0

    def addSongCount(self, track):
        self.tracks[track] += 1

    def getSortedList(self):
        return sorted(self.tracks.items(), key=lambda x: int(x[1]), reverse=True)
    
    def getMostPlayedSong(self):
        mostpl =  max(self.tracks, key=self.tracks.get)
        return "(%s, %i)" % (mostpl, self.tracks[mostpl])
    
    def getPlayCount(self):
        return sum(self.tracks.values())

    def __str__(self):
        return "\n%s \nTimes Played: %s \nDuration: " % (self.name, self.getPlayCount()) + '{:.2f}'.format(self.getDurationHours()) + "\nMost Played Song: " + self.getMostPlayedSong() +"\n"
