from sort import merge_pairs
from eca import *
import json
import eca.http

from eca.generators import start_offline_tweets
import datetime
import textwrap

root_content_path = 'test_static'

@event('init')
def setup(ctx, e):
    # start the offline tweet stream
    start_offline_tweets('data/batatweets.txt', time_factor=100000, event_name='tweet')
    ctx.filterword = None

@event('tweet')
def echo(ctx, e):
    tweet = e.data
    if ctx.filterword != None and tweet_filter(tweet, ctx.filterword):
        print(ctx.filterword)
        emit ('tweet', e.data)
    elif ctx.filterword == None:
        emit ('tweet', e.data)
    
@event('word')
def set_filter(ctx, e):
    ctx.filterword = e.data['word']
    print (ctx.filterword)

@event('tweet')
def tweet(ctx, e):
    # we receive a tweet
    tweet = e.data

    # parse date
    time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

    # nicify text
    text = textwrap.fill(tweet['text'], initial_indent='    ', subsequent_indent='    ')
    uranking = adjustranking(text.lower())

    # generate output
    output = "[{}] {} (@{}):\n{}".format(time, tweet['user']['name'], tweet['user']['screen_name'], text)
    emit('ranking', {
        'text': uranking
    });


ulist = ["tilburg", "erasmus", "radboud", "rijksuniversiteit groningen", "tu delft", "tu eindhoven", "leiden", "maastricht", "utwente", "utrecht", "universiteit van amsterdam", "vrije universiteit", "boeren"]
uwords = [["tilburg", "kub"], ["erasmus", "rotterdam", "eur"], ["radboud", "nijmegen", "ru"], ["rijksuniversiteit", "groningen", "rug"], ["tudelft", "delft", "tu delft"], ["eindhoven", "tue"], ["leiden", "ul"], ["maastricht", "um"], ["utwente", "enschede", "ut"], ["utrecht", "uu"], ["universiteit van amsterdam", "amsterdam", "uva"], ["vrije universiteit", "amsterdam", "vu"], ["wageningen", "wu"]]

ranking = [0 for x in range(len(ulist))]

def add_request_handlers(httpd):
    httpd.add_route('/api/word', eca.http.GenerateEvent('word'), methods=['POST'])
    
def newranking(uid):
    global ranking
    ranking[uid] += 1


def uwordsearch(uid, text): #returns 1 if a word from the u
    global uwords
    i = 0
    while i < len(uwords[uid]):
        iout = True
        if text.find(uwords[uid][i]) >= 0:
            if text.find(uwords[uid][i]) > 0:
                if str.isalpha(text[text.find(uwords[uid][i])-1]):
                    iout = False
            if text.find(uwords[uid][i])+len(uwords[uid][i]) < len(text):
                if str.isalpha(text[text.find(uwords[uid][i])+len(uwords[uid][i])]):
                    iout = False
            if iout:
                return 1
        i += 1
    return 0

#(not str.isalpha(text[text.find(uwords[uid][i])-1]) or not str.isalpha(text[text.find(uwords[uid][i])+len(uwords[uid][i])]))

def adjustranking(text): #adjusts current ranking
    global ranking
    rankingtemp = [ranking[i] + uwordsearch(i, text) for i in range(len(ulist))]
    if ranking != rankingtemp:
        ranking = rankingtemp
    ranking = rankingtemp
    return orderedranking()


def orderedranking():
    rank = merge_pairs([(ranking[i], ulist[i]) for i in range(len(ulist))])
    rank.reverse()
    return rank
    
swear = ['fuck','shit','nigger','nikker','kanker','cancer','kut','klere','kolere','cholera','tering','typhus', 'tyfus','pussy','butt','dick','wtf','snikkel','master race','cock','piemel','pik','cunt','neger','thijs konst']
blacklist = ['realDonaldTrump']

def tweet_clean(tweet):
    i = 0
    text = tweet['text']
    cleantext = text
    while i < len(swear):
        cleantext = cleantext.replace(swear[i],'bobba')
        i+=1
    tweet['text'] = cleantext
    return tweet

def tweet_filter(tweet, filter):
    text = tweet['text']
    if (filter in text):
        greenlight = True
    else:
        greenlight = False
    return greenlight

def batacheck(tweet):
    user = tweet['user']
    if user == '"'+batavierenrace+'"':
        batalight = True
    else:
        batalight = False
    return batalight
    
def blacklist_check(tweet):
    i = 0
    user = tweet['user']
    while i < len(blacklist):
        blocked = '"'+blacklist[0]+'"'
        if user == blocked:
            blacklight = False
            return blacklight
        else:
            i+=1
    blacklight = True
    return blacklight