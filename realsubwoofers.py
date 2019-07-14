#!/usr/bin/env python
import os
import random
import json
from twython import Twython


def create_client():
    """Create Twython client"""

    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_key = os.environ.get('ACCESS_KEY')
    access_secret = os.environ.get('ACCESS_SECRET')
    twitter = Twython(consumer_key, consumer_secret, access_key, access_secret)

    return twitter


def tweet(test=False):
    """Build and push tweet"""

    twitter = create_client()

    # Get random follower
    followers = (twitter.get_followers_list())['users']
    username = (random.choice(followers))['screen_name']

    # Get a random message
    messages = open('/opt/subwoofers_assets/messages.txt').read().splitlines()
    message = (random.choice(messages).format('micort35') if test
               else random.choice(messages).format(username))

    # Get random image/gif from library
    image = random.choice(os.listdir('/opt/subwoofers_assets/media/'))
    image_path = f'/opt/subwoofers_assets/media/{image}'

    # Push tweet, log API response
    with open(image_path, 'rb') as photo:
        print(f'Attempting to tweet the following: {message}, {image_path}')
        media = twitter.upload_media(media=photo)
        status = twitter.update_status(status=message,
                                       media_ids=[media['media_id']])
        print(f'Response from status post: {json.dumps(status, indent=4)}')
        if test:
            twitter.destroy_status(id=status['id'])


def lambda_handler(event, context):
    """Entry point for AWS Lambda"""

    if event['test']:
        print('TESTING: Invoked by AWS Lambda test')
        tweet(test=True)
    else:
        tweet()

    # Log remaining execution time
    time_left = context.get_remaining_time_in_millis()
    print(f'Allotted time(ms) remaining: {time_left}')
