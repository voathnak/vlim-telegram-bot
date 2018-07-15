from vlim_telegram_update import getUpdates
from vlim_telegram_send import VLTelegram

class AI:

    def __init__(self, startup_time):
        self.startup_time = startup_time

    def action(self):
        updates = getUpdates()
        print "type of updates: %s" % type(updates)
        print updates
        if len(updates)>0:
            print "update length %s" % len(updates)
            # print updates()[len(updates()) - 1]

            last_update = updates[-1]
            last_message_date = last_update.message.date
            # print "last_message_date: %s" % last_message_date
            # print "last_message_date type: %s" % type(last_message_date)
            # print "startup_time: %s" % self.startup_time
            # print "startup_time type: %s" % type(self.startup_time)

            text = last_update.message.text
            # print "[action] last update: %s" % last_update
            if last_message_date > self.startup_time and text not in self.answered_question:
            # if self.last_display != text:
                print "[action] last update: %s: %s" % (last_update.message.from_user.username, text)
                self.last_display = text

            # if self.last_answered != text:
            if last_message_date > self.startup_time and text not in self.answered_question:

                # Greating
                greating = ['hey', 'hi', 'Hello','Hola']
                if any(x.lower() in text.lower() for x in greating):
                    VLTelegram.send(self, "Hello Sir")
                    self.answered_question.append(text)
                #
                greating2 = ['How are you', 'How are you doing', 'How have you been']
                if any(x.lower() in text.lower() for x in greating2):
                    VLTelegram.send(self, "I am fine, Sir.")
                    VLTelegram.send(self, "Thank You.")
                    self.answered_question.append(text)

                self.last_answered = text

