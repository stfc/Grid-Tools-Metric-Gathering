"""This script can be used to unit test metric_apel"""
import xml.dom.minidom
from metrics_apel import get_sites, get_services, get_countries
import unittest



class TeestMetricsAPEL(unittest.TestCase):
    """This class holds the test for metrics_APELv4"""
    def test_get_sites(self):
        """Tests the get_sites method"""
        apel_xml_parsed = xml.dom.minidom.parseString(apel_xml)
        xml_obj =\
            apel_xml_parsed.getElementsByTagName('SERVICE_ENDPOINT')
        site_list = get_sites("APEL", xml_obj)
        answer_list = (1, [u"MD-02-IMI"])
        self.assertEquals(site_list, answer_list)

    def test_get_services(self):
        """Tests the get_services method"""
        apel_xml_parsed = xml.dom.minidom.parseString(apel_xml)
        xml_obj =\
            apel_xml_parsed.getElementsByTagName('SERVICE_ENDPOINT')
        service_list = get_services("APEL", xml_obj)
        self.assertEquals(service_list, 1)

    def test_get_countries(self):
        """Tests the get_countries method"""
        apel_xml_parsed = xml.dom.minidom.parseString(apel_xml)
        xml_obj =\
            apel_xml_parsed.getElementsByTagName('SERVICE_ENDPOINT')
        country_list = get_countries("APEL", xml_obj)
        answer_list = ([u"CRETE"], 1)
        self.assertEquals(country_list, answer_list)


apel_xml = """<results>
<SERVICE_ENDPOINT PRIMARY_KEY="368G0">
<PRIMARY_KEY>368G0</PRIMARY_KEY>
<HOSTNAME>node05-02.imi.renam.md</HOSTNAME>
<GOCDB_PORTAL_URL>
</GOCDB_PORTAL_URL>
<BETA>N</BETA>
<SERVICE_TYPE>APEL</SERVICE_TYPE>
<CORE/>
<IN_PRODUCTION>Y</IN_PRODUCTION>
<NODE_MONITORED>Y</NODE_MONITORED>
<NOTIFICATIONS>N</NOTIFICATIONS>
<SITENAME>MD-02-IMI</SITENAME>
<COUNTRY_NAME>CRETE</COUNTRY_NAME>
<COUNTRY_CODE>MD</COUNTRY_CODE>
<ROC_NAME>NGI_MD</ROC_NAME>
<URL/>
<ENDPOINTS/>
<SCOPES>
<SCOPE>EGI</SCOPE>
</SCOPES>
<EXTENSIONS/>
<HOSTDN> ALEX TSELOS </HOSTDN>
</SERVICE_ENDPOINT>
</results>"""
