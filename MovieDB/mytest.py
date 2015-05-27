import os
import xml.etree.cElementTree as ET

# from django.db import models

from moviedb_project.settings import BASE_DIR
# from MovieDB.models import Actor


def main():
    print 'loading seed data...'
    SEED_DIR = os.path.join(BASE_DIR, 'MovieDB/sql/seed_data/xml/')

    tree = ET.parse(SEED_DIR + 'actor1.xml')
    root = tree.getroot()
    i = 0
    for row in root:
        print row.find('id').text, row.find('last').text, row.find('first').text, row.find('sex').text, row.find('dob').text, row.find('dod').text
        i += 1
        if i > 10:
            break



if __name__ == '__main__':
    main()