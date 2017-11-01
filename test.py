from eca import *
from eca.generators import start_offline_tweets

@event('init')
def setup(c, e):
    # start the offline tweet stream
    start_offline_tweets('data/batatweets.txt', time_factor=100000)

@event('tweet')
def echo(c, e):
    emit('tweet', e.data)