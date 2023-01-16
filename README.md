# MandarinDictantPreprocessor
Language learning tool. Split Chinese content with subtitles into chunks for listening training

### Usage
Split video into chunks according to subtitles (1 subtitile = 1 chunk)
```
python .\preprocessor.py video_file.mp4 subtitle_file.srt
```

Download video and Chinese srt subtitles from YouTube (id = shotcut link letters)
```
python .\utils.py yt youtube_video_id
```