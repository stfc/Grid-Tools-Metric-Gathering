"""This script is used to collect information about GOCDB -AT"""
import requests
import xml.dom.minidom
from datetime import datetime, timedelta
import logging
from common import ESWrite, GetData, ModLogger, es_check
from optparse import OptionParser
from elasticsearch import Elasticsearch

def _parse_get_user_xml(xml_obj):
    """
    Parse XML from GOCDBPI endpoint get_users.

    Parameters
    ----------
    xml_obj: xml minidom object
             Contains the data needed, can be aquired from GOCDBPI

    Returns
    --------
    user_number: int
                 This represents the number of users

    Notes
    ------
    Someone who has appropriate permissions could
    modify this to work with a request to GOCDB. Add
    the code below to the top of the function!

    xml = requests.get("https://goc.egi.eu/gocdbpi/private/?method=get_user")
    #user_data = xml.text
    #context = xml.dom.minidom.parseString(user_data)
    """

    users = xml_obj.getElementsByTagName("EGEE_USER")
    user_number = len(users)
    return user_number

def get_sites(xml_obj):

    """
    Parses XML and finds the number of sites, through GOCDBPI

    Parameters
    ---------
    xml_obj: xml minidom object
             This is the data needed for the function to work. It
             comes from the GOCDBPI.

    Returns
    --------
    site_number: int
                 The number of sites

    Notes
    ------
    The function saves the data needed, parses it and
    converts the number of sites to a list. The length of the list
    is then used to determine the number of sites.
    """

    results = xml_obj.getElementsByTagName('SITE')
    site_number = len(results)
    return site_number

def get_countries(xml_obj):
    """
    This function gets the list and number of countries using GOCDB.

    Parameters
    ---------
    xml_obj: xml minidom object
             This is the data needed for the function to work. It comes
             from GOCDBPI(get_site_count_per_country).

    Returns
    -------
    country_list: list
                  Holds the list of countries using GOCDB

    country_number: int
                    Holds the number of countries using GOCDB

    Notes
    -----
    The way this function accomplishes this task is by checking if a country
    has sites running in it. If it does and it is not already in the list it
    is added to the list. "gocbd_portal_url" is set to "blank", as there is
    no data to help identify the error, to allow the "GetData" class to be used.
    """

    # Gets all the data into an object
    site_object = xml_obj.getElementsByTagName('SITE')

    country_list = []  # empty list made to hold countries

    gocdb_portal_url = 'blank'
    for site in site_object:
        country = GetData('COUNTRY', site, gocdb_portal_url)
        country = country.data_finder()
        try:
            count = site.getElementsByTagName(
                'COUNT'
            )[0].firstChild.nodeValue  # finds the count and stores it

            if country not in country_list and int(count) != 0:
                # Store the country if it is not in the list already
                country_list.append(country)

        except IndexError:
            logger.error('Error when requesting count')

    return (len(country_list), country_list)

def get_queries():
    """
    This function gets the number of queries GOCDB received the day before

    Returns
    -------
    query_num: int
               This is the number of queries

    Notes
    -----
    This collects yesterday's number of GOCDBPI queries whose name starts with
    "_get". It collects the previous day's data to reduce the possibility
    of acquiring incomplete data. To futher reduce the possibility the script
    should be run a sufficient time away from when the statistics update (for
    example at noon every day).
    """

    date = datetime.strftime(datetime.now() - timedelta(1), '%Y.%m.%d')

    ELASTIC_SEARCH_HOST = "elasticsearch2.gridpp.rl.ac.uk"
    elastic = Elasticsearch(ELASTIC_SEARCH_HOST)
    params_dict = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"type": "gocdb"}},
                    {"match": {"fields.service_level": "prod"}}
                ]
            }
        },
        "query": {
            "prefix": {"endpoint": "get_"}
        },
        "size": 0
    }

    result = elastic.search(index="logstash-" + date, body=params_dict)
    return result["hits"]["total"]

def __main__(options):
    """
    This is the main class. It runs all of the functions above.
    If a new metric needs to be added, make a function above and
    implement in one of the two if statements. This function also
    checks if the GOCDB API and Elastic search are up and if they
    are not it skips the metrics related to them. It also writes
    the data collected to Elastic Search if "options" is set to "True".
    """
    verify_server_cert = bool(options.verify == "True")

    es_up = es_check()
    logger = logging.getLogger('GOCDB logger')
    logger.addHandler(logging.NullHandler())
    ModLogger('GOCDB.log').logger_mod()
    logger.info('service has started')

    gocdb_metrics_dict = {}

    try:
        # Get the number of registered service providers (aka sites)
        # registered in GOCDB.
        response = requests.get(
            'https://goc.egi.eu/gocdbpi/public/?method=get_site_list',
            verify=verify_server_cert
        )

        response = response.text
        response = xml.dom.minidom.parseString(response)
        gocdb_metrics_dict['Number of sites in GOCDB'] = get_sites(response)

        # Get the number and names of the countries with atleast one site.
        response = requests.get(
            'https://goc.egi.eu/gocdbpi/public/?method=get_site_count_per_country',
            verify=verify_server_cert
        )

        response = response.text
        response = xml.dom.minidom.parseString(response)
        country_number, country_list = get_countries(response)
        gocdb_metrics_dict['Number of countries using GOCDB'] = country_number
        gocdb_metrics_dict['List of countries using GOCDB'] = country_list

    except requests.exceptions.ConnectionError:
        logger.error("Error connecting to GOCDB, "
                     "some metrics may not be fetched.")

    if es_up == True:

        gocdb_metrics_dict["Number of GOCDB API queries"] = get_queries()

    else:

        print("Elastic search is currently down "
              "Metrics could not be fetched and "
              "the dictionary of metrics could"
              "not be stored.")

        logger.error("Elastic search unresponsive: Data has not"
                     "been read or written")

    if options.write == "True":
        date = datetime.strftime(datetime.now() - timedelta(1), '%Y.%m.%d')
        ESWrite(gocdb_metrics_dict).write()
        logger.info("Elastic Search updated for " + date)
    else:
        # This can be used for testing
        print(gocdb_metrics_dict)

    logger.info('Service has ended')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-w", "--write-to-elastic", dest="write",
                      default="False",
                      help="Wether to write result to ElasticSearch or not.")
    parser.add_option("-v", "--verify-server-certificate", dest="verify",
                      default="True",
                      help="Wether to verify the server certificate or not.")
    (options, args) = parser.parse_args()

    __main__(options)
