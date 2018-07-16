# -*- coding: utf-8 -*-

import sys
import time
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
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


logger = get_logger("VLIM Bot")

logger.info("Log Level INFO")
print logger.handlers


class Bot:

    def __init__(self):
        self.last_display = ''
        self.last_answered = ''
        self.startup_time = datetime.now()
        self.answered_message = []
        self.answered_question = []
        self.vlim_telegram = VLIMTelegram()

    def do_something(self):
        with open("/tmp/current_time.txt", "w") as f:
            f.write("The time is now " + time.ctime())

    def run(self):
        while True:
            time.sleep(2)
            # logger.info("## current time: %s" % time.ctime())
            # print "current time: %s" % time.ctime()
            # getUpdates()
            self.action()

    def action(self):
        updates = self.vlim_telegram.getUpdates()
        # print "type of updates: %s" % type(updates)
        # print updates
        if len(updates) > 0:
            # logger.info("## update length %s" % len(updates))
            # print updates()[len(updates()) - 1]

            last_update = updates[-1]
            last_message_date = last_update.message.date
            # print "last_message_date: %s" % last_message_date
            # print "last_message_date type: %s" % type(last_message_date)
            # print "startup_time: %s" % self.startup_time
            # print "startup_time type: %s" % type(self.startup_time)

            text = last_update.message.text
            chat_id = last_update.message.chat.id
            # print "[action] last update: %s" % last_update
            if last_message_date > self.startup_time and text not in self.answered_question:
                # if self.last_display != text:
                # print "[action] last update: %s: %s" % (last_update.message.from_user.username, text)
                logger.info("last update: %s: %s" % (last_update.message.from_user.username, text))
                self.last_display = text

            # if self.last_answered != text:
            logger.info("Answered_question: %s", self.answered_question)
            if last_message_date > self.startup_time and text not in self.answered_question:

                # Greating
                greating = ['hey', 'hi', 'Hello', 'Hola']
                if any(x.lower() in text.lower() for x in greating):
                    self.vlim_telegram.send(chat_id, "Hello Sir")
                    self.answered_question.append(text)
                #
                greating2 = ['How are you', 'How are you doing', 'How have you been']
                if any(x.lower() in text.lower() for x in greating2):
                    self.vlim_telegram.send(chat_id, "I am fine, Sir.")
                    self.vlim_telegram.send(chat_id, "Thank You.")
                    self.answered_question.append(text)

                self.last_answered = text

    def error_callback(self, bot, update, error):
        logger.debug(update)
        try:
            raise error
        except Unauthorized:
            logger.info("except Unauthorized")
            bot.run()
        # remove update.message.chat_id from conversation list
        except BadRequest:
            logger.info("except BadRequest")
            bot.run()
        except TimedOut:
            logger.info("except TimedOut")
            bot.run()
        # handle slow connection problems
        except NetworkError:
            logger.info("except NetworkError")
            bot.run()
        # handle other connection problems
        except ChatMigrated as e:
            logger.info("except ChatMigrated as e: %s" % e)
            bot.run()
        # the chat_id of a group has changed, use e.new_chat_id instead
        except TelegramError:
            logger.info("except TelegramError")
            bot.run()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
