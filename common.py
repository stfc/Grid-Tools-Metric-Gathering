"""
This script holds the common functions between the GOCDB and
APEL metric collecting scripts
"""
import logging
import json
import requests
from datetime import datetime, timedelta

date = datetime.strftime(datetime.now() - timedelta(1), '%Y.%m.%d')


logger = logging.getLogger(__name__)

class GetData(object):
    """This class is used to fetch data"""
    def __init__(self, data, location, url):
        self.data = data
        self.location = location
        self.url = url
    def data_finder(self):
        """This function fetches the data"""
        try:
            info = \
                self.location.getElementsByTagName(self.data.upper())[0]\
                .firstChild.nodeValue
                # finds the sitename and stores it
            return info
        except IndexError:
            logger.warning('Index error when requesting '
                           +self.data.upper() + 'from' + self.url)


class ModLogger(object):
    """This class is used to modify the logger"""
    def __init__(self, LogName):
        self.LogName = LogName

    def logger_mod(self):
        """Sets up the logger"""
        # sets the logger

        #logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # sets the a file handler

        handler = logging.FileHandler(self.LogName)
        handler.setLevel(logging.INFO)

        # create a logging format

        formatter = \
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s\
                              - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger

        logger.addHandler(handler)
        logger.info('Hello world')


class ESWrite(object):
    """This class writes to elastic search"""
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def write(self):
        """This function writes the data to elastic search"""
        self.dictionary = json.dumps(self.dictionary)
        requests.post(("http://elasticsearch2.gridpp.rl.ac.uk:9200/"
                       "logstash-gridtools-metrics-%s/"
                       "metric_data/") % date,
                      data=self.dictionary)

def es_check():
    '''This function checks to see if elastic search is up '''
    code = requests.get("http://elasticsearch2.gridpp.rl.ac.uk" +
                        "/logstash-gridtools-metrics-2018.07.07/gocdb/_search").status_code
    if code == 200:
        return True
    else:
        return False
