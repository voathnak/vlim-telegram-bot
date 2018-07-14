import time

from datetime import date, datetime

from telegram.ext import dispatcher

from ai import action
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)



class self():
    last_display = ''
    last_answered = ''
    startup_time = datetime.now()
    answered_message = []
    answered_question = []

def do_something():
    with open("/tmp/current_time.txt", "w") as f:
        f.write("The time is now " + time.ctime())

def run():
    while True:
        time.sleep(2)
        print "current time: %s" % time.ctime()
        # getUpdates()
        action(self)

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
    run()