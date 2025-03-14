import pygit2
import datetime

class SongUpdate:

    def __init__(self, state, date, song):
        self.state = state
        self.date = date
        self.song = song

    def key(self):
        return self.state + self.date + self.song

    state: str
    date: str
    song: str

def newSongsSort(ns: SongUpdate):
    return ns.date

def parseDiff(patch: str, commit_time: int):
    print(patch)
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
                if (line.startswith('+') or line.startswith('-')):
                    # parse line into SongUpdate and add to dict
                    update = lineToSongUpdate(line, commit_time)
                    newSongs[update.key()] = update
                elif (line.find("diff --git") != -1): #this is assuming the line for dbexport diff doesn't show up more than once. It shouldn't
                    processing = False
        except StopIteration:
            print("done iterating")
            iterating = False
    #sort dict by added date, turn into list, make into file
    return newSongs
    # songs = list(newSongs.values())
    # songs.sort(key = newSongsSort)
    # for s in songs:
    #     print(s.date + s.artist + s.title)

def lineToSongUpdate(line: str, commit_time: int):
    split = line.replace("\"", "")
    firstChar = split[0][0] #should be + or -
    return SongUpdate(firstChar, str(datetime.datetime.fromtimestamp(commit_time)), split[1:])

def printSongUpdates():
    repo = pygit2.Repository("../")
    mostRecent = repo[repo.head.target]
    diving = True
    commit = mostRecent
    songs = []
    try:
        while(diving):
            parent = commit.parents[0]
            diff = repo.diff(parent, commit, flags=pygit2.enums.DiffOption.MINIMAL)
            songs.append(parseDiff(diff.patch, commit.commit_time))
            commit = parent
    except IndexError:
        diving = False

    # print(f"{[for item in list]})

    removals = {}
    print("PRINTING SONG UPDATES")
    print("================================================================")
    for updates in songs:
        for update in list(updates.values()):
            if (update.state == '-'):
                removals[update.date + update.song] = update
            if (update.state == '+'):
                if removals.get(update.date + update.song) == None:
                    print(update.date + " " + update.song)

printSongUpdates()
