from djongo import models
import djongo.base
from django.db import connections

from bson import ObjectId

# Create your models here.

####
# Monkey patch
djongo.base.DatabaseWrapper.operators['in'] = '$in %s'
#####

def get_database_connection():
    """
    Get DB connection
    :return:
    """
    db_wrapper = connections['default']
    # If first call, make sure connection is established
    db_wrapper.ensure_connection()

    # has open connection? get it!
    return db_wrapper.connection


class MongoModelMixin:
    # TODO: need to support the "in" operator in djongo
    @classmethod
    def query_by_ids(cls, ids):
        """
        Query objects by list of ids
        :param ids: objects ids (as string)
        :return: list of objects (models)
        """

        # Workaround to get the "__in" working in other way
        # Put in mixin not in Model manager as this return List not QuerySet
        db = get_database_connection()
        documents = db[cls.objects.model._meta.db_table].find({
            '_id': {'$in': [ObjectId(id) for id in ids]}
        })
        return [cls(**doc) for doc in documents]


class Club(models.Model, MongoModelMixin):
    class Meta:
        db_table = 'clubs'
    _id = models.ObjectIdField()
    Club = models.TextField()
    Country = models.TextField()
    UCL = models.IntegerField()
    UEL = models.IntegerField()
    CWC = models.IntegerField()
    USC = models.IntegerField()
    UIC = models.IntegerField()
    IC = models.IntegerField()
    Total = models.IntegerField()


class User(models.Model, MongoModelMixin):
    class Meta:
        db_table = 'users'

    _id = models.ObjectIdField()

    external_id = models.TextField()
    external_id_str = models.TextField()
    name = models.TextField()
    screen_name = models.TextField()
    club = models.TextField()
    location = models.TextField()
    description = models.TextField()
    url = models.TextField()
    protected = models.BooleanField()
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    listed_count = models.IntegerField()
    created_at = models.TextField()
    favourites_count = models.IntegerField()
    utc_offset = models.TextField()
    time_zone = models.TextField()
    geo_enabled = models.BooleanField()
    verified = models.BooleanField()
    statuses_count = models.IntegerField()
    lang = models.BooleanField()
    contributors_enabled = models.BooleanField()
    is_translator = models.BooleanField()
    is_translation_enabled = models.BooleanField()
    profile_background_color = models.TextField()
    profile_background_image_url = models.TextField()
    profile_background_image_url_https = models.TextField()
    profile_background_tile = models.BooleanField()
    profile_image_url = models.TextField()
    profile_image_url_https = models.TextField()
    profile_banner_url = models.TextField()
    profile_link_color = models.TextField()
    profile_sidebar_border_color = models.TextField()
    profile_sidebar_fill_color = models.TextField()
    profile_text_color = models.TextField()
    profile_use_background_image = models.BooleanField()
    has_extended_profile = models.BooleanField()
    default_profile = models.BooleanField()
    default_profile_image = models.BooleanField()
    following = models.BooleanField()
    follow_request_sent = models.BooleanField()
    notifications = models.BooleanField()
    translator_type= models.TextField()
    entities = models.JSONField()
