from google.cloud import translate


class GoogleTranslate:

    def __init__(self):
        self.translate_client = translate.Client.from_service_account_json('/vlim-telegram-bot-secret-key.json')

    def translate(self, target, source_word):
        shortcut = {
            'ch': 'zh-CN',
            'kh': 'km',
        }
        if target in shortcut:
            target = shortcut[target]
        translation = self.translate_client.translate(source_word, target_language=target)
        # noinspection PyTypeChecker
        return translation['translatedText']