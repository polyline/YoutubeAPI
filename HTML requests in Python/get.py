
# coding: utf-8

# ### Reference Tutorial
# http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
# 

# Introduction
# First, we use an simple example to review how to send requests and deal with it in Python.
# Second, we use an API to get comments. We should understand the JSON structure of response.
# And We download comments by chunks of 20.(It could change up to 100) So if there are more than 20 comments, we should send another request.
# This thing could be detected by checking if there is a nextPageToken attribute.
# Finally, we run this loop, keep sending requests until we get all the comments.


# ### Simple Example
# We are trying to get the information of a channel. So
# 
# 1. We need an API Key
# 2. We need to know how to send request in Python
# 3. Set parameters to construct an URL in Python(Using dictionary)
# 

import requests
import json

### MUST-DO ###
# API_KEY
YOUTUBE_API_KEY = ''
# VIDEO_ID
VIDEO_ID = ''
# CHANNEL_ID
CHANNEL_ID = ''

channels = {'part': 'statistics', 'id': CHANNEL_ID, 'key': YOUTUBE_API_KEY}
r = requests.get('https://www.googleapis.com/youtube/v3/channels', params = channels)
print(r.text)


# Try to get a list of comments
# From this video: https://www.youtube.com/watch?v=CmEVyRYmWUw
# 

comments = {'part': 'snippet,replies', 'videoId': VIDEO_ID, 'key': YOUTUBE_API_KEY, 'pageToken': None}
cnt = 0
while(1):
    r = requests.get('https://www.googleapis.com/youtube/v3/commentThreads', params = comments)

    # Turn the data into dictionary structure
    J_dic = r.json()
        
    # Store the next page token
    if 'nextPageToken' in J_dic.keys():
        comments['pageToken'] = J_dic['nextPageToken']
    else:
        comments['pageToken'] = None
        
    # Page Data Display
    print('---------------')
    print('**PAGE INFORMATION**')
    print('data type', J_dic['kind'])
    print('etag', J_dic['etag'])
    print('result counts', J_dic['pageInfo'])
    print('---------------')
    
    # Loop for each comment 
    for comment in J_dic['items']:
        snippet = comment['snippet']
        topLevelComment = snippet['topLevelComment']
        com_info = topLevelComment['snippet']
        
        print('Author Name', com_info['authorDisplayName'])
        print('Comment', com_info['textDisplay'])
        print('Original Comment', com_info['textOriginal'])
        print('likeCount', com_info['likeCount'])
        print('---', cnt)
        cnt = cnt + 1
    if comments['pageToken'] == None:
        break
print('The Total number of comments:', cnt)

