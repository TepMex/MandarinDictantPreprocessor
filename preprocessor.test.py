# -*- coding: utf-8 -*-
# Unit testing
import unittest
import pysrt
from preprocessor import *

class TestJsonGeneration(unittest.TestCase):
    def setUp(self):
        self.expected = {
            'id': 100500,
            'syllable_count': 13,
            'tones': [1, 2, 2, 2, 4, 1, 2, 3, 1, 4, 5, 4, 1],
            'pinyin': [
                'zhong1', 'guo2', 'qi2', 'tan2', 'di4',
                'yi1', 'ji2', 'xiao3', 'yao1', 'guai4',
                'de5', 'xia4', 'tian1'
            ],
            'hanzi': '中国奇谭第一集小妖怪的夏天'
        }
        self.dummy_sub = pysrt.SubRipItem(100500, None, None,
                                          '中国奇谭第一集（小妖怪的夏天）')

    def test_id_recording(self):
        '''id from srt-chunk number'''
        actual = subtitle_part_to_dict(self.dummy_sub, 'chunk.mp4')
        self.assertEqual(actual['id'], self.expected['id'])

    def test_pinyin_extraction(self):
        '''pinyin from srt-chunk hanzi text'''
        actual = subtitle_part_to_dict(self.dummy_sub, 'chunk.mp4')
        self.assertEqual(actual['pinyin'], self.expected['pinyin'])

    def test_syllable_count(self):
        '''each Chinese hanzi must be counted as 1 syllable'''
        actual = subtitle_part_to_dict(self.dummy_sub, 'chunk.mp4')
        self.assertEqual(actual['syllable_count'],
                         self.expected['syllable_count'])

    def test_hanzi_output(self):
        '''in resultng JSON must be only hanzi, no other symbols'''
        actual = subtitle_part_to_dict(self.dummy_sub, 'chunk.mp4')
        self.assertEqual(actual['hanzi'], self.expected['hanzi'])

    def test_tones_count(self):
        '''tones array'''
        actual = subtitle_part_to_dict(self.dummy_sub, 'chunk.mp4')
        self.assertEqual(actual['tones'], self.expected['tones'])


class TestFFmpegGraphGeneration(unittest.TestCase):
    pass

unittest.main(argv=[''], verbosity=2, exit=False)