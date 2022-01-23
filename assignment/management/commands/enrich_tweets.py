import logging

from django.core.management.base import BaseCommand

import requests
import pandas as pd

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            's3_source', type=str, help='S3 link')

    def handle(self, **options):
        s3_source = options.get('s3_source', None)
        df = pd.read_parquet(s3_source)
        page_size = 10
        index = 0

        all_ids = list(set(df['user_id_str']))
        output_df = pd.DataFrame()
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
            for user in users_info:
                # _id or external_id? if the later is correct then we need to fix the API...
                output_df['user_id'] = user['_id']
                # user country not club country, right?
                # seems like location is "Address" not country, maybe we need to use google geocoder to infer country?
                output_df['country'] = user['location']
                output_df['club'] = user['club']
                output_df['hashtags,'] = ','.join(df.loc[df.user_id_str == user['_id'], 'tweet_entities'])

        output_df.to_parquet('./output.parquet')

        # TODO
        # output_df to hive
        # had issues installing hive image into docker locally...

