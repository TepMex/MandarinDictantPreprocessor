# -*- coding: utf-8 -*-
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
import sys

def download_youtube_mp4(youtube_id):
    yt = YouTube(f'https://youtu.be/{youtube_id}')
    yt.streams.filter(file_extension='mp4').first().download(
        filename=f'{youtube_id}.mp4')


def download_youtube_srt(youtube_id):
    subs = YouTubeTranscriptApi.list_transcripts(youtube_id)
    subs = subs.find_manually_created_transcript(['zh-Hant'])
    subs = subs.fetch()

    formatter = SRTFormatter()

    # .format_transcript(transcript) turns the transcript into a JSON string.
    srt_formatted = formatter.format_transcript(subs)

    # Now we can write it out to a file.
    with open(f'{youtube_id}.srt', 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_formatted)

if __name__ == "__main__":
    command = sys.argv[1]
    if command == 'yt':
        youtube_id = sys.argv[2]
        download_youtube_mp4(youtube_id)
        download_youtube_srt(youtube_id)
