"""
This script holds the common functions between the GOCDB and
APEL metric collecting scripts
"""
import logging
import json
import requests
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch

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
        self.elastic = Elasticsearch(
            [
                {
                    'host': 'elasticsearch1.gridpp.rl.ac.uk',
                    'port': 9200,
                },
                {
                    'host': 'elasticsearch5.gridpp.rl.ac.uk',
                    'port': 9200,
                },
                {
                    'host': 'elasticsearch6.gridpp.rl.ac.uk',
                    'port': 9200,
                },
                {
                    'host': 'elasticsearch7.gridpp.rl.ac.uk',
                    'port': 9200,
                },
                {
                    'host': 'elasticsearch8.gridpp.rl.ac.uk',
                    'port': 9200,
                },
            ],
            use_ssl=True,
            verify_certs=False,
        )

    def write(self):
        """This function writes the data to elastic search"""
        data = json.dumps(self.dictionary)

        date = datetime.strftime(datetime.now(), '%Y.%m.%d')

        self.elastic.index(
            index="logstash-gridtools-metrics-%s" % date,
            doc_type='doc',
            body=data,
        )

def es_check():
    '''This function checks to see if elastic search is up '''
    code = requests.get("http://elasticsearch2.gridpp.rl.ac.uk" +
                        "/logstash-gridtools-metrics-2018.07.07/gocdb/_search").status_code
    if code == 200:
        return True
    else:
        return False
