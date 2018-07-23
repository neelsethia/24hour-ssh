#!/bin/env python

import sys
import boto3
import moto
import string
import random
import pytest
import botocore
from botocore.exceptions import ClientError
import datetime


def generate_random_s3_bucketname(size=12):
    try:
        assert isinstance(size, int) and size >= 1
    except AssertionError:
        raise ValueError("'size' param must be a positive integer grater than 0")
    chars=string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def test_generate_random_s3_bucketname():
    bucket_name = generate_random_s3_bucketname()
    assert len(bucket_name) == 12
    bucket_name = generate_random_s3_bucketname(6)
    assert len(bucket_name) == 6 
    with pytest.raises(ValueError):
        bucket_name = generate_random_s3_bucketname(-5)
        bucket_name = generate_random_s3_bucketname('blee')
    for x in generate_random_s3_bucketname():
        assert x in string.ascii_lowercase + string.digits


def new_bucket(name, region='us-west-2'):
    s3 = boto3.resource('s3')
    return s3.create_bucket(
        Bucket=name,
        CreateBucketConfiguration={'LocationConstraint': region},
    )

def test_new_bucket():
    with moto.mock_s3():
        bucket_name = generate_random_s3_bucketname()
        bucket = new_bucket(bucket_name)
        assert isinstance(bucket, boto3.resources.base.ServiceResource)
        assert isinstance(bucket.creation_date, datetime.datetime)
        assert bucket.name == bucket_name


def delete_bucket(name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name)
    bucket.delete()

def test_delete_bucket():
    with moto.mock_s3():
        bucket_name = generate_random_s3_bucketname()
        bucket = new_bucket(bucket_name)
        delete_bucket(bucket_name)
        assert bucket.creation_date == None
        client = botocore.session.get_session().create_client('s3')
        with pytest.raises(client.exceptions.NoSuchBucket):
            client.list_objects(Bucket=bucket_name)


if __name__ == '__main__':
    bucket_name = generate_random_s3_bucketname()
    print(bucket_name)
    bucket = new_bucket(bucket_name)
    print(type(bucket))
    delete_bucket(bucket_name)
    print(bucket.creation_date)
