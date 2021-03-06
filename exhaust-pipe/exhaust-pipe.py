#!/usr/bin/python

import os
import json
import yaml
import random
import struct
import socket
import uuid
import gzip
import boto3
from time import sleep

from randomdate import RandomDate

def read_yaml(filename):
    """
    Read a yaml resource file
    """
    with open(filename, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def newlogline(randomdate, locations, movies):
        # date and time
        line = randomdate.random()
        # x-edge-location
        line += '\t' + locations[random.randint(0, len(locations)-1)]
        # sc-bytes
        line += '\t' + str(random.randint(1024, 262144000))
        # c-ip
        line += '\t' + socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        # cd-method
        line += '\tGET'
        # cs host
        line += '\td111111abcdef8.cloudfront.net'
        # cs-uri-stem
        slug = movies[random.randint(0, len(movies)-1)]
        line += '\t/movies/' + slug + '/dummy.mp4'
        # cs-status
        line += '\t200'
        # cs referer
        line += '\thttps://www.example.com/movies/' + slug
        # cs user-agent
        line += '\tMozilla/5.0%2520(Windows%2520NT%25206.3;%2520WOW64)%2520AppleWebKit/537.36' \
                '%2520(KHTML,%2520like%2520Gecko)%2520Chrome/46.0.2490.71%2520Safari/537.36'
        # cs-uri-query
        line += '\t-'
        # cs cookie
        line += '\t-'
        # x-edge-result-type
        line += '\tHit'
        # x-edge-request-id
        line += '\t' + str(uuid.uuid4())
        # x-host-header
        line += '\twww.example.com'
        # cs-protocol
        line += '\thttps'
        # cs-bytes
        line += '\t' + str(random.randint(128, 1024))
        # time-taken
        line += '\t' + str(round(random.uniform(0.03, 2.0), 4))
        # x-forwarded-for
        line += '\t-'
        # ssl-protocol
        line += '\tTLSv1.2'
        # ssl-cipher
        line += '\tECDHE-RSA-AES128-GCM-SHA256'
        # x-edge-response-result-type
        line += '\tHit'

        return line

def newlogfile(config, s3_client, randomdate, locations, movies):
    filename =  str(uuid.uuid4()) + '.gz'
    if s3_client is None:
        path = config['files']['location']
    else:
        path = '/tmp/'

    with gzip.open(path + filename, 'wb') as stream:
        lines = random.randint(config['content']['minLines'], config['content']['maxLines'])
        for _ in range(lines):
            line = newlogline(randomdate, locations, movies) + '\n'
            stream.write(line.encode())

    if s3_client is not None:
        s3_client.upload_file(path + filename, config['files']['bucket'], filename)
        os.remove(path + filename)

def main():
    config = read_yaml('resources/config.yml')

    s3_client = None
    if config['files']['storage'] == 'S3':
        AWS_ACCESS_KEY_ID = os.environ['EXHAUST_AWS_ACCESS_KEY_ID']
        AWS_SECRET_ACCESS_KEY = os.environ['EXHAUST_AWS_SECRET_ACCESS_KEY']

        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='eu-west-1')
    else:
        if os.path.isdir(config['files']['location']) == False:
            os.mkdir(config['files']['location'])
        else:
            print('Local path exists.')

    locations = read_yaml('resources/edgelocations.yml')['locations']
    movies = read_yaml('resources/movies.yml')['slugs']
    randomdate = RandomDate(config['content']['startDate'], config['content']['endDate'])

    if config['forever']:
        while True:
            newlogfile(config, s3_client, randomdate, locations, movies)
            seconds = round(random.uniform(config['interval']['minSeconds'], \
                    config['interval']['maxSeconds']), 1)
            print('sleep for ' + str(seconds) + ' seconds')
            sleep(seconds)
    else:
        newlogfile(config, s3_client, randomdate, locations, movies)

if __name__ == '__main__':
    main()
