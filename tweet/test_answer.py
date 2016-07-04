import tempfile

from django.conf import settings
from django.core.files import File
from django.test import TestCase

import tweepy
import storages

from .models import MyTweet

auth = tweepy.OAuthHandler(*settings.TWEEPY_CREDS)
auth.set_access_token(*settings.TWEEPY_TOKENS)

api = tweepy.API(auth)


class TestS3Tweet(TestCase):
    def test_store_to_storage(self):
        assert MyTweet.objects.count() == 0

        # Open an existing file using Python's built-in open()
        # and save it to our S3 bucket
        with open(settings.EXAMPLE_IMAGE_PATH) as f:
            tweet = MyTweet()
            tweet.image.save(f.name, File(f))
            tweet.save()

            assert tweet.image.size == 148647

            # assert we're testing an S3 stored file
            assert isinstance(tweet.image.file, storages.backends.s3boto.S3BotoStorageFile)

        # now assert can haz media upload
        with tempfile.NamedTemporaryFile(delete=True) as f:
            name = tweet.image.file.name
            f.write(tweet.image.read())
            media_ids = api.media_upload(filename=name, f=f)
            params = dict(status='test media', media_ids=[media_ids.media_id_string])
            api.update_status(**params)
