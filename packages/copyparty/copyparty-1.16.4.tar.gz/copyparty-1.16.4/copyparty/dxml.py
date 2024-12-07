import importlib
import sys
import xml.etree.ElementTree as ET

from .__init__ import PY2

def get_ET()  :
    pn = "xml.etree.ElementTree"
    cn = "_elementtree"

    cmod = sys.modules.pop(cn, None)
    if not cmod:
        return ET.XMLParser  # type: ignore

    pmod = sys.modules.pop(pn)
    sys.modules[cn] = None  # type: ignore

    ret = importlib.import_module(pn)
    for name, mod in ((pn, pmod), (cn, cmod)):
        if mod:
            sys.modules[name] = mod
        else:
            sys.modules.pop(name, None)

    sys.modules["xml.etree"].ElementTree = pmod  # type: ignore
    ret.ParseError = ET.ParseError  # type: ignore
    return ret.XMLParser  # type: ignore


XMLParser  = get_ET()


class DXMLParser(XMLParser):  # type: ignore
    def __init__(self)  :
        tb = ET.TreeBuilder()
        super(DXMLParser, self).__init__(target=tb)

        p = self._parser if PY2 else self.parser
        p.StartDoctypeDeclHandler = self.nope
        p.EntityDeclHandler = self.nope
        p.UnparsedEntityDeclHandler = self.nope
        p.ExternalEntityRefHandler = self.nope

    def nope(self, *a , **ka )  :
        raise BadXML("{}, {}".format(a, ka))


class BadXML(Exception):
    pass


def parse_xml(txt )  :
    parser = DXMLParser()
    parser.feed(txt)
    return parser.close()  # type: ignore


def mktnod(name , text )  :
    el = ET.Element(name)
    el.text = text
    return el


def mkenod(name , sub_el  = None)  :
    el = ET.Element(name)
    if sub_el is not None:
        el.append(sub_el)
    return el
