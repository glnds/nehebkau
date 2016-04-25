#!/usr/bin/python

import json
import yaml
import random
import struct
import socket

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
    print(config)

    locations = read_edgelocations()
    sizel = len(locations)

    movies = read_movies()
    print(len(movies))

    rd = RandomDate('2016-01-01', '2016-04-30')
    print(rd.random())

    with open('cf.log', 'w') as stream:
        # date and time
        line = rd.random()
        # x-edge-location
        line += '\t' + locations[random.randint(0, sizel-1)]
        # sc-bytes
        line += '\t' + random.randint(1024, 262144000)
        # c-ip
        socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        stream.write(line)

if __name__ == '__main__':
    main()
