# -*- coding: utf-8 -*-
"""DictantPreprocessor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KF2MRLTY2loGxtZVylgAMt2lWY-Mj0pQ
"""

#!git clone https://github.com/rokibulislaam/colab-ffmpeg-cuda.git

#!chmod +x ./colab-ffmpeg-cuda/build && ./colab-ffmpeg-cuda/build --build

#!cp -r ./colab-ffmpeg-cuda/bin/. /usr/bin/

#!ffmpeg -version

# Commented out IPython magic to ensure Python compatibility.
#!pip install ipython-autotime
# %load_ext autotime

#!pip install ffmpeg-python

#!pip install git+https://github.com/pytube/pytube

#!pip install youtube_transcript_api

#!pip install pysrt

#!pip install -U xpinyin

import pysrt
from pysrt.srtitem import SubRipTime
import ffmpeg
from xpinyin import Pinyin
import json
import re
import sys

def subtitle_part_to_dict(subtitle, file_name):
    filtered_text = get_only_hanzi_from(subtitle.text)
    syllable_count = len(filtered_text)

    pinyin_str = get_pinyin_from_hanzi(filtered_text)
    tones_str = re.sub('[^0-9]', '', pinyin_str)

    return {
        'id': subtitle.index,
        'file_path': file_name,
        'syllable_count': syllable_count,
        'tones': [int(tone_number) for tone_number in tones_str],
        'pinyin': pinyin_str.split(' '),
        'hanzi': filtered_text
    }


def get_only_hanzi_from(text):
    return re.sub(r'[^\u4e00-\u9fff]+', '', text)


def get_pinyin_from_hanzi(text):
    pinyin_str = Pinyin().get_pinyin(text, splitter=' ', tone_marks='numbers')
    pinyin_str = re.sub(r'[)(]', r'', pinyin_str)
    return pinyin_str


def subtitle_part_to_ffmpeg_graph(input_file, output_file, subtitle_item):
    start_time = subtitle_item.start.to_time()
    end_time = subtitle_item.end.to_time()

    input = ffmpeg.input(input_file)

    audio = input.audio.filter('atrim',
                               start=start_time,
                               end=end_time)

    video = input.video.filter('trim',
                               start=start_time,
                               end=end_time)

    return ffmpeg.output(audio, video, output_file)


def get_chunk_file_name(subtitle_item, input_file):
    chunk_file_name = str(
        subtitle_item.start.to_time()
    ).replace(':', '_').replace('.', '_')
    return f'{chunk_file_name}_{input_file}'


def dictant_preprocess(video_file, subtitles_file):
    subs = pysrt.open(subtitles_file)

    result_json = []
    result_ffmpeg = []
    for sub in subs:
        chunk_file_name = get_chunk_file_name(sub, video_file)
        json_item = subtitle_part_to_dict(sub, chunk_file_name)
        result_json.append(json_item)

        ffmpeg_graph = subtitle_part_to_ffmpeg_graph(
            video_file, chunk_file_name, sub
        )
        # print(ffmpeg_graph.compile())
        result_ffmpeg.append(ffmpeg_graph)

    save_processed_json(video_file, result_json)
    run_ffmpeg_trims(result_ffmpeg[:5])


def run_ffmpeg_trims(ffmpeg_nodes):
    logs = []
    for node in ffmpeg_nodes:
        log = run_ffmpeg_node(node)
        logs.append(log)
    print(logs)


def run_ffmpeg_node(ffmpeg_node):
    try:
        stdout, err = ffmpeg_node.run(capture_stderr=True, capture_stdout=True)
        return (stdout, err)
    except ffmpeg.Error as e:
        print(e.stderr)
        print(e.stdout)


def save_processed_json(input_file, json_obj):
    json_str = json.dumps(json_obj)

    with open(f'{input_file}.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)

def main():
    print(sys.argv)
    # dictant_preprocess('Vws4DE7UvtM.mp4', 'Vws4DE7UvtM.srt')

# Run test
#unittest.main(argv=[''], verbosity=2, exit=False)

