#!/usr/bin/python

import json
import yaml
import random
import struct
import socket
import uuid

from randomdate import RandomDate

def read_config():
    """
    Read exhuast.conf
    """
    with open('resources/exhaust.conf', 'r') as config_file:
        config = json.load(config_file)
        return config

def read_edgelocations():
    """
    Read edge locations from a resource file
    """
    with open('resources/edgelocations.yml', 'r') as stream:
        try:
            doc = yaml.load(stream)
            return  doc["locations"]
        except yaml.YAMLError as exc:
            print(exc)

def read_movies():
    """
    Read movie slugs from a resource file
    """
    with open('resources/movies.yml', 'r') as stream:
        try:
            doc = yaml.load(stream)
            return doc["slugs"]
        except yaml.YAMLError as exc:
            print(exc)

def main():

    config = read_config()

    locations = read_edgelocations()
    sizel = len(locations)

    movies = read_movies()
    sizem = len(movies)

    rd = RandomDate('2016-01-01', '2016-04-30')

    with open('cf.log', 'w') as stream:
        for _ in range(75000):
            # date and time
            line = rd.random()
            # x-edge-location
            line += '\t' + locations[random.randint(0, sizel-1)]
            # sc-bytes
            line += '\t' + str(random.randint(1024, 262144000))
            # c-ip
            line += '\t' + socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            # cd-method
            line += '\tGET'
            # cs host
            line += '\td111111abcdef8.cloudfront.net'
            # cs-uri-stem
            slug = movies[random.randint(0, sizem-1)]
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
            stream.write(line + '\n')
            # x-forwarded-for
            line += '\t-'
            # ssl-protocol
            line += '\tTLSv1.2'
            # ssl-cipher
            line += '\tECDHE-RSA-AES128-GCM-SHA256'
            # x-edge-response-result-type
            line += '\tHit'

if __name__ == '__main__':
    main()
