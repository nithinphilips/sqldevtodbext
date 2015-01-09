# -*- coding: utf-8 -*-


"""sqldevtodbext.sqldevfileparser: Parses SQL Developer connection.xml files"""

import re

from bunch import Bunch
from xml.etree import ElementTree
from .sqldevpasswordcrypto import encryptv4, decryptv4

class OracleConnection(Bunch):
    """
    An Oracle Connection configuration object.
    """

    def postinit(self):
        """
        Performs post-initialization tasks. You MUST call this after the
        initialization of this object is complete.

        This provides some default values and creates
        some generated values based on what was read
        from the XML file.
        """
        if 'sid' in self:
            self.srvname = ("(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)"
                            "(Host={hostname})(Port={port}))(CONNECT_DATA="
                            "(SID={sid})))").format(**self)
        elif 'serviceName' in self:
            self.srvname = ("(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)"
                            "(Host={hostname})(Port={port}))(CONNECT_DATA="
                            "(SERVICE_NAME={serviceName})))").format(**self)
        else:
            self.srvname = ''

        if 'password' not in self:
            self.password = ''

        self.ConnNameSafe = re.sub(r'\s', '', self.ConnName)


def parse(xmlfile, password):
    """
    Parses a SQL Developer ``Connection.xml`` file. This could be
    the default config file or an export made from SQL Developer.

    A password is required to decrypt any passwords.

    Only SQLDeveloper version 4 files are supported.

    xmlfile: path to the ``Connection.xml`` file
    password: the password to decode encrypted stored passwords
    """
    tree = ElementTree.parse(xmlfile)
    references = tree.getroot()

    for reference in references:
        conn = OracleConnection()
        conn.name = reference.get('name')

        for refaddress in reference.find('RefAddresses'):
            addrType = refaddress.get('addrType')
            addrValue = refaddress.find('Contents').text

            if addrType == 'password':
                try:
                    addrValue = decryptv4(addrValue, password)
                except:
                    pass

            conn[addrType] = addrValue

        conn.postinit()
        yield conn

