# -*- coding: utf-8 -*-
import linecache
import re
import subprocess
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import time
import logging

from pony.orm import *
# from csv_data import CSVData
from telegram.error import NetworkError
from google_translate import GoogleTranslate
from models.vxdb import VXUser
from models.vxmessage import VXMessage
from nginx_config import NGINXConfig
from vlim_telegram import VLIMTelegram

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
log_path = 'logs'

subprocess.call("mkdir -p %s" % log_path, shell=True)

LOG_FILE = "%s/vlim-bot.log" % log_path


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


# print logger.handlers
# Todo: what can i say?
# Todo: what can i do?
# Todo: currency exchage
# Todo:
# Todo: make a release version
# Todo: make an install script run successfully
# Todo: possibly answer
# Todo:
# Todo:


class VLIMBot:

    def __init__(self):
        self.last_display = ''
        self.last_updated_message = {}
        self.last_updated_message_id = 0
        self.last_updated_id = 0
        self.startup_time = datetime.now()
        self.answered_message = []
        self.answered_messages = []
        self.answered_messages_ids = []
        self.answered_question = []
        self.question = []
        self.vlim_telegram = VLIMTelegram()
        self.no_answered_questions = []
        # self.no_answered_questions_data = CSVData('no_answered_messages')
        # self.no_answered_questions_ids = self.no_answered_questions_data.read_ids()
        # self.no_answered_questions_data_ids = self.no_answered_questions_data.read()
        self.updates = self.vlim_telegram.getUpdates()
        # self.answered_messages_ids_data = CSVData('answered_messages_ids')
        # self.answered_messages_ids = self.answered_messages_ids_data.read_ids()
        self.messages = []
        self.google_translate = GoogleTranslate()
        self.nginx_config = NGINXConfig()
        self.silence = False

        updates = self.vlim_telegram.getUpdates(offset=-100, limit=100)

        if len(updates) > 0:
            self.last_updated_id = updates[-1].update_id
        else:
            self.last_updated_id = 0

        read_updates = list(filter(
            lambda x: x.message and x.message.message_id and x.message.date and x.message.text and x.message.from_user,
            updates))

        logger.info("Updating existing users into database...")
        self.update_user_database(read_updates)
        logger.info("Updating existing messages into database...")
        self.update_message_database(read_updates, read=True)

    def print_exception(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    def run(self):
        while True:
            time.sleep(1)
            try:
                self.action()

            except NetworkError as ne:
                logger.warning(ne)

            except OperationalError as oe:
                logger.info(oe)

            except KeyboardInterrupt:

                logger.info("You have stopped the programm.")

            except Exception as ec:
                self.print_exception()
                logger.error(ec)

    @db_session
    def update_message_database(self, updates, **kwargs):
        messages = set(map(lambda x: x.message, updates))

        for tg_message in messages:
            message = VXMessage.get(message_id=tg_message.message_id)

            if message is None and tg_message.text:
                user = VXUser.get(telegram_user_id=tg_message.from_user.id)
                message = VXMessage(message_id=tg_message.message_id, date=tg_message.date,
                                    text=tg_message.text, chat_id=tg_message.chat_id,
                                    user_id=user)

            if "read" in kwargs and kwargs["read"] is True:
                message.read = True
        logger.info("Done update_message_database.")
        commit()

    @db_session
    def update_user_database(self, updates):
        tg_users = set(map(lambda x: x.message.from_user,
                           list(filter(lambda x: x.message is not None and x.message.from_user is not None, updates))))
        for tg_user in tg_users:
            user = VXUser.get(telegram_user_id=tg_user.id)
            if user is None:
                user = VXUser(telegram_user_id=tg_user.id, first_name=tg_user.first_name, last_name=tg_user.last_name,
                              name=tg_user.name, full_name=tg_user.full_name,
                              honorific_address='Sir')
                logger.info("Added User: %s" % user.first_name)
        logger.info("Done update_user_database.")
        commit()

    @db_session
    def action(self):

        def validate_update(update):
            if \
                    update.update_id > self.last_updated_id and \
                    update.message and update.message.message_id and \
                    update.message.text and \
                    update.message.message_id > self.last_updated_message_id:
                return True

            else:
                return False

        updates = self.vlim_telegram.getUpdates(offset=-100, limit=100)
        new_updates = list(filter(lambda x: validate_update(x), updates))

        update_messages = list(map(lambda y: y.message, new_updates))
        if len(update_messages):
            self.update_user_database(new_updates)
            self.update_message_database(new_updates)
            self.last_updated_id = new_updates[-1].update_id

            for update_message in update_messages:
                text = update_message.text
                user = VXUser.get(telegram_user_id=update_message.from_user.id)
                message = VXMessage.get(message_id=update_message.message_id)
                if message is None:
                    message = VXMessage(message_id=update_message.message_id, date=update_message.date,
                                        text=update_message.text, chat_id=update_message.chat_id,
                                        user_id=user)

                if not message.read:

                    logger.info(
                        ">>>>> last_updated_message: %s: %s: %s, %s" % (
                            message.date, "%s %s (%s)" % (user.first_name, user.last_name, message.chat_id),
                            message.message_id, message.text))

                    greating1 = ['hey', 'hi']
                    greating2 = ['Hello', 'Hola']
                    greating3 = ['How are you', 'How are you doing', 'How have you been']

                    honorific_address_man = [
                        "I am a man",
                        "I'm a man",
                        "I am a boy",
                        "I'm a boy",
                        "I am not a woman",
                        "I'm not a woman",
                        "I am not a girl",
                        "I'm not a girl",
                    ]

                    honorific_address_woman = [
                        "I am a woman",
                        "I'm a woman",
                        "I am a girl",
                        "I'm a girl",
                        "I am not a man",
                        "I'm not a man",
                        "I am not a boy",
                        "I'm not a boy",
                        "I'm a lady",
                        "I am a lady"
                    ]

                    # ^(\/\.([a-z]|[A-Z])+\s.*)|(\.([a-z]|[A-Z])+\s.*)$
                    command_pattern = '(\/\.([a-z]|[A-Z])+\s)|(\.([a-z]|[A-Z])+\s)'
                    matched = re.match(command_pattern, text)

                    # Command
                    if matched:
                        logger.debug("matched: %s" % matched.group())
                        command = matched.group()[1:-1]
                        command = re.sub('\.', "", command)
                        searched = re.search('%s.*' % command_pattern, text).group()
                        logger.debug("searched: %s" % searched)
                        context = re.sub(command_pattern, "", text)
                        logger.debug("sub: %s" % context)

                        # GoogleTranslate Command
                        if command == 't' and len(context.split(',')) > 1:
                            target_lang = context.split(',')[0]
                            translate_text = context.split(',')[1]
                            translated_text = self.google_translate.translate(target_lang, translate_text)
                            self.vlim_telegram.send(message.chat_id, translated_text)

                        elif command == 'dpoint' and len(context.split('to')) > 1:
                            server_name = context.split('to')[0]
                            proxy_pass = context.split('to')[1]
                            self.nginx_config.create(server_name, proxy_pass, server_name)
                            # print "%s -->> %s" % (source, target)
                            pass

                        elif command == 'silence' and len(context) == 1:
                            if context == "1":
                                self.silence = True
                            elif context == "0":
                                self.silence = False
                            self.vlim_telegram.send(message.chat_id,
                                                    "Roger that, %s." % user.honorific_address)

                        else:
                            message.state = "no_answer"
                    elif not self.silence:
                        # Greating
                        if any(x.lower() in text.lower() for x in greating1):
                            self.vlim_telegram.send(message.chat_id, "Hello, %s." % user.first_name)

                        elif any(x.lower() in text.lower() for x in greating2):
                            self.vlim_telegram.send(message.chat_id,
                                                    "Hello, %s." % user.honorific_address)

                        elif any(x.lower() in text.lower() for x in greating3):
                            self.vlim_telegram.send(message.chat_id,
                                                    "I am fine, %s." % user.honorific_address)
                            self.vlim_telegram.send(message.chat_id,
                                                    "Thank You, %s." % user.honorific_address)

                        elif any(x.lower() in text.lower() for x in honorific_address_man):
                            user.honorific_address = "Sir"
                            self.vlim_telegram.send(message.chat_id,
                                                    "Okay, %s." % user.honorific_address)
                            self.vlim_telegram.send(message.chat_id, "Thank You for Letting me know.")

                        elif any(x.lower() in text.lower() for x in honorific_address_woman):
                            user.honorific_address = "Madam"
                            self.vlim_telegram.send(message.chat_id,
                                                    "Okay, %s." % user.honorific_address)
                            self.vlim_telegram.send(message.chat_id, "Thank You for Letting me know.")

                        else:
                            message.state = "no_answer"
                            self.vlim_telegram.send(message.chat_id, "I do not know about <<%s>>, %s." % (
                                message.text, user.honorific_address))
                            self.vlim_telegram.send(message.chat_id, "But I will ask my creator.")

                    self.last_updated_message_id = message.message_id
                    message.read = True


if __name__ == "__main__":
    try:
        vlim_bot = VLIMBot()
        vlim_bot.run()
    except Exception as e:
        logger.error(e)
