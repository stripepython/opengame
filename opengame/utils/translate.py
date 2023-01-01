import os
import re
import json
from string import Template
from typing import Optional, Dict, Union

import requests
import execjs

from ..exceptions import OpenGameError

__all__ = ['languages', 'engines', 'Translator']


class languages(object):
    auto = 'auto'
    english = 'en'
    france = 'fra'
    spanish = 'spa'
    chinese = 'zh'
    japanese = 'jp'
    japanese_kana = 'jpka'
    thai = 'th'
    korean = 'kor'
    turkish = 'tr'
    vietnamese = 'vie'
    malay = 'ms'
    german = 'de'
    russian = 'ru'
    iranian = 'ir'
    arabic = 'ara'
    estonian = 'est'
    belarusian = 'be'
    bulgarian = 'bul'
    hindi = 'hi'
    icelandic = 'is'
    polish = 'pl'
    farsi = 'fa'
    danish = 'dan'
    filipino = 'tl'
    finnish = 'fin'
    dutch = 'nl'
    catalan = 'ca'
    czech = 'cs'
    croatian = 'hr'
    latvian = 'lv'
    lithuanian = 'lt'
    romanian = 'rom'
    south_african = 'af'
    norwegian = 'no'
    brazilian = 'pt_BR'
    portuguese = 'pt'
    swedish = 'swe'
    serbian = 'sr'
    esperanto = 'eo'
    slovak = 'sk'
    slovenian = 'slo'
    swahili = 'sw'
    ukrainian = 'uk'
    hebrew = 'iw'
    greek = 'el'
    hungarian = 'hu'
    armenian = 'hy'
    italian = 'it'
    indonesian = 'id'
    albanian = 'sq'
    amharic = 'am'
    assamese = 'as'
    azerbaijani = 'az'
    basque = 'eu'
    bengali = 'bn'
    bosnian = 'bs'
    galician = 'gl'
    georgian = 'ka'
    gujarati = 'gu'
    hausa = 'ha'
    igbo = 'ig'
    inuit = 'iu'
    irish = 'ga'
    zulu = 'zu'
    kannada = 'kn'
    kazakh = 'kk'
    kyrgyz = 'ky'
    luxembourgish = 'lb'
    macedonian = 'mk'
    maltese = 'mt'
    maori = 'mi'
    marathi = 'mr'
    nepali = 'ne'
    oriya = 'or'
    punjabi = 'pa'
    kachua = 'qu'
    seswana = 'tn'
    sinhala = 'si'
    tamil = 'ta'
    tatar = 'tt'
    telugu = 'te'
    urdu = 'ur'
    uzbek = 'uz'
    welsh = 'cy'
    yoruba = 'yo'
    cantonese = 'yue'
    classical_chinese = 'wyw'
    traditional_chinese = 'cht'
    

class engines(object):
    node = node_js = 'Node'
    pyv8 = 'PyV8'
    java_script_core = 'JavaScriptCore'
    spidermonkey = spider_monkey = 'SpiderMonkey'
    jscript = 'JScript'
    phantomjs = 'PhantomJS'
    slimerjs = 'SlimerJS'
    nashorn = 'Nashorn'
    

_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/68.0.3440.106 Safari/537.36'
)
_GTK = '320305.131321201'
_JS = os.path.join(os.path.dirname(__file__), 'baidu.js')

with open(_JS, 'r', encoding='utf-8') as js_file:
    _JS_TEMPLATE = Template(js_file.read())


def _get_sign(word: str):
    js = _JS_TEMPLATE.substitute(word=word, gtk=_GTK)
    return execjs.compile(js).call('e', word)


def _get_token(session: requests.Session, headers: Dict[str, str], cookies: Optional[Dict[str, str]], proxies: Optional[Dict[str, str]]):
    url = 'https://fanyi.baidu.com/?aldtype=16047'
    response = session.get(url, headers=headers, cookies=cookies, proxies=proxies)
    
    html = response.text
    token = re.findall("token: '(.*)'", html)
    if not token:
        raise OpenGameError('not found token')
    return token[0]


class Translator(object):
    def __init__(self, input_language: str = languages.auto, output_language: str = languages.english,
                 session: Optional[requests.Session] = None, js_engine: str = engines.node_js,
                 cookies: Optional[Union[Dict[str, str], str]] = None, user_agent: str = _USER_AGENT,
                 proxies: Optional[Dict[str, str]] = None, other_headers: Optional[Dict[str, str]] = None):
        os.environ['EXECJS_RUNTIME'] = js_engine
        self.url = 'https://fanyi.baidu.com/v2transapi'
        if not other_headers:
            other_headers = {}
            
        self.headers = {'User-Agent': user_agent, **other_headers}
        if isinstance(cookies, str):
            self.headers['Cookie'] = cookies
            cookies = None
        self.cookies = cookies
        
        if not session:
            session = requests.session()
        self.session = session
        
        if not proxies:
            proxies = {}
        self.proxies = proxies.copy()

        self.form = {
            'from': input_language,
            'to': output_language,
            'query': '',
            'transtype': 'translang',
            'simple_means_flag': '3',
            'domain': 'common',
            'sign': '',
            'token': ''
        }
        self.data = {}
    
    def load(self, text: str):
        self.form['query'] = text
        self.form['sign'] = _get_sign(text)
        self.form['token'] = _get_token(self.session, self.headers, self.cookies, self.proxies)
    
    def get(self, **kwargs):
        response = self.session.post(self.url, data=self.form, headers=self.headers,
                                     cookies=self.cookies, proxies=self.proxies, **kwargs)
        response.encoding = 'utf-8'
        self.data = json.loads(response.text)
        if 'errno' in self.data:
            code = self.data['errno']
            msg = self.data.get('errmsg', '')
            raise OpenGameError(f'translate error [No {code}] {msg}')
        
        return self.data['trans_result']['data'][0]['dst']
