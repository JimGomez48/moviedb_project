import os
import xml.etree.ElementTree as ET


def main():
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    tree = ET.parse(PROJECT_ROOT + '/data/navbar.xml')
    root = tree.getroot()
    for item in root:
        text = item.find('text')
        tooltip = item.find('tooltip')
        url = item.find('url')
        print(text.text, tooltip.text, url.text)

    a=3


if __name__ == '__main__':
    main()