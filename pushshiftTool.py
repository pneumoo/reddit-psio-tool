# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 21:43:23 2018

@author: Brian
"""

import json
import requests
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


"""
Returns a string of the URL COMMENT Search command for Pushshift.io
Example: 'https://api.pushshift.io/reddit/search/comment/?author=username123'
Inputs (not all have been implemented here, see github.com/pushshift/api for more info)
    * q is search term, type=str. 
        PSIO will search the comments' 'body' field for this search term
    * author is a redditor user name, type=str
        Restrict search to a specific author
    * after is an epoch value or integer + "s,m,h,d" (i.e. 30d for 30 days), type=str
        Returns any results more recently than this date
    * before is an epoch value or integer + "s,m,h,d" (i.e. 30d for 30 days), type=str
        Returns any results prior to this date
    * size Number of results to return, type=str or int
        Number must be <=500
    * fields is a single string of comma-delimited database fields
        Ex: fields='body,created_utc,id,link_id,parent_id,subreddit'
    * ids is a comma-delimited string of a reddit comment ID number
        Either form acceptable: "t1_dvtkqx4" or "dvtkqx4" 
    
Note: leaving all inputs blank defaults to retrieving the most recent 25
comments in the database with all fields returned.
"""
def mkComURL(q=None, 
                  author=None, 
                  after=None, 
                  before=None,
                  size=None, 
                  fields=None,
                  ids=None):
   
    searchstr = 'https://api.pushshift.io/reddit/comment/search/?'
   
    if q:
        searchstr += "q={0}&".format(q)
    if author:
        searchstr += "author={0}&".format(author)
    if after:
        searchstr += "after={0}&".format(after)
    if before:
        searchstr += "before={0}&".format(before)
    if size:
        searchstr += "size={0}&".format(size)
    if fields:
        searchstr += "fields={0}&".format(fields)
    if ids:
        searchstr += "ids={0}&".format(ids)
    
    return(searchstr)



"""
Returns a string of the URL SUBMISSION Search command for Pushshift.io
Example: 'https://api.pushshift.io/reddit/search/submission/?author=username123'
Inputs (not all have been implemented here, see github.com/pushshift/api for more info)
    * q is search term, type=str. 
        PSIO will search ALL possible fields for this string
    * author is a redditor user name, type=str
        Restrict search to a specific author
    * after is an epoch value or integer + "s,m,h,d" (i.e. 30d for 30 days), type=str
        Returns any results more recently than this date
    * before is an epoch value or integer + "s,m,h,d" (i.e. 30d for 30 days), type=str
        Returns any results prior to this date
    * size Number of results to return, type=str or int
        Number must be <=500
    * fields is a single string of comma-delimited database fields
        Ex: fields='body,created_utc,id,link_id,parent_id,subreddit'
    * ids is a comma-delimited string of a reddit comment ID number
        Either form acceptable: "t1_dvtkqx4" or "dvtkqx4" 
    *
"""
def mkSubURL(q=None, 
                  author=None, 
                  after=None, 
                  before=None,
                  size=None, 
                  fields=None,
                  ids=None):
    
    searchstr = 'https://api.pushshift.io/reddit/submission/search/?'
   
    if q:
        searchstr += "q={0}&".format(q)
    if author:
        searchstr += "author={0}&".format(author)
    if after:
        searchstr += "after={0}&".format(after)
    if before:
        searchstr += "before={0}&".format(before)
    if size:
        searchstr += "size={0}&".format(size)
    if fields:
        searchstr += "fields={0}&".format(fields)
    if ids:
        searchstr += "ids={0}&".format(ids)
    
    return(searchstr)
    
    ### FOLLOW commentSearch function for building this...
    
    
"""
Returns JSON object of requested Pushshift.io data
inputs:
    * psioAPIendpoint is a URL command to extract data from db
"""
def getPSIOjson(psioAPIendpoint):
    r = requests.get(psioAPIendpoint)
    rjson = r.json()
    return(rjson)


"""
Returns a list of comment parameter values
inputs:
    * json_data is json output from pushshift.io
    * commentParam (str) is any of the Keys returned for each comment
        See https://github.com/pushshift/api "Search parameters for comments" section
