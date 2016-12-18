# -*- coding: utf-8 -*-
from datetime import datetime
import pprint
import re
import sys

import telepot
import pickle


REGEX_HORA = re.compile(r'^/hora(@claudinhorabot)?$')
REGEX_NOMBRE = re.compile(r'^/claudin(@claudinhorabot)?$')
REGEX_PREGUNTA = re.compile(r'^[¿]?qu[eé] hora es\?$')

def handle(msg):
    global reply
    content_type, _, chat_id  = telepot.glance(msg)
    if content_type == 'text':

        message = msg.get('text', '').lower()

        if REGEX_HORA.match(message) is not None and chat_id == -112413533:
            bot.sendMessage(
                chat_id=chat_id,
                text=datetime.fromtimestamp(msg['date']).strftime('%H:%M:%S'),
                reply_to_message_id=reply
            )
        elif REGEX_NOMBRE.match(message) is not None:
            bot.sendSticker(
                chat_id=chat_id,
                sticker='BQADAQADcgADi8feAtZGtWNnOb_GAg'
            )
        elif REGEX_PREGUNTA.match(message) is not None:
            bot.sendMessage(
                chat_id=chat_id,
                text=datetime.fromtimestamp(msg['date']).strftime('%H:%M:%S'),
                reply_to_message_id=msg['message_id']
            )
            if chat_id == -112413533:
                reply = msg['message_id']
                pickle.dump(reply,  open( "reply.p", "wb" ))

bot = telepot.Bot(sys.argv[1])
print ('Listening ...')
try:
	reply = pickle.load(open( "reply.p", "rb" ))
except (OSError, IOError) as e:
	reply = -1;
        pickle.dump(reply,  open( "reply.p", "wb" ))
bot.message_loop(callback=handle, run_forever=True)
