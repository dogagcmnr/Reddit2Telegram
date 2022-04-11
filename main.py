import praw, credientials, telepot, time, os, urllib3, random, emoji
reddit = praw.Reddit(client_id=credientials.clid,client_secret=credientials.csec,user_agent=credientials.uag)
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

telepot.api.set_proxy('http://proxy.server:3128') # for pythonanywhere
#telepot.api._pools = {
#    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30)
#}
#telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(credientials.bot)

def Redditto(sub):
    hot_posts = reddit.subreddit(sub).hot(limit=10)
    return hot_posts

def Reddittro(sub):
    random_post = reddit.subreddit(sub).random()
    return random_post

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    chat_id = msg['chat']['id']
    command = msg.get('text', '')
    print('{} wrote {}.'.format(str(chat_id),str(command)))
    userjson = bot.getChat(chat_id)
    dictlist = []
    for key, value in userjson.items():
        temp = [key, value]
        dictlist.append(temp)
    if content_type == 'text':
        f = open("log.txt","a")
        f.write('{0} -- {1}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M")," Chat ID : {} -- Username : {} -- Message : {}".format(str(chat_id),str(dictlist[2][1]),str(command))))
        subname="MachineLearning"
        main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')],[KeyboardButton(text=subname)]])
        if command == '/start':
            bot.sendMessage(chat_id, "Welcome.", reply_markup=main_menu, parse_mode="Markdown")
        elif "/ch" in command:
            subname=command[4:]
            main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')],[KeyboardButton(text=subname)]])
            bot.sendMessage(chat_id,"Sub is set.", reply_markup=main_menu, parse_mode="Markdown")
        else:
            try:
                #hot_posts=Redditto(command) -- this method for Redditto function with 10 hot posts
                #for post in hot_posts:
                #    bot.sendPhoto(chat_id, post.url)
                #    bot.sendMessage(chat_id,"Title: " + post.title + " Score: " + str(post.score) + " Comments: " + str(post.num_comments))
                #i=0
                #for i in range(5):
                #    i+=1
                rpost=Reddittro(command)
                bot.sendPhoto(chat_id, rpost.url)
                bot.sendMessage(chat_id,"Title: " + rpost.title + " Score: " + str(rpost.score) + " Comments: " + str(rpost.num_comments))

            except:
                pass

MessageLoop(bot, handle).run_forever()