""" 
def getParam(json_data, param):
    data = json_data['data']
    paramList = []
    for i in data:
        try:
            paramList.append(i[param])
        except:
            print("**ERROR: Could not find " + param + " in the following entry. SKIPPING***")
            print(i)
            print()
    return(paramList)



def getAllUserComments():
    author = input("Get all comment info for user: ")
    maxsize = 100
    loopcount = 0
    beforetime = int(time.time())
    userdata = {'data':[]}
    while True:
        # print("LOOP: {0}".format(loopcount))
        # print("beforetime: {0}".format(beforetime))
        url = mkComURL(author=author, before=beforetime, size=maxsize)
        data = getPSIOjson(url)
        userdata['data'] += data['data']
        
        datalen = len(data['data'])
        if datalen == maxsize:
            print("{0} comments found".format(maxsize*loopcount))
        else:
            print("COMPLETE. {0} comments found.".format(maxsize*loopcount + datalen))
            break
        
        loopcount += 1
        beforetime = data['data'][-1]['created_utc']
    
    return(userdata)


def getAllUserSubmissions():
    author = input("Get all submission info for user: ")
    maxsize = 100
    loopcount = 0
    beforetime = int(time.time())
    userdata = {'data':[]}
    while True:
        url = mkSubURL(author=author, before=beforetime, size=maxsize)
        data = getPSIOjson(url)
        userdata['data'] += data['data']
        
        datalen = len(data['data'])
        if datalen == maxsize:
            print("{0} submissions found".format(maxsize*loopcount))
        else:
            print("COMPLETE. {0} submissions found.".format(maxsize*loopcount + datalen))
            break
        
        loopcount += 1
        beforetime = data['data'][-1]['created_utc']
    
    return(userdata)


"""
Returns a list of comment IDs for a submission ID - PSIO IS BUGGY??
inputs:
    * Base36 submission ID as a string
"""
def getCommentIDsForSubmission(submissionID):
    searchstr = 'http://api.pushshift.io/reddit/submission/comment_ids/' + str(submissionID)
    jsondata = getPSIOjson(searchstr)
    return(jsondata["data"])


"""
"""
def getParents(comment_parent_ids):
    numperreq = 100 #max number of parent comments to get per request
    parent_data = {'data':[]}
    com_parents_string = ""
    sub_parents_string = ""
    commentbaseurl = "https://api.pushshift.io/reddit/comment/search?ids="
    subbaseurl = "https://api.pushshift.io/reddit/submission/search?ids="
    print("Total parent comments = " + str(len(parent_data["data"])))
    for i,j in enumerate(comment_parent_ids):
#        print(i,j,len(comment_parent_ids))
        if j[1] == '1':
            com_parents_string += j[3:] + ','
        
        if j[1] == '3':
            sub_parents_string += j[3:] + ','
        
        if (i%numperreq == numperreq-1) or (i+1 == len(comment_parent_ids)):
            #comments and submissions have to be queried separately
            print(com_parents_string)
            print(sub_parents_string)
            
            if com_parents_string != "":
                print("Getting parent comments from PSIO...")
                com_search_str = commentbaseurl + com_parents_string
                print(com_search_str)
                comjsondata = getPSIOjson(com_search_str)
                for comment in comjsondata["data"]:
                    parent_data["data"].append(comment)
                print("Parent comments fetched in last batch = " + str(len(comjsondata["data"])))
                
            if sub_parents_string != "":
                print("Getting parent submissions from PSIO...")
                sub_search_str = subbaseurl + sub_parents_string
                print(sub_search_str)
                subjsondata = getPSIOjson(sub_search_str)
                for sub in subjsondata["data"]:
                    parent_data["data"].append(sub)
                print("Parent submissions fetched in last batch = " + str(len(subjsondata["data"])))

            com_parents_string = "" #clears comment ID list string for next batch
            sub_parents_string = "" #clears submission ID list string for next batch
            print("Total parent comments = " + str(len(parent_data["data"])))
            print(".")
            print(".")
            
    return(parent_data)


"""
=====================================================================
+++++++++ PLOTTING AND ANALYSIS +++++++++++++++++++++++++++++++++++++
=====================================================================
Ideas: 
    * Language processing of comments
    * Language processing of submission titles
    * subreddit activity over time
    * Top-level domains used over time
    * Duration between activity heat map
    * Engagement level in comments sections of own submissions

"""



"""
===== Compares user selfposts to linkposts
 only works with submission json data
