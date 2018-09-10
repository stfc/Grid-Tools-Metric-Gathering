"""This script is a unit test for metrics_gocdb"""
import xml.dom.minidom
import unittest
from metrics_gocdb import _parse_get_user_xml, _parse_get_user_xml_roles, get_sites, get_countries

class TestMetricsGOCDB(unittest.TestCase):
    """This class holds the functions needed to test metrics_GOCDBv4"""
    def test_parse_get_user_xml(self):
        """Test the _parse_get_user_xml method."""
        parsed_user_xml = xml.dom.minidom.parseString(GET_USER_XML)
        number_of_user = _parse_get_user_xml(parsed_user_xml)
        self.assertEquals(number_of_user, 2)

    def test_parse_get_user_xml_roles(self):
        """Test the _parse_get_user_xml method."""
        parsed_user_xml = xml.dom.minidom.parseString(GET_USER_XML)
        number_of_user_with_roles = _parse_get_user_xml_roles(parsed_user_xml)
        self.assertEquals(number_of_user_with_roles, 1)

    def test_get_sites(self):
        """Test the get_sites method"""
        parsed_site_xml = xml.dom.minidom.parseString(GET_SITE_XML)
        site_number = get_sites(parsed_site_xml)
        self.assertEquals(site_number, 3)
    def test_get_countries(self):
        """Test the get_countries method"""
        parsed_country_xml = xml.dom.minidom.parseString(GET_COUNTRY_XML)
        country_list = get_countries(parsed_country_xml)
        answer_list = (1, [u"Algeria"])
        self.assertEquals(country_list, answer_list)

GET_USER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<results>
  <EGEE_USER ID="1G0" PRIMARY_KEY="1G0">
    <FORENAME>ALEX</FORENAME>
    <SURNAME>TSELOS</SURNAME>
    <TITLE>MR</TITLE>
    <DESCRIPTION></DESCRIPTION>
    <GOCDB_PORTAL_URL></GOCDB_PORTAL_URL>
    <EMAIL>LeeGit@user.com</EMAIL>
    <TEL>4</TEL>
    <WORKING_HOURS_START/>
    <WORKING_HOURS_END/>
    <CERTDN>LeeGit DN</CERTDN>
    <SSOUSERNAME>lgit</SSOUSERNAME>
    <APPROVED/>
    <ACTIVE/>
    <HOMESITE>STFC RAL</HOMESITE>
    <USER_ROLE>
      <USER_ROLE>Site Operations Manager</USER_ROLE>
      <ON_ENTITY>RAL</ON_ENTITY>
      <ENTITY_TYPE>site</ENTITY_TYPE>
      <PRIMARY_KEY>4</PRIMARY_KEY>
      <RECOGNISED_IN_PROJECTS>
      <PROJECT ID="1">EGI</PROJECT>
      </RECOGNISED_IN_PROJECTS>
    </USER_ROLE>
  </EGEE_USER>
 <EGEE_USER ID="2G0" PRIMARY_KEY="2G0">
    <FORENAME>X</FORENAME>
    <SURNAME>Y</SURNAME>
    <TITLE/>
    <DESCRIPTION></DESCRIPTION>
    <GOCDB_PORTAL_URL></GOCDB_PORTAL_URL>
    <EMAIL>LeeGit@user.com</EMAIL>
    <TEL>2</TEL>
    <WORKING_HOURS_START/>
    <WORKING_HOURS_END/>
    <CERTDN>LeeGit DB</CERTDN>
    <SSOUSERNAME>lgit</SSOUSERNAME>
    <APPROVED/>
    <ACTIVE/>
    <HOMESITE></HOMESITE>
  </EGEE_USER>
</results>"""

GET_SITE_XML = \
"""<results>
 <SITE ID="40" PRIMARY_KEY="73G0" NAME="TU-Kosice" COUNTRY="Slovakia"
 COUNTRY_CODE="SK" ROC="NGI_SK" SUBGRID=""
 GIIS_URL="ldap://mon.grid.tuke.sk:2170/Mds-Vo-name=TU-Kosice,o=grid"/>

<SITE ID="41" PRIMARY_KEY="201G0" NAME="IISAS-Bratislava" COUNTRY="Slovakia"
 COUNTRY_CODE="SK" ROC="NGI_SK" SUBGRID=""
 GIIS_URL="ldap://sbdii.ui.savba.sk:2170/Mds-Vo-name=IISAS-Bratislava,o=grid"/>

<SITE ID="42" PRIMARY_KEY="8G0" NAME="prague_cesnet_lcg2_cert"
 COUNTRY="Czech Republic" COUNTRY_CODE="CZ"
 ROC="NGI_CZ" SUBGRID=""
 GIIS_URL=" ldap://skurut16.cesnet.cz:2170/m_cert,o=grid"/>
</results>"""

GET_COUNTRY_XML = \
"""<results>
<SITE>
<COUNTRY>Afghanistan</COUNTRY>
<COUNT>0</COUNT>
</SITE>
<SITE>
<COUNTRY>Albania</COUNTRY>
<COUNT>0</COUNT>
</SITE>
<SITE>
<COUNTRY>Algeria</COUNTRY>
<COUNT>2</COUNT>
</SITE>
<SITE>
<COUNTRY>American Samoa</COUNTRY>
<COUNT>0</COUNT>
</SITE>
</results>"""

