swear = ['fuck','shit','nigger','nikker','kanker','cancer','kut','klere','kolere','cholera','tering','typhus', 'tyfus','pussy','ass','butt','dick','wtf','snikkel','master race','cock','piemel','pik','cunt','neger','thijs konst']
blacklist = [realDonaldTrump,]

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
    name = tweet['name']
    if (filter in text or filter in name):
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
    
def blacklist_add(user):
    global blacklist
    if user in blacklist:
        return(user, ' is already part of the blacklist')
    else:
        blacklist.append(user)
        return(user, ' is added to the blacklist')
        
def blacklist_remove(user):
    global blacklist
    if user in blacklist:
        blacklist.remove(user)
        return(user, ' is removed from the blacklist')
    else:
        return(user, ' is not in the blacklist')

def swear_add(word):
    global swear
    if word in swear:
        return(word, ' is already in list of cursewords')
    else:
        swear.append(word)
        return(word, ' is added to list of cursewords')

def swear_remove(word):
    global swear
    if word in swear:
        swear.remove(word)
        return(word, ' is removed from list of cursewords')
    else:
        return(word, ' is not in list of cursewords')
