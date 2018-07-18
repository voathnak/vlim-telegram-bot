# -*- coding: utf-8 -*-
import re
import sys
import time
from numpy import unique
from csv_data import CSVData
from google_translate import GoogleTranslate
from vlim_telegram import VLIMTelegram
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

reload(sys)
sys.setdefaultencoding('utf8')

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "vlim-bot.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    _logger = logging.getLogger(logger_name)
    _logger.setLevel(logging.INFO)  # better to have too much log than not enough
    _logger.addHandler(get_console_handler())
    _logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    _logger.propagate = False
    return _logger


logger = get_logger("VLIM Bot")

logger.info("Log Level INFO")
print logger.handlers


class Bot:

    def __init__(self):
        self.last_display = ''
        self.last_updated_message = {}
        self.last_updated_message_id = 0
        self.startup_time = datetime.now()
        self.answered_message = []
        self.answered_messages = []
        self.answered_messages_ids = []
        self.answered_question = []
        self.question = []
        self.vlim_telegram = VLIMTelegram()
        self.no_answered_questions = []
        self.no_answered_questions_data = CSVData('no_answered_messages')
        self.no_answered_questions_ids = self.no_answered_questions_data.read_ids()
        self.updates = self.vlim_telegram.getUpdates()
        self.answered_messages_ids_data = CSVData('answered_messages_ids')
        self.answered_messages_ids = self.answered_messages_ids_data.read_ids()
        self.sean_messages_ids = unique(self.answered_messages_ids + self.no_answered_questions_ids).tolist()
        self.messages = []
        self.google_translate = GoogleTranslate()

    def run(self):
        while True:
            time.sleep(1)
            self.action()

    def action(self):
        updates = self.vlim_telegram.getUpdates(offset=-100, limit=100)
        self.messages = filter(lambda x: x.message_id not in self.sean_messages_ids,
                               map(lambda x: x.message, updates))
        if len(updates) > 0:
            if not self.last_updated_message_id == updates[-1].message.message_id:
                self.last_updated_message = updates[-1].message
                self.last_updated_message_id = updates[-1].message.message_id
                logger.info(
                    ">>>>> last_updated_message: %s: %s: %s, %s" % (
                        self.last_updated_message.date,
                        "%s %s (%s)" % (
                            self.last_updated_message.chat.first_name, self.last_updated_message.chat.last_name,
                            self.last_updated_message.chat_id),
                        self.last_updated_message.message_id, self.last_updated_message.text))
        if len(self.messages) > 0:
            logger.info("pending reply messages: %s" % map(lambda x: x.text, self.messages))
            for message in self.messages:
                text = message.text

                greating = ['hey', 'hi', 'Hello', 'Hola']
                greating2 = ['How are you', 'How are you doing', 'How have you been']

                command_pattern = '@([a-z]|[A-Z])+\s'
                matched = re.match(command_pattern, text)

                # Command
                if matched:
                    logger.debug("matched: %s" % matched.group())
                    command = matched.group()[1:-1]
                    searched = re.search('%s.*' % command_pattern, text).group()
                    logger.debug("searched: %s" % searched)
                    context = re.sub(command_pattern, "", text)
                    logger.debug("sub: %s" % context)

                    # GoogleTranslate Command
                    if command == 't' and len(context.split(',')) > 1:
                        target_lang = context.split(',')[0]
                        translate_text = context.split(',')[1]
                        translated_text = self.google_translate.translate(target_lang, translate_text)
                        self.vlim_telegram.send(message.chat.id, translated_text)
                        self.update_answered(message)
                    else:
                        self.update_no_answered_questions(message)

                # Greating
                elif any(x.lower() in text.lower() for x in greating):
                    self.vlim_telegram.send(message.chat.id, "Hello Sir")
                    self.update_answered(message)

                elif any(x.lower() in text.lower() for x in greating2):
                    self.vlim_telegram.send(message.chat.id, "I am fine, Sir.")
                    self.vlim_telegram.send(message.chat.id, "Thank You.")
                    self.update_answered(message)

                else:
                    self.update_no_answered_questions(message)
                    self.vlim_telegram.send(message.chat.id, "I do not know about <<%s>>, Sir." % message.text)
                    self.vlim_telegram.send(message.chat.id, "But I will ask my creator.")

                self.messages.remove(message)
                self.sean_messages_ids = self.answered_messages_ids + self.no_answered_questions_ids

    def update_no_answered_questions(self, message):
        self.no_answered_questions.append(message)
        logger.info("no_answered_questions: %s" % message.text)
        self.no_answered_questions_ids.append(message.message_id)
        self.no_answered_questions_data_ids = self.no_answered_questions_data.read()
        self.no_answered_questions_data_ids.append([message.message_id, message.text])
        self.no_answered_questions_data.write(self.no_answered_questions_data_ids)

    def update_answered(self, message):
        self.answered_messages_ids.append(message.message_id)
        self.answered_messages_ids_data.write(self.answered_messages_ids)


if __name__ == "__main__":
    bot = Bot()
    bot.run()
