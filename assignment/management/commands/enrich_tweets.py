import logging
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from sqlalchemy.engine import create_engine
import requests
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Hive connection
engine = create_engine(settings.HIVE_CONNECTION_STR)


def hash_tags_from_tweets(tweets):
    if not tweets:
        return ''
    try:
        tweets1 = tweets.replace('"', '__-qv-__') # temp
        tweets1 = tweets1.replace('\'', '"') # replace single quote with double to be valid JSON
        tweets1 = tweets1.replace('__-qv-__', "'") # set original double quote as single
        tweets_json = json.loads(tweets1)  # JSON is double quotes string,
        hash_tags_json = tweets_json['hashtags']
        hash_tags = []
        for hash_tag in hash_tags_json:
            hash_tags.append(hash_tag['text'])
        return hash_tags
    except Exception as e:
        # ideally, the tweets field should be JSON field so it shouldn't fail -- not sure what format this value have!
        # #TODO I don't want to spend more on this so ignore and fix later
        logger.warning(f'could not parse: {tweets}')
        logger.exception(e)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            's3_source', type=str, help='S3 link')

    def handle(self, **options):
        s3_source = options.get('s3_source', None)
        df = pd.read_parquet(s3_source)
        df = df.drop(columns=['tweet_full_text', 'tweet_in_reply_to_screen_name',
                              'tweet_in_reply_to_user_id_str', 'tweet_source'])
        page_size = 10
        index = 0

        all_ids = list(set(df['user_id_str']))
        df['club'] = ''

        # TODO - cross product, timing out so I think I'm doing something wrong here
        # df2 = pd.DataFrame()
        # df2['hash_tag'] = df.apply(lambda row: hash_tags_from_tweets(row['tweet_entities']),axis=1)
        # df.merge(df2, how='cross')

        while True:
            ids_page = all_ids[index:index+page_size]
            if not ids_page:
                # empty
                break

            # get bulk of ids
            # I don't want to run in parallel to avoid over-heading server/database
            # throttling on server might be needed
            r = requests.get(f'http://127.0.0.1:8000/assignment/api/v1/users/query/?ids={",".join(str(v) for v in ids_page)}')
            users_info = r.json()
            # index data for quicker access
            user_id_to_user_obj = {user['external_id']: user for user in users_info['results']}
            # too slow, not sure if this is realistic for Dataframe.apply...? too much data or not optimized?
            df['club'] = df.apply(
                lambda x: user_id_to_user_obj.get(x['user_id_str'])['club'] if user_id_to_user_obj.get(x['user_id_str']) else x['club'],
                axis=1
            )
            index += page_size
        df.to_parquet('./output.parquet')

        df = df.drop(columns=['tweet_entities'])

        conn = engine.connect()
        df.to_sql(name='tweets', con=engine, index=False, if_exists='append', chunksize=1000, method='multi')