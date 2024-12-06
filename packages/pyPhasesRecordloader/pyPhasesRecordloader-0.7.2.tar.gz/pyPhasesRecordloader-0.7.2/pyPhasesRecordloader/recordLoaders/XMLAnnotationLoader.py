import xml.etree.ElementTree as ET

from pyPhases.util.Logger import classLogger

from pyPhasesRecordloader.RecordLoader import ParseError


@classLogger
class XMLAnnotationLoader:
    def __init__(self) -> None:
        super().__init__()

        self.annotations = []
        self.metaXML = None
        self.lightOff = 0
        self.lightOn = None
        self.annotationFrequency = 1
        self.minApneaDuration = 0
        self.xmlNameSpace = None

    def addNs(self, path, ns):
        ns = "{%s}" % (ns)
        nsJoin = "/" + ns
        return ns + nsJoin.join(path)

    def getXMLPath(self, xml, path):
        return xml.find(self.addNs(path, self.xmlNameSpace))

    def loadXmlFile(self, filePath):
        # nur trusted verwenden! siehe: https://docs.python.org/3/library/xml.html#xml-vulnerabilities
        self.log(f"Load xml file {filePath}")
        try:
            self.metaXML = ET.parse(filePath).getroot()
        except Exception as e:
            raise ParseError(f"Error parsing xml file {filePath}") from e
