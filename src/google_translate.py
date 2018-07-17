import json

import requests


class GoogleTranslate:

    def __init__(self):
        pass

    def translate(self, target, source_word, source='auto'):
        shortcut = {
            'ch': 'zh-CN',
            'kh': 'km',
        }
        if target in shortcut:
            target = shortcut[target]
        r = requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=%s&tl=%s&dt=t&q=%s" % (
        source, target, source_word))
        r.encoding = 'utf-8'
        text = r.text.encode('utf-8')
        data = json.loads(text)
        return data[0][0][0]

