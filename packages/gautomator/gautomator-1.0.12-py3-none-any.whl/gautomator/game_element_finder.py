from xml.dom import minidom
from lxml import etree

from gautomator.by import By
from gautomator.element_type import ElementType
from gautomator.game_element import GameElement


class GameElementFinder:
    _gauto: object
    _xml: str
    _xml_doc: object
    _element_type: str

    def __init__(self, gauto, xml: str):
        self._gauto = gauto
        self._xml = xml
        if len(xml) > 0:
            self._xml_doc = minidom.parseString(xml)
            self._element_type = self._xml_doc.documentElement.getAttribute("elementType")

    def construct_game_element(self, dom_element) -> GameElement:
        return GameElement(self._gauto, self._element_type, dom_element.attributes.items())

    def construct_game_element_from_lxml(self, element) -> GameElement:
        return GameElement(self._gauto, self._element_type, element.items())

    def construct_game_elements_from_uwidget_info(self, uwidget_info) -> GameElement:
        ret = []
        if uwidget_info[0] :
            widget_info = uwidget_info[1]
            ret.append(GameElement(self._gauto, "UWidget", widget_info.to_json().items(), widget_info=widget_info, deferred_load=True))
        return ret

    def find_by_attribute(self, attribute_name: str = None, attribute_value: str = None):
        found_game_elements = []
        if self._element_type == ElementType.UWIDGET or \
                self._element_type == ElementType.SWIDGET or \
                self._element_type == ElementType.GAMEOBJECT:
            all = self._xml_doc.getElementsByTagName(self._element_type)
            for element in all:
                if element.getAttribute(attribute_name) == attribute_value:
                    found_game_elements.append(self.construct_game_element(element))
        return found_game_elements

    def find_by_xpath(self, xpath):
        found_game_elements = []
        root = etree.XML(self._xml)
        all = root.xpath(xpath)
        for element in all:
            found_game_elements.append(self.construct_game_element_from_lxml(element))
        return found_game_elements

    def find_by(self, by: str = By.NAME, value: str = None) -> GameElement:
        if by == By.XPATH:
            return self.find_by_xpath(value)
        else:
            if self._element_type == ElementType.UWIDGET or \
                    self._element_type == ElementType.SWIDGET or \
                    self._element_type == ElementType.GAMEOBJECT:
                return self.find_by_attribute(by, value)

    def find_by_xpath_and_get_parent(self, xpath):
        found_game_elements = []
        root = etree.XML(self._xml)
        all = root.xpath(xpath)
        for element in all:
            parent = element.getparent()
            if parent is not None and parent.tag == self._element_type:
                found_game_elements.append(self.construct_game_element_from_lxml(element.getparent()))
                return found_game_elements
        return []

    def find_by_attribute_and_get_parent(self, attribute_name: str = None, attribute_value: str = None):
        found_game_elements = []
        if self._element_type == ElementType.UWIDGET or \
                self._element_type == ElementType.SWIDGET or \
                self._element_type == ElementType.GAMEOBJECT:
            root = etree.XML(self._xml)
            all = root.findall('.//'+self._element_type)
            for element in all:
                if element.get(attribute_name) == attribute_value:
                    parent = element.getparent()
                    if parent is not None and parent.tag == self._element_type:
                        found_game_elements.append(self.construct_game_element_from_lxml(element.getparent()))
                        return found_game_elements
        return found_game_elements

    def find_by_and_get_parent(self, by: str = By.NAME, value: str = None) -> GameElement:
        if by == By.XPATH:
            return self.find_by_xpath_and_get_parent(value)
        else:
            if self._element_type == ElementType.UWIDGET or \
                    self._element_type == ElementType.SWIDGET or \
                    self._element_type == ElementType.GAMEOBJECT:
                return self.find_by_attribute_and_get_parent(by, value)
