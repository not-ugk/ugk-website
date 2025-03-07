import pygit2
import datetime

repo = pygit2.Repository("../")

commit = repo[repo.head.target]
diff = repo.diff(commit.parents[0], commit, flags=pygit2.enums.DiffOption.MINIMAL)

class SongUpdate:

    def __init__(self, date, artist, title):
        self.date = date
        self.artist = artist
        self.title = title

    date: str
    artist: str
    title: str

def newSongsSort(ns: SongUpdate):
    return ns.date

def parseDiff(patch: str, commit_time: int):
    lines = iter(patch.splitlines())
    iterating = True
    processing = False
    newSongs = dict()
    while(iterating):
        try:
            line = next(lines)
            #print("iterating " + line)
            if (processing == False):
                #print("not processing!")
                if (line == "diff --git a/dbexport.csv b/dbexport.csv"):
                #skip next 3 lines, prepare for actual parsing
                    _ = next(lines)
                    _ = next(lines)
                    _ = next(lines)
                    #print("processing true!")
                    processing = True
                #else loop
            else: #actual processing
                #print("processing!")
                if (line.startswith('+')):
                    # parse line into SongUpdate and add to dict
                    print("Add: "+ line)
                    update = lineToSongUpdate(line, commit_time)
                    newSongs[update.artist + update.date + update.title] = update
                elif (line.startswith('-')):
                    # parse line to SongUpdate and remove from dict if it is there    
                    print("Remove "+ line)
                    remove = lineToSongUpdate(line, commit_time)
                    if (newSongs.get(remove.artist + remove.date + remove.title)):
                        newSongs.pop(remove.artist + remove.date + remove.title)
                elif (line.find("diff --git") != -1): #this is assuming the line for dbexport diff doesn't show up more than once. It shouldn't
                    processing = False
        except StopIteration:
            print("done iterating")
            iterating = False
    #sort dict by added date, turn into list, make into file
    songs = list(newSongs.values())
    songs.sort(key = newSongsSort)
    for s in songs:
        print(s.date + s.artist + s.title)

def lineToSongUpdate(line: str, commit_time: int):
    split = line.replace("\"", "").replace("+", "").replace("-", "").split(",")
    return SongUpdate(str(datetime.datetime.fromtimestamp(commit_time)), split[0], split[1])

parseDiff(diff.patch, commit.commit_time)