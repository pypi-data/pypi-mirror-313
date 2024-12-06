from typing import Optional, Union
from decimal import Decimal
from bs4 import Tag, BeautifulSoup


__all__ = [
    'child_text',
    'child_value'
]


def find_element(
        xml_tag_or_string: Union[str, BeautifulSoup, Tag], element_name) -> Tag:
    """
    Find the element with that name in the string or Tag
    :param xml_tag_or_string: either an exml tag or string containing xml
    :param element_name: The name of the element to find
    :return: An element
    """
    if isinstance(xml_tag_or_string, Tag):
        return xml_tag_or_string.find(element_name, recursive=False)
    elif isinstance(xml_tag_or_string, str) and "<" in xml_tag_or_string:
        soup: BeautifulSoup = BeautifulSoup(xml_tag_or_string, features="xml")
        return soup.find(element_name, recursive=False)


def child_text(parent: Tag, child: str) -> Optional[str]:
    """
    Get the text of the child element if it exists or None
    :param parent: The parent tag
    :param child: The name of the child element
    :return: the text of the child element if it exists or None
    """
    el = parent.find(child, recursive=False)
    if el and isinstance(el.text, str) and el.text.strip() not in ("N/A", "000000000", "XXXX"):
        return el.text.strip()
    return None


def child_value(parent: Tag, child: str, key: str = "value") -> Optional[str]:
    """
    Get the value of the child element if it exists or None
    :param parent: The parent tag
    :param child: The name of the child element
    :param key: The key of the child element's attributes
    :return: the value of the child element attribute if it exists or None
    """
    el = parent.find(child, recursive=False)
    if el:
        value = el.attrs.get(key)
        if isinstance(value, str) and value.strip() not in ("N/A", "000000000", "XXXX"):
            return value
    return None
