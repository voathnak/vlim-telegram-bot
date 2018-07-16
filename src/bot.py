import time
from ai import AI
from vlim_telegram import VLIMTelegram
from datetime import date, datetime

from telegram.ext import dispatcher


from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)



# class self():


class Bot:

    def __init__(self):
        self.last_display = ''
        self.last_answered = ''
        self.startup_time = datetime.now()
        self.answered_message = []
        self.answered_question = []
        self.ai = AI(self.startup_time)
        self.vlim_telegram = VLIMTelegram()

    def do_something(self):
        with open("/tmp/current_time.txt", "w") as f:
            f.write("The time is now " + time.ctime())

    def run(self):
        while True:
            time.sleep(2)
            print "current time: %s" % time.ctime()
            # getUpdates()
            self.action()

    def action(self):
        updates = self.vlim_telegram.getUpdates()
        print "type of updates: %s" % type(updates)
        print updates
        if len(updates) > 0:
            print "update length %s" % len(updates)
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
                print "[action] last update: %s: %s" % (last_update.message.from_user.username, text)
                self.last_display = text

            # if self.last_answered != text:
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


    def error_callback(bot, update, error):
        try:
            raise error
        except Unauthorized:
            print "except Unauthorized"
        # remove update.message.chat_id from conversation list
        except BadRequest:
            print "except BadRequest"
        # handle malformed requests - read more below!
        except TimedOut:
            print "except TimedOut"
        # handle slow connection problems
        except NetworkError:
            print "except NetworkError"
        # handle other connection problems
        except ChatMigrated as e:
            print "except ChatMigrated as e"
        # the chat_id of a group has changed, use e.new_chat_id instead
        except TelegramError:
            print "except TelegramError"



# handle all other telegram related errors

# dispatcher.add_error_handler(error_callback)

if __name__ == "__main__":
    print "__name__: %s" % __name__
    bot = Bot()
    bot.run()