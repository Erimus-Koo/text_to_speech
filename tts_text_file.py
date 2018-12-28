#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'


'''
把一个文本文件中的每一行，逐行转换为单独的语音，并保存到本地。
主要用于视频剪辑时的配音。
需要预先写好脚本，逐行生成语音后，导入Premiere使用。
'''

import os
import re
import json
import codecs
from xunfei_tts import xunfei_tts


# ═══════════════════════════════════════════════

AUE = 'lame'  # raw=wav, lame=mp3
with open('xunfei_access.private.json', 'r') as f:
    data = json.load(f)
    APPID = data['APPID']
    API_KEY = data['API_KEY']

language = 'intp65'  # aisound:普通效果, intp65:中文, intp65_en:英文, mtts:小语种需配合小语种发音人使用, x:优化效果
voice = 'xiaoyan'  # https://www.xfyun.cn/services/online_tts

# ═══════════════════════════════════════════════


def legalFileName(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, '', title)  # 替换为下划线
    return new_title


def tts_every_lines(textFile):
    with codecs.open(textFile, 'r', 'utf-8') as f:
        lines = [i.strip() for i in f.readlines()]

    currentPath = os.path.split(os.path.realpath(__file__))[0]
    resultPath = 'audio_' + ''.join(textFile.split('.')[:-1])

    for i, text in enumerate(lines):
        if not text:
            continue
        filename = '%03d_%s' % (i + 1, legalFileName(text)[:10])
        filename = os.path.join(currentPath, resultPath, filename)
        result = xunfei_tts(text, AUE, APPID, API_KEY, voice, language)
        if result:
            ext = '.wav'if AUE == "raw" else '.mp3'
            fullPath = filename + ext
            folder_check(fullPath)
            with codecs.open(fullPath, 'wb') as f:
                f.write(result)


# 文件夾若不存在 創建文件夾
def folder_check(file):
    path = os.path.split(file)[0]
    if not os.path.exists(path):
        print('Create folder:', path)
        os.makedirs(path)


# ═══════════════════════════════════════════════


if __name__ == '__main__':
    file = 'test.txt'
    tts_every_lines(file)
