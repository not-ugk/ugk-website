import pygit2
import datetime
import csv
import codecs

class Song:

    def __init__(self, line, commit_time):
        print(f"creating song! {line}")
        self.most_recent_state = line[0] #should be + or -
        self.first_encountered =  datetime.datetime.fromtimestamp(commit_time)
        #change this to just get id, I think the strange characters are causing the problem
        reader = list(csv.reader([codecs.decode(line[1:]]))
        print("reading")
        try:
            blah = reader[0]
            self.id = reader[0][2]
        except:
            print("An exception occurred") 
        print(f"{self.id}")

    def update(self, commit_time):
        self.first_encountered = datetime.datetime.fromtimestamp(commit_time)
        return self

    id: str
    most_recent_state: str
    first_encountered: datetime

def new_songs_sort(ns: Song):
    return ns.first_encountered

def parse_diff(patch: str, commit_time: int, songs):
    updated_songs = songs
    #print(patch)
    lines = iter(patch.splitlines())
    iterating = True
    processing = False
    while(iterating):
        try:
            line = next(lines)
            print("iterating " + line)
            if (processing == False):
                print("not processing!")
                if (line == "diff --git a/dbexport.csv b/dbexport.csv"):
                #skip next 3 lines, prepare for actual parsing
                    _ = next(lines)
                    _ = next(lines)
                    _ = next(lines)
                    print("processing true!")
                    processing = True
                #else loop
            else: #actual processing
                print(f"processing! {line}")
                print(f"line starts with + {str(line.startswith('+'))}")
                print(f"line starts with - {str(line.startswith('-'))}")
                if (line.startswith('+') or line.startswith('-')):
                    # if first time seeing song, add to list. Otherwise update timestamp
                    song = Song(line, commit_time)
                    print(f"TYPE SONG: {str(type(songs))}")
                    print(f"TYPE ID: {str(type(song.id))}")
                    if song.id not in updated_songs:
                        updated_songs[song.id] = song
                    else:
                        updated_songs[song.id] = updated_songs[song.id].update(commit_time)
                elif (line.find("diff --git") != -1): #this is assuming the line for dbexport diff doesn't show up more than once. It shouldn't
                    processing = False
        except StopIteration:
            print("done iterating")
            iterating = False
    #sort dict by added date, turn into list, make into file
    return updated_songs
    # songs = list(newSongs.values())
    # songs.sort(key = newSongsSort)
    # for s in songs:
    #     print(s.date + s.artist + s.title)
def fetch_recently_added():
    repo = pygit2.Repository("./")
    mostRecent = repo[repo.head.target]
    diving = True
    commit = mostRecent
    songs = dict()
    try:
        while(diving):
            parent = commit.parents[0]
            diff = repo.diff(parent, commit, flags=pygit2.enums.DiffOption.MINIMAL)
            #may not work as expected:
            songs = parse_diff(diff.patch, commit.commit_time, songs)
            commit = parent
    except IndexError:
        diving = False

    return songs