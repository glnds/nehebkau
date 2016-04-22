#!/usr/bin/python

import json
import yaml

def read_config():
    """
    Read exhuast.conf
    """
    with open('resources/exhaust.conf', 'r') as config_file:
        config = json.load(config_file)
        print(config)

def exhaust():

    read_config()

    with open('resources/movies.yml', 'r') as stream:
        try:
            doc = yaml.load(stream)
            txt = doc["slugs"][4]
            print(txt)
            txt = doc["slugs"][13]
            print(txt)
        except yaml.YAMLError as exc:
            print(exc)

if __name__ == '__main__':
    exhaust()
