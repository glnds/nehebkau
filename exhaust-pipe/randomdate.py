import time
import random

class RandomDate:
    """
    Class to generate random dates
    """

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, start, end):
        self.starttime = time.mktime(time.strptime(start, self.DATE_FORMAT))
        self.endtime = time.mktime(time.strptime(end, self.DATE_FORMAT))

    def random(self):
        randomtime = self.starttime + random.random() * (self.endtime - self.starttime)
        return time.strftime('%Y-%m-%d\t%H:%M:%S', time.localtime(randomtime))
