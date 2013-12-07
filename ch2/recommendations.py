#A dictionary of movie critics and their ratings of a small set of movies.

critics = {
'Lisa Rose': {
'Lady in the water': 2.5,
'Snakes on a plane': 3.5,
'Just my luck': 3.0,
'Superman returns': 3.5,
'You, me and dupree': 2.5,
'The night listener': 3.0
},
'Gene Seymour': {
'Lady in the water': 3.0,
'Snakes on a plane': 3.5,
'Just my luck': 1.5,
'Superman returns': 5.0,
'The night listener': 3.0,
'You, me and dupree': 3.5
},
'Michael Phillips': {
'Lady in the water': 2.5,
'Snakes on a plane': 3.0,
'Just my luck': 1.5,
'Superman returns': 3.5,
'The night listener': 4.0
},
'Claudia Puig': {
'Snakes on a plane': 3.5,
'Just my luck': 3.0,
'Superman returns': 4.0,
'You, me and dupree': 2.5,
'The night listener': 4.5
},
'Mick LaSalle': {
'Lady in the water': 3.0,
'Snakes on a plane': 4.0,
'Just my luck': 2.0,
'Superman returns': 3.0,
'You, me and dupree': 2.0,
'The night listener': 3.0
},
'Jack Matthews': {
'Lady in the water': 3.0,
'Snakes on a plane': 4.0,
'Superman returns': 5.0,
'You, me and dupree': 3.5,
'The night listener': 3.0
},
'Toby': {
'Snakes on a plane': 4.5,
'Superman returns': 4.0,
'You, me and dupree': 1.0,
}}

topics = {
'Argenti': {
'Sci-fi': 1,
'Action': 1,
'Grotesque': 0,
'Horror': 0,
'Erotic': 1,
'War': 0,
'Gay': 0,
'Drama': 0,
'Crime': 0,
'Classics': 0,
'Thriller': 1
},
'Trulli': {
'Sci-fi': 1,
'Action': 1,
'Grotesque': 0,
'Horror': 0,
'Erotic': 0,
'War': 1,
'Gay': 0,
'Drama': 0,
'Crime': 1,
'Classics': 0,
'Thriller': 0,
'Historic': 0
},
'Cazzaniga': {
'Sci-fi': 0,
'Grotesque': 1,
'Horror': 1,
'Erotic': 0,
'War': 0,
'Gay': 1,
'Crime': 0,
'Classics': 0,
'Thriller': 0,
'Porn':1,
'Historic': 1
},
'Albini': {
'Sci-fi': 1,
'Action': 1,
'Grotesque': 0,
'Horror': 1,
'War': 1,
'Gay': 1,
'Drama': 0,
'Crime': 1,
'Classics': 0,
'Thriller': 0,
'Porn': 1,
'Historic': 1
}
}

from math import sqrt

def euclideanDistance(prefs, person1, person2):
    """Take common items people have rated in critics.
    Calculate distance between two people tastes by
    taking the difference between two movies on x,y axis, squaring them and then
    add them together. To get a % value 1/result.
    This is the Euclidean distance score.

    :param prefs:
        Holds in key person name and in value subkey movie name and in subvalue rating information, dict.
    :param person1:
        Rating of first movie for second person, int.
    :param person2:
        Rating of second movie by first person, int.

    Return int with similarity score.
    """

    #List of shared items
    sharedItems = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            sharedItems[item] = 1 #random value could be anything!
    if len(sharedItems) == 0: return 0
    #Add up squares of all differences:
    sumOfSquares = sum([pow(prefs[person1][item] - prefs[person2][item],2) for item in sharedItems])
    return 1/(1+sqrt(sumOfSquares))


def pearsonCorrelation(prefs, p1, p2):
    """Calculates Pearson correlation  between two people.
    Corrects not normalized data.
    1. Find items rated by both critics.
    2. Calculate sum of ratings for both people.
    3. Sum the ratings squared.
    4. Sum product of ratings.

    :param prefs:
        Holds in key person name and in value subkey movie name and in subvalue rating information, dict.
    :param person1:
        Rating of first movie for second person, int.
    :param person2:
        Rating of second movie by first person, int.

    Return int with Pearson correlation score.
    """
    sharedItems = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            sharedItems[item] = 1
    totalCommonElements = len(sharedItems)
    if totalCommonElements == 0: return 0
    #Calculate sum of ratings for both people:
    sum1 = sum([prefs[p1][it] for it in sharedItems])
    sum2 = sum([prefs[p2][it] for it in sharedItems])
    #Calculate sum of the ratings squared
    sum1Sq = sum([pow(prefs[p1][it],2) for it in sharedItems])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in sharedItems])
    #Sum product of ratings
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in sharedItems])
    #Calculate Pearson score, how much the variables change together divided by the product of how much they vary individually.
    num = pSum - (sum1 * sum2/totalCommonElements)
    den = sqrt((sum1Sq - pow(sum1, 2)/totalCommonElements) * (sum2Sq - pow(sum2, 2)/totalCommonElements))
    if den == 0: return 0
    return num/den

