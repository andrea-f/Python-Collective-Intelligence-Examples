from pydelicious import get_popular, get_userposts, get_urlposts

def initializeUserDict(tag, count=5):
    """Build delicious dataset.

    :param tag:
        Word to use to build dataset by, string.

    :param count:
        Max number of results to retrieve.

    Return dict with most popular users by top posts.
    """
    userDict = {}
    #top 'count' popular posts
    for p1 in get_popular(tag=tag)[0:count]:
        #find users who posted this
        for p2 in get_urlposts(p1['url']):
            user = p2['user']
            userDict[user] = {}
    return userDict

import time

def fillItems(userDict):
    """Populate user dict with 1 or 0 based on if link is shared or not.

    :param userDict:
        Most popular users by top posts, dict.
    """
    allItems = {}
    #find links posted by all users
    for user in userDict:
        for i in range(3):
            try:
                posts = get_userposts(user)
                break
            except:
                print "Fallito user "+user+", riprovo."
                time.sleep(4)
        try:
            for post in posts:
                url = post['url']
                userDict[user][url] = 1.0
                allItems[url] = 1
        except Exception as e:
            print user + " has no posts"
    for ratings in userDict.values():
        for item in allItems:
            if item not in ratings:
                ratings[item] = 0.0


def tagsSimilarity(tag = 'programming'):
    """Builds a dataset of tags and items(links/urls) and then calculates similar tags for one input.

    :param tag:
        Word to use to build dataset by, string.

    Return dict with tags as key and items as values.
    """
    tagsDict = {}
    userDict = initializeUserDict(tag)
    fillItems(userDict)
    for user in userDict:
        for key in user.items():
            tags = get_urlposts(key[0])[0]['tags']
            tagsDict[tags][url] = key[1]
    return tagsDict



