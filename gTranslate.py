## google translate from Vadym Zakovinko (identify function added)
## at https://github.com/Quard/gtranslate/blob/master/gtranslate/__init__.py
## you need a payed google.api key to push requests to google translate

import urllib
try:
    import simplejson
except ImportError:
    import json as simplejson


__author__ = 'Vadym Zakovinko'
__email__ = 'vp@zakovinko.com'


GTRANSLATE_URL = 'https://www.googleapis.com/language/translate/v2'
LANGUAGES = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Arabic': 'ar',
    'Belarusian': 'be',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Chinese Simplified': 'zh-CN',
    'Chinese Traditional': 'zh-TW',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'Galician': 'gl',
    'German': 'de',
    'Greek': 'el',
    'Haitian Creole': 'ht',
    'Hebrew': 'iw',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Macedonian': 'mk',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Yiddish': 'yi',
}

class IvalidLanguage(Exception):
    pass


class SameLanguages(Exception):
    pass


class Translate(object):

    def __init__(self, api_key, source=None, target=None):
        self._api_key = api_key
        self._source = source
        self._target = target

    def __get_language__(self, lng):
        try:
            lng = LANGUAGES[lng]
        except KeyError:
            if not lng in LANGUAGES.values():
                raise IvalidLanguage('%s not known' % lng)

        return lng

    def translate(self, phrase, source=None, target=None):
        source = source or self._source
        target = target or self._target
        source = self.__get_language__(source)
        target = self.__get_language__(target)
        phrase = urllib.quote(phrase.encode('utf-8'))

        if source == target:
            raise SameLanguages('Use different languages')

        args = {
            'key': self._api_key,
            'source': source,
            'target': target,
        }
        if not hasattr(phrase, '__iter__'):
            args['q'] = phrase
        url = '%s?%s' % (GTRANSLATE_URL, urllib.urlencode(args))
        if hasattr(phrase, '__iter__'):
            url += '&q=' + '&q='.join([urllib.quote(q) for q in phrase])
        try:
            content = urllib.FancyURLopener().open(url)
            json = simplejson.load(content)
        except:
            return None
        try:
            translations = json['data']['translations']
        except KeyError:
            pass
        else:
            if hasattr(translations, '__iter__'):
                return [i['translatedText'] for i in translations]

            return translations

        return None

    @property
    def languages(self):
        return LANGUAGES


def translate(phrase, source, target, api_key):
    translator = Translate(api_key)
    print "translated"
    return translator.translate(phrase, source=source, target=target)

def identify(phrase,api_key):
    """Pushes request to google to identify languages"""
    phrase = urllib.quote(phrase.encode('utf-8'))
    request = '%s/detect?key=%s&q=%s' % (GTRANSLATE_URL,api_key,phrase)
    content = urllib.FancyURLopener().open(request)
    json = simplejson.load(content)
    result = json['data']['detections'][0][0]
    language = result['language']
    return language
