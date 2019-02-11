# -*- coding: utf-8 -*-

print('Iniciando o fcnIAbot...')

# metodos
from amanobot.loop import MessageLoop
from amanobot.exception import TelegramError
from amanobot.namedtuple import InlineKeyboardMarkup

# biblioteca
import datetime
import amanobot
import time
import threading
import aiml
import numexpr
import wolframalpha

# parametros
import config
import credencial

# iniciarlizar instancia bot
bot = amanobot.Bot(config.TOKEN)
bot.deleteWebhook()

k = aiml.Kernel()
k.learn('../aiml/*.aiml')

# credenciais de acesso ao bot e a pesquisa
whitelist = credencial.TURMADM
wolclient = wolframalpha.Client(config.WOLFA)

# retorna qual idioma esta sendo usada
def get_user_lang(language_code):
    if language_code.startswith('pt'):
        return 'Portuguese'
    elif language_code.startswith('en'):
        return 'English'
    elif language_code.startswith('es'):
        return 'Spanish'
    else:
        return 'Indefinida'


def handle_thread(*args):
    t = threading.Thread(target=handle, args=args)
    t.start()


def handle(msg):
    if msg.get('text'):

        if msg['chat']['type'] == 'private':
            msg['message_id'] = None

        # sertifica se tem credencial de interação.
        if msg['chat']['id'] not in whitelist:
            if msg['text'].lower() == '/id':
                bot.sendChatAction(msg['chat']['id'], 'typing')
                time.sleep(1)
                bot.sendMessage(msg['chat']['id'], ''' \
                    Nome: {} \
                    User_ID: {} \
                    Localização: {} \
                    Idioma: {}'''.format(msg['from']['first_name']+('\nSobrenome: '+msg['from']['last_name'] if msg['from'].get('last_name') else ''), msg['from']['id'], msg['from']['language_code'], get_user_lang(msg['from']['language_code'])), reply_to_message_id=msg['message_id'])
            return

        # /start - inicia o boot e lista estatus 
        if msg['text'].lower() == '/start' or msg['text'].lower() == 'começar':
            bot.sendChatAction(msg['chat']['id'], 'typing')
            time.sleep(1)
            start = InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text='🧠 Developer', url='https://blog.cancaonova.com/neviim/')],
                    [dict(text='👤 Instagram', url='https://instagr.am/neviim')],
                    [dict(text='😐 Neviim',  url='https://t.me/neviim')],
                    [dict(text='❤️ FCN',  url='https://fcn.edu.br')]
            ])
            bot.sendMessage(msg['chat']['id'], f'''Olá {msg["from"]["first_name"]}! Prazer em conhecê-lo 😜 Digite oi para começar a conversa comigo 😊''', reply_markup=start, reply_to_message_id=msg['message_id'])

        # /pesquisa no wolframalpha
        elif msg['text'].lower().startswith('/pesquisa '):
            bot.sendChatAction(msg['chat']['id'], 'typing')
            time.sleep(1)
            try:
                res = wolclient.query(msg['text'].replace('/pesquisa ', ''))
                retorno = next(res.results).text

                # cria um log do que foi pesquisado
                # não esta legal acertar isso......
                if len(retorno) < 1:
                    F = open('../log/log_pesquisa.txt','a') 
                    F.write(str(datetime.datetime.now()) +" "+ str(msg['chat']['id']) + " " + msg['text'] + "\n")
                    F.close()
                    # .......

                bot.sendMessage(msg['chat']['id'], f'Resultado: `{retorno}`', 'Markdown', reply_to_message_id=msg['message_id'])
            except TelegramError:
                bot.sendMessage(msg['chat']['id'], 'O resultado desta conta ultrapassa o limite de caracteres que eu posso enviar aqui :(', reply_to_message_id=msg['message_id'])
            except:
                bot.sendMessage(msg['chat']['id'], 'Parece que tem um problema com o item de sua pesquisa 🤔', reply_to_message_id=msg['message_id'])            

        # /eu - Retorna dados pessoais
        elif msg['text'].lower() == '/eu':
            bot.sendChatAction(msg['chat']['id'], 'typing')
            time.sleep(1)
            bot.sendMessage(msg['chat']['id'], ''' \
                Nome: {} \
                User_ID: {} \
                Localização: {} \
                Idioma: {}'''.format(msg['from']['first_name']+('\nSobrenome: '+msg['from']['last_name'] if msg['from'].get('last_name') else ''), msg['from']['id'], msg['from']['language_code'], get_user_lang(msg['from']['language_code'])), reply_to_message_id=msg['message_id'])

        # /hora - Retorna a hora atual 
        elif msg['text'].lower() == '/hora':
            bot.sendChatAction(msg['chat']['id'], 'typing')
            time.sleep(1)
            now = datetime.datetime.now()
            bot.sendMessage(msg['chat']['id'], f'Agora são: {now.strftime("%X")}', reply_to_message_id=msg['message_id'])

        # /data - Retorna a data atual 
        elif msg['text'].lower() == '/data':
            bot.sendChatAction(msg['chat']['id'], 'typing')
            time.sleep(1)
            now = datetime.date.today()
            bot.sendMessage(msg['chat']['id'], f'Hoje é dia: {now.strftime("%d/%m/%Y")}', reply_to_message_id=msg['message_id'])

        # /calcule - ((2*4)/3)
        elif msg['text'].lower().startswith('/calcule '):
            bot.sendChatAction(msg['chat']['id'], 'typing')
            time.sleep(1)
            try:
                exp = numexpr.evaluate(msg['text'].replace('/calcule ', ''))
                bot.sendMessage(msg['chat']['id'], f'Resultado: `{exp}`', 'Markdown', reply_to_message_id=msg['message_id'])
            except TelegramError:
                bot.sendMessage(msg['chat']['id'], 'O resultado desta conta ultrapassa o limite de caracteres que eu posso enviar aqui :(', reply_to_message_id=msg['message_id'])
            except:
                bot.sendMessage(msg['chat']['id'], 'Parece que tem um problema com a sua expressão matemática 🤔', reply_to_message_id=msg['message_id'])

        # Busca nas base .aiml de conhecimento 
        else:
            if msg['chat']['type'] == 'private' or msg.get('reply_to_message', dict()).get('from', dict()).get('id', dict()) == int(config.token.split(':')[0]):
                response = k.respond(msg['text'])
                if response:
                    response = response.replace('#', '\n').replace('$nome', msg['from']['first_name'])
                    bot.sendChatAction(msg['chat']['id'], 'typing')
                    time.sleep(1)
                    bot.sendMessage(msg['chat']['id'], response, reply_to_message_id=msg['message_id'], disable_web_page_preview=True)

                    # cria um log do que foi pesquisado
                    # não esta legal acertar isso......
                    if len([x for x in credencial.GRAVALOG if x == response]) == 0:
                        F = open('../log/log_nao_encontrado.txt','a') 
                        F.write(str(datetime.datetime.now()) +" "+ str(msg['chat']['id']) +" "+ msg['text'] + "\n")
                        F.close()
                        # .......
                    #print(len(credencial.GRAVALOG[0]))
                    #print(len(response)) 

MessageLoop(bot, handle_thread).run_as_thread()

print('Bot iniciado!')

while True:
    time.sleep(10)