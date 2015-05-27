import xml.etree.cElementTree as ET
import csv
import os
from moviedb_project.settings import BASE_DIR

def main():
    # orig = 'actor1.del'
    PATH = os.path.join(BASE_DIR, 'MovieDB/sql/seed_data/csv')
    orig = os.path.join(PATH, 'actor1.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'sex').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'dob').text = str(tokens[4]).decode('utf8')
            ET.SubElement(row, 'dod').text = str(tokens[5]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'actor2.del'
    orig = os.path.join(PATH, 'actor2.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'sex').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'dob').text = str(tokens[4]).decode('utf8')
            ET.SubElement(row, 'dod').text = str(tokens[5]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'actor3.del'
    orig = os.path.join(PATH, 'actor3.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'sex').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'dob').text = str(tokens[4]).decode('utf8')
            ET.SubElement(row, 'dod').text = str(tokens[5]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'director.del'
    orig = os.path.join(PATH, 'director.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'dob').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'dod').text = str(tokens[4]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'movie.del'
    orig = os.path.join(PATH, 'movie.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'title').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'year').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'rating').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'company').text = str(tokens[4]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'movieactor1.del'
    orig = os.path.join(PATH, 'movieactor1.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'actor_id').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'role').text = str(tokens[3]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'movieactor2.del'
    orig = os.path.join(PATH, 'movieactor2.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'actor_id').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'role').text = str(tokens[3]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'moviedirector.del'
    orig = os.path.join(PATH, 'moviedirector.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'director_id').text = str(tokens[2]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    # orig = 'moviegenre.del'
    orig = os.path.join(PATH, 'moviegenre.del')
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'genre').text = str(tokens[2]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')


if __name__ == '__main__':
    main()
