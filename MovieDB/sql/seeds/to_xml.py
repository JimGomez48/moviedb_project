#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xml.etree.cElementTree as ET
import csv
import os
from moviedb_project.settings import BASE_DIR

def main():
    IN_PATH = os.path.join(BASE_DIR, 'MovieDB/sql/seeds/csv')
    OUT_PATH = os.path.join(BASE_DIR, 'MovieDB/sql/seeds/xml')
    file_name = 'actor1.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'last').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'first').text = tokens[2].decode('utf-8')
            ET.SubElement(row, 'sex').text = tokens[3].decode('utf-8')
            ET.SubElement(row, 'dob').text = tokens[4].decode('utf-8')
            ET.SubElement(row, 'dod').text = tokens[5].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'actor2.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'last').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'first').text = tokens[2].decode('utf-8')
            ET.SubElement(row, 'sex').text = tokens[3].decode('utf-8')
            ET.SubElement(row, 'dob').text = tokens[4].decode('utf-8')
            ET.SubElement(row, 'dod').text = tokens[5].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'actor3.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'last').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'first').text = tokens[2].decode('utf-8')
            ET.SubElement(row, 'sex').text = tokens[3].decode('utf-8')
            ET.SubElement(row, 'dob').text = tokens[4].decode('utf-8')
            ET.SubElement(row, 'dod').text = tokens[5].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'director.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'last').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'first').text = tokens[2].decode('utf-8')
            ET.SubElement(row, 'dob').text = tokens[3].decode('utf-8')
            ET.SubElement(row, 'dod').text = tokens[4].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'movie.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'title').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'year').text = tokens[2].decode('utf-8')
            ET.SubElement(row, 'rating').text = tokens[3].decode('utf-8')
            ET.SubElement(row, 'company').text = tokens[4].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'movieactor1.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'mid').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'aid').text = tokens[2].decode('utf-8')
            ET.SubElement(row, 'role').text = tokens[3].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'movieactor2.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'mid').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'aid').text = tokens[2].decode('utf-8')
            ET.SubElement(row, 'role').text = tokens[3].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'moviedirector.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'mid').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'did').text = tokens[2].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)
    file_name = 'moviegenre.csv'
    orig = os.path.join(IN_PATH, file_name)
    with open(orig, 'r') as infile:
        root = ET.Element('root')
        for tokens in csv.reader(infile):
            row = ET.SubElement(root, 'row')
            ET.SubElement(row, 'id').text = tokens[0].decode('utf-8')
            ET.SubElement(row, 'mid').text = tokens[1].decode('utf-8')
            ET.SubElement(row, 'genre').text = tokens[2].decode('utf-8')
        tree = ET.ElementTree(root)
        tree.write(os.path.join(OUT_PATH, file_name[:-3] + 'xml'), encoding="UTF-8", xml_declaration=True)


if __name__ == '__main__':
    main()