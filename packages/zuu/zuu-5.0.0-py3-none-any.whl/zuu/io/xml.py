import xml.etree.ElementTree as ET


class Xml:
    @staticmethod
    def load(path: str) -> ET.Element:
        return ET.parse(path).getroot()

    @staticmethod
    def dump(path: str, data: ET.Element):
        ET.ElementTree(data).write(path)

    @staticmethod
    def dumps(data: ET.Element) -> str:
        return ET.tostring(data, encoding="utf-8")

    loads = ET.fromstring
