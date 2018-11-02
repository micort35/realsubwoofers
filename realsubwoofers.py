#!/usr/bin/env python
from twython import Twython
import random
import os
import string
from logzero import logger

#get necessary keys and interface with Twitter API
def create_client():
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_key = os.environ.get('ACCESS_KEY')
    access_secret = os.environ.get('ACCESS_SECRET')
    twitter = Twython(consumer_key, consumer_secret, access_key, access_secret)
    return twitter

def tweet():
    #establish interface with Twitter API
    twitter = create_client()
    #get random follow's handle to format message with
    followers = (twitter.get_followers_ids()['ids'])
    follower = random.choice(followers)
    user = twitter.lookup_user(user_id = follower)[0]
    id = user['screen_name']
    messages = open('./assets/messages.txt').read().splitlines()
    message = random.choice(messages)
    message = message.format(id)
    #get random file from library to pair with message
    images = './assets/media/'
    image = random.choice(os.listdir(images))
    image_path = images + image
    #attempt to tweet, log variables and attempt outcome
    logger.info('Attempting to tweet the following: message = %s, image = %s'
            , message, image_path)
    with open(image_path, 'rb') as photo:
        response = twitter.upload_media(media=photo)
        twitter.update_status(status = message
                            , media_ids = [response['media_id']])
    logger.info('API response: %s', tweet)

def lambda_handler(event, context):
    tweet()