def topMatches(prefs, person, n=5, similarity = pearsonCorrelation):
    """Compares all critics in prefs with person specified, returns list of most related people descending.

    :param prefs:
        Holds in key person name and in value subkey movie name and in subvalue rating information, dict.

    :param person:
        Name to compare other critics to, string.

    :param n:
        Number of items in list to return, int.

    :param similarity:
        Which similarity function to use when comparing items in prefs, function.

    Return list with most similar items, descending, highest at the top.
    """
    #similarity passes the input params to the function specified in similarity
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendations(prefs, person, similarity = pearsonCorrelation):
    """Computes list of videos I am most likely to watch.
    Based on my affinity to other critics and their score on a particular movie.
    Divided by the sum of all similarities.

    :param prefs:
        Holds in key person name and in value subkey movie name and in subvalue rating information, dict.

    :param person:
        Name to compare other critics to, string.

    :param similarity:
        Which similarity function to use when comparing items in prefs, function.

    Return list of videos I am most likely to enjoy.
    """
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person: continue #dont compare me to myself
        sim = similarity(prefs, person, other)
        if sim<=0: continue #if similarity score is zero or lower
        for item in prefs[other]:
            #only compare movies I haven't seen
            if item not in prefs[person] or prefs [person][item]==0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim #<- similarity of me to critics * vote given by other person to specific item
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(total/simSums[item],item) for item, total in totals.items()] #normalized list of tuples of similarity to me, video name
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    """Swap names with items to get a list of most similar items to a specific item.
    Same procedure as most similar critics compared to a specific critic.

    :param prefs:
        Holds in key person name and in value subkey movie name and in subvalue rating information, dict.

    Return dict with transposed items and names.
    """
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {}) #creates dict with item as key and dict as value.
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n=10):
    """Creates a dict of items with associated most similar items to one being considered.
    Item based collaborative filtering.

    :param prefs:
        Holds in key person name and in value subkey movie name and in subvalue rating information, dict.

    :param n:
        Number of items in list to return, int.

    Return dict with item in key and most similar items in value.
    """
    result = {}
    #invert preference matrix to put item in key.
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        #large datasets
        c+=1
        if c%100==0: print "%d / %d" % (c, len(itemPrefs))
        #find most similar item to one being considered.
        scores = topMatches(itemPrefs, item, n=n, similarity = pearsonCorrelation)
        result[item] = scores
    return result

def getRecommendedItems(prefs, itemMatch, user):
    """Generate list of recommended items based on user preferences.
    Get rating for a movie.
    Multiply this rating with similarity score of this movie with another I have not watched.
    Repeat this process for all movies related to first movie I have not watched.
    Sum similarity scores for movies I have watched with movie I have not watched.
    Sum products of multiplication between (similarity score for each movie I have watched with movie I have not watched) and my rating.
    Divide total sum of multiplication by total of similarity scores for movies I have watched with movie I have not watched. Pag24

    :param prefs:
        Holds in key person name and in value subkey movie name and in subvalue rating information, dict.

    :param itemMatch:
        Item name with related items by descending order, dict.

    :param user:
        Name of user to generate recommendations for, string.

    Return list with tuples with likelyhood of enjoying an item and item name.
    """
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        #Loop over items similar to this one.
        for (similarity, item2) in itemMatch[item]:
            #Ignore item if user has already rated this item
            if item2 in userRatings: continue
            #Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating #item2 is item not already rated.
            #Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    #Divide total score of similarity*rating by total weight of similarities to get an average
    rankings = [(score/totalSim[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def loadMovieLens(path='/home/legionovainvicta/app/collective/ch2/data/movielens'):
    """Uses MovieLens.org database to generate recommendations for similar movies taking one user into account.

    :param path:
        Location of dataset, string.

    Return dict with user info and rated movies.
    """
    movies = {}
    for line in open(path+'/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
    #load data
    prefs = {}
    for line in open(path+'/u.data'):
        (user, movieid,rating,ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs

def tanimotoScore(prefs, refTopic, otherTopic ):
    """Calculates tanimoto score for reference input.

    :param prefs:
        Input dict. Holds in key person name and in value subkey movie name and in subvalue rating information, dict.

    :param refTopic:
        Original topic to compare similar topics to based on wether people follow that topic or not, string.

    :param otherTopic:
        Other topic to compare similarity with reference topic, string.

    Return int with tanimoto score.
    """
    a = b = c = 0
    from pprint import pprint
    #Prefs needs to be normalized to account for missing topics in each user data.
    allTopics = []
    for person in prefs.values():
        for topic in person:
            if topic not in allTopics:
                allTopics.append(topic)
    #Make sure matrices all are the same.
    for t in allTopics:
        for person in prefs:
            topicsByPerson = [key for key in prefs[person]]
            if t not in topicsByPerson:
                prefs[person][t] = 0
    #pprint(prefs)
    for person in prefs:
        c += prefs[person][refTopic] & prefs[person][otherTopic]
        a += prefs[person][refTopic]
        b += prefs[person][otherTopic]
    if not c:
        return 0
    return float(c)/(a+b-c)