"""
def selfVsLink(submissionjson):
    selfpost=0
    linkpost=0
    for submission in submissionjson["data"]:
        if submission["is_self"]:
            selfpost+=1
        else:
            linkpost+=1
    print("{0}% link posts".format(100*linkpost/(selfpost+linkpost)))
    print("Selfposts:linkposts => {0}:{1}".format(selfpost,linkpost))
    return(selfpost, linkpost)


"""
===== Examines time-of-day posting patterns w/ plots
Will work with comment or submission json data
"""        
def actionsTimeOfDay(userdata, local_time=False):
    i=0
    utc_list = []
    mpl_dates = []
    tod_list = []
    while i < len(userdata["data"]):
        utc_item = userdata["data"][i]["created_utc"]
        mpl_item = matplotlib.dates.epoch2num(utc_item)
       
        if local_time:
            #Making time-of-day (by hour) so we can plot on 0-24h scale
            h = time.localtime(utc_item).tm_hour
            m = time.localtime(utc_item).tm_min
            s = time.localtime(utc_item).tm_sec
            tod_list.append((h*60*60 + m*60 + s)/3600)
        else:
            h = time.gmtime(utc_item).tm_hour
            m = time.gmtime(utc_item).tm_min
            s = time.gmtime(utc_item).tm_sec
            tod_list.append((h*60*60 + m*60 + s)/3600)
        
        utc_list.append(utc_item)
        mpl_dates.append(mpl_item)
        
        i+=1
    
    # time of day vs. posting date
    plt.figure()    
    plt.plot_date(mpl_dates, tod_list, xdate=True, ydate=False)
    plt.title("Posting time throughout history")
    plt.xlabel('Posting date')
    if local_time==1:
        plt.ylabel('Time of Day (local)')
    else:
        plt.ylabel('Time of Day (UTC)')
    plt.show()
    
    
    # 24-hour histogram of posts, binned by minute
    plt.figure()
    plt.hist(tod_list, bins=24*60)
    plt.title("24-hour histogram of posts, by minute")
    if local_time==1:
        plt.xlabel('Time of Day (local)')
    else:
        plt.xlabel('Time of Day (UTC)')
    plt.ylabel('Count')
    plt.show()
    
    
    
""""
====== Bar graph of domain submissions
 only works with submission json data
"""
def submissionDomainBarGraph(datajson, nitems=20):
    subreddit_actions = getParam(datajson, 'domain')
    counts = dict(Counter(subreddit_actions).most_common(nitems))

    labels, values = zip(*counts.items())
    # sort your values in descending order
    indSort = np.argsort(values)[::-1]
    # rearrange your data
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    indexes = np.arange(len(labels))
    
    plt.figure()
    plt.bar(indexes, values)
    plt.title('Number of submissions by top-level domain')
    plt.xlabel('Domain Name')
    plt.ylabel('Quantity')
    
    # add labels
    plt.xticks(indexes, labels, rotation='vertical')
    plt.show()
    return(counts)




""""
====== Bar graph of subreddit activity
 will work with comment or submission json data
"""
def subActivityBarGraph(datajson, nitems=20):
    subreddit_actions = getParam(datajson, 'subreddit')
    counts = dict(Counter(subreddit_actions).most_common(nitems))

    labels, values = zip(*counts.items())
    # sort your values in descending order
    indSort = np.argsort(values)[::-1]
    # rearrange your data
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    indexes = np.arange(len(labels))
    
    plt.figure()
    plt.bar(indexes, values)
    plt.title('Posts by subreddit')
    plt.xlabel('Subreddit Name')
    plt.ylabel('Quantity')
    
    # add labels
    plt.xticks(indexes, labels, rotation='vertical')
    plt.show()
    return(counts)


""""
====== Bar graph of parent commenter usernames
 will work with parent comment or parent submission json data
 """
def parentUsernameBarGraph(datajson, nitems=20):
    parent_comment_authors = getParam(datajson, 'author')
    counts = dict(Counter(parent_comment_authors).most_common(nitems))

    labels, values = zip(*counts.items())
    # sort your values in descending order
    indSort = np.argsort(values)[::-1]
    # rearrange your data
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    indexes = np.arange(len(labels))
    
    plt.figure()
    plt.bar(indexes, values)
    plt.title('Number of responses TO a given user')
    plt.xlabel('Reddit Username')
    plt.ylabel('# Responses')
    
    # add labels
    plt.xticks(indexes, labels, rotation='vertical')
    plt.show()
    return(counts)