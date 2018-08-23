#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

'''
这是利用了 讯飞 的 在线文本转语音 api，把单句文本转为语音文件，并保存到本地。
需要先填入 APPID 和 API_KEY。
详情见 https://www.xfyun.cn/services/online_tts
'''

import json
import requests
import time
import hashlib
import base64
import os

# ═══════════════════════════════════════════════

# init setting
URL = 'http://api.xfyun.cn/v1/service/v1/tts'
AUE = 'lame'  # raw=wav, lame=mp3
APPID = ''  # your appid
API_KEY = ''  # your api key
if not APPID or API_KEY:
    with open('xunfei_access.private.json', 'r') as f:
        data = json.load(f)
        APPID = data['APPID']
        API_KEY = data['API_KEY']

language = 'intp65'  # aisound:普通效果, intp65:中文, intp65_en:英文, mtts:小语种需配合小语种发音人使用, x:优化效果
voice = 'xiaoyan'

# ═══════════════════════════════════════════════


def getHeader(AUE, APPID, API_KEY, voice, language):
    curTime = str(int(time.time())).encode('utf-8')

    param = {
        'aue': AUE,
        'auf': 'audio/L16;rate=16000',
        'voice_name': voice,
        'engine_type': language,
    }
    paramBytes = str(param).encode('utf-8')
    # fix format (if ' or space exists, returns params error.)
    paramBytes = paramBytes.replace(b'\'', b'\"').replace(b' ', b'')
    paramBase64 = base64.b64encode(paramBytes)

    m2 = hashlib.md5()
    m2.update(API_KEY.encode('utf-8') + curTime + paramBase64)
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def xunfei_tts(text, AUE='lame', APPID='', API_KEY='',
               voice='xiaoyan', language='intp65'):
    header = getHeader(AUE, APPID, API_KEY, voice, language)
    data = {'text': text}
    r = requests.post(URL, headers=header, data=data)
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        print("success | sid: %s | %s" % (sid, text[:10]))
        return r.content
    else:
        print(r.text)


# ═══════════════════════════════════════════════


if __name__ == '__main__':
    text = '床前明月光，疑是地上霜。'
    text += 'The moonlight flow on the floor, just like frost.'

    # return binary audio file
    result = xunfei_tts(text, AUE, APPID, API_KEY, voice, language)
    if result:  # write to test file
        root = os.path.split(os.path.realpath(__file__))[0]
        ext = '.wav'if AUE == "raw" else '.mp3'
        file = os.path.join(root, 'test' + ext)
        with open(file, 'wb') as f:
            f.write(result)
