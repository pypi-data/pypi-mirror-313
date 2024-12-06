# https://open.spotify.com/get_access_token   Here you get access token to spotify (for what?)
from yta_general_utils.programming.env import get_current_project_env
from musixmatch import Musixmatch

import requests


MUSIXMATCH_API_KEY = get_current_project_env('MUSIXMATCH_API_KEY')

def get_lyrics_from_musixmatch(song_id):
    musixmatch = Musixmatch(MUSIXMATCH_API_KEY)

    # example id: 15953433
    return musixmatch.track_lyrics_get(song_id)

def get_song_lyrics_srt(author, song, output_filename):
    """
    Looks for the 'author's 'song' lyrics and, if found, builds an SRT file
    with those lyrics and stores it locally as 'output_filename'.
    """
    lyrics = get_timestamped_lyrics(author, song)

    if lyrics:
        timestamped_lyrics_to_srt(lyrics, output_filename)

def get_timestamped_lyrics(author, song):
    # Found here: https://stackoverflow.com/questions/62253539/api-with-lyrics-and-timestamps
    # This below works
    #url = 'https://api.textyl.co/api/lyrics?q=alan%20walker%20faded'
    # TODO: Find a better solution because this one doesn't take care about when the
    # author is not singing. The lyric is shown even when voice silence, and I don't
    # want that. This returns the moment in which a sentence starts, but not when it
    # ends, just when the next one starts, that is not the same.
    url = 'https://api.textyl.co/api/lyrics?q=' + author + ' ' + song

    response = requests.get(url)
    response = response.json()

    return response

def timestamped_lyrics_to_srt(timestamped_lyrics, output_filename):
    index = 0
    srt_content = ''
    while index < (len(timestamped_lyrics) - 1):
        # TODO: This fails if only 1 timestamp_lyric element
        timestamped_lyric = timestamped_lyrics[index]
        srt_content += str(index + 1) + '\n'

        m, s = divmod(timestamped_lyric['seconds'], 60)
        h, m = divmod(m, 60)
        
        srt_content += '{:d}:{:02d}:{:02d},000'.format(h, m, s) + ' --> '

        m, s = divmod(timestamped_lyrics[index + 1]['seconds'], 60)
        h, m = divmod(m, 60)
        srt_content += '{:d}:{:02d}:{:02d},000'.format(h, m, s) + '\n'

        srt_content += timestamped_lyric['lyrics'] + '\n'
        srt_content += '\n'

        index += 1

    # Write .srt file
    with open(output_filename, 'w') as outfile:
        outfile.write(srt_content)

       
    """
    # This is the SRT format
    1
    00:00:00,000 --> 00:00:02,500
    Welcome to the Example Subtitle File!

    """


