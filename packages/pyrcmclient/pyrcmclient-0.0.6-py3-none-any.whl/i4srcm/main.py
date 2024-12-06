
import sys,os
from lxml.etree import _Element as Elem
from i4srcm.xml.XmlBinaryStream import from_binary, to_binary
from i4srcm.client import RCMCNT_Client
import i4srcm.lxmlutil as lx
from i4srcm.ctl import RCMCTL

def import_test():
    ctl = RCMCTL( '127.0.0.1', 'testuser', passwd='testpass')
    client = RCMCNT_Client( 'http://127.0.0.1', username='testuser', passwd='testpass')
    elem:Elem = lx.create_element('test')
    lx.to_str(elem)

def main():
    import_test()

if __name__ == "__main__":
    main()