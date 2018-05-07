import os
import random
import argparse
from pydub import AudioSegment

def read_song_url():
    songUrl = open('./song_url.txt').read().strip().split('\n')
    return songUrl

def convert_to_song(songUrl, shuffle):
    song = []
    songName = []
    for i, line in enumerate(songUrl):
        command = 'youtube-dl --extract-audio --audio-format mp3 '
        line = line.split()
        url = line[0]
        if len(line) == 2:
            name = "\'{}.%(ext)s\'".format(line[1])
        else:
            # need to fix name issue
            name = "\'song{}.%(ext)s\'".format(i)
            #name = "\'%(title)s.%(ext)s\'"
        songName.append(name[1:-8] + 'mp3')
        command += url + ' -o ' + name
        os.system(command)

    song = []
    for name in songName:
        sound = AudioSegment.from_mp3(name)
        song.append(sound)

    if shuffle:
        combine = list(zip(songName, song))
        random.shuffle(combine)
        songName, song = zip(*combine)
        songName = list(songName)
        song = list(song)

    return song, songName

def export_song_collection(song, filename):
    songCollection = song[0]

    for i in range(1, len(song)):
        songCollection += song[i]

    songCollection.export(filename, format='mp3')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='join.mp3', help='output of filename')
    parser.add_argument('--random', action='store_true', help='random shuffle order')
    args = parser.parse_args()

    songUrl = read_song_url()
    song, songName = convert_to_song(songUrl, args.random)
    export_song_collection(song, args.filename)