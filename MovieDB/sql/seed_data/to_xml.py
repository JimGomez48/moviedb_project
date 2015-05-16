import xml.etree.cElementTree as ET
import csv
import os

def main():
    orig = 'actor1.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'field', name='sex').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'field', name='dob').text = str(tokens[4]).decode('utf8')
            ET.SubElement(row, 'field', name='dod').text = str(tokens[5]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'actor2.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'field', name='sex').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'field', name='dob').text = str(tokens[4]).decode('utf8')
            ET.SubElement(row, 'field', name='dod').text = str(tokens[5]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'actor3.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'field', name='sex').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'field', name='dob').text = str(tokens[4]).decode('utf8')
            ET.SubElement(row, 'field', name='dod').text = str(tokens[5]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'director.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='last').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='first').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'field', name='dob').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'field', name='dod').text = str(tokens[4]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'movie.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='title').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='year').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'field', name='rating').text = str(tokens[3]).decode('utf8')
            ET.SubElement(row, 'field', name='company').text = str(tokens[4]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'movieactor1.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='actor_id').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'field', name='role').text = str(tokens[3]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'movieactor2.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='actor_id').text = str(tokens[2]).decode('utf8')
            ET.SubElement(row, 'field', name='role').text = str(tokens[3]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'moviedirector.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='director_id').text = str(tokens[2]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')
    orig = 'moviegenre.del'
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'field', name='id').text = str(tokens[0]).decode('utf8')
            ET.SubElement(row, 'field', name='movie_id').text = str(tokens[1]).decode('utf8')
            ET.SubElement(row, 'field', name='genre').text = str(tokens[2]).decode('utf8')
        tree = ET.ElementTree(root)
        tree.write(orig[:-3] + 'xml')


if __name__ == '__main__':
    main()
