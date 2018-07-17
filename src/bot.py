# -*- coding: utf-8 -*-

import sys
import time
from csv_data import CSVData
from google_translate import GoogleTranslate
from vlim_telegram import VLIMTelegram
from datetime import datetime
import logging
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

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
        self.answered_messages_ids_data = CSVData('answered_messages_ids')
        self.no_answered_questions = []
        self.no_answered_questions_ids = []
        self.no_answered_questions_data = CSVData('no_answered_messages')
        self.updates = self.vlim_telegram.getUpdates()
        self.answered_messages_ids_data.write(map(lambda x: x.message.message_id, self.updates))
        self.answered_messages_ids = self.answered_messages_ids_data.read_ids()
        self.messages = []
        self.google_translate = GoogleTranslate()

    def run(self):
        while True:
            time.sleep(1)
            self.action()

    def action(self):
        updates = self.vlim_telegram.getUpdates(offset=-100, limit=100)
        self.messages = filter(lambda x: x.message_id not in self.answered_messages_ids,
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

                # Command
                if text[0] == "@":
                    if text[1] == 't' and text[2] == ' ' and len(text[3:].split(',')) > 1:
                        target_lang = text[3:].split(',')[0]
                        translate_text = text[3:].split(',')[1]
                        translated_text = self.google_translate.translate(target_lang, translate_text)
                        self.vlim_telegram.send(message.chat.id, translated_text)
                        self.update_answered(message)
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
                    self.update_answered(message)
                    self.vlim_telegram.send(message.chat.id, "What do you mean?, Sir.")

                self.messages.remove(message)

    def update_no_answered_questions(self, message):
        self.no_answered_questions.append(message)
        logger.info("no_answered_questions: %s" % message.text)
        self.no_answered_questions_ids = self.no_answered_questions_data.read()
        self.no_answered_questions_ids.append([message.message_id, message.text])
        self.no_answered_questions_data.write(self.no_answered_questions_ids)

    def update_answered(self, message):
        self.answered_messages_ids.append(message.message_id)
        self.answered_messages_ids_data.write(self.answered_messages_ids)

    def error_callback(self, bot, update, error):
        logger.debug(update)
        try:
            raise error
        except Unauthorized:
            logger.error("except Unauthorized")
            bot.run()
        # remove update.message.chat_id from conversation list
        except BadRequest:
            logger.error("except BadRequest")
            bot.run()
        except TimedOut:
            logger.error("except TimedOut")
            bot.run()
        # handle slow connection problems
        except NetworkError:
            logger.error("except NetworkError")
            bot.run()
        # handle other connection problems
        except ChatMigrated as e:
            logger.error("except ChatMigrated as e: %s" % e)
            bot.run()
        # the chat_id of a group has changed, use e.new_chat_id instead
        except TelegramError:
            logger.error("except TelegramError")
            bot.run()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
