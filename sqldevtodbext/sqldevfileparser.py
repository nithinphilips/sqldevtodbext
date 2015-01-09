# -*- coding: utf-8 -*-


"""sqldevtodbext.stuff: stuff module within the sqldevtodbext package."""

import re

from bunch import Bunch
from xml.etree import ElementTree
from .sqldevpasswordcrypto import encryptv4, decryptv4

class OracleConnection(Bunch):

    def init(self):
        """ """
        if 'sid' in self:
            self.service = self.sid
        elif 'serviceName' in self:
            self.service = self.serviceName
        else:
            self.service = ''

        if 'password' not in self:
            self.password = ''

        self.passwordSafe = re.sub(r'\$', '\\$', self.password)

        self.ConnNameSafe = re.sub(r'\s', '', self.ConnName)




def parse_sqldev_xml(xmlfile, password):
    tree = ElementTree.parse(xmlfile)
    references = tree.getroot()

    for reference in references:
        conn = OracleConnection()
        conn.name = reference.get('name')

        for refaddress in reference.find('RefAddresses'):
            addrType = refaddress.get('addrType')
            addrValue = refaddress.find('Contents').text

            if addrType == 'password':
                addrValue = decryptv4(addrValue, password)

            conn[addrType] = addrValue

        conn.init()
        yield conn

