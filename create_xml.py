#! /usr/bin/env python3

import numpy as np
from lxml import etree as xml
from subprocess import check_call
from pathlib import Path
home = str(Path.home())

check_call('libreoffice -env:UserInstallation=file://' + home +
           '/.config/libreoffice-alt --convert-to csv:"Text - txt - csv (StarCalc)":59,34,0,1,1,0,true Sample_and_gear_types_AeN.xlsx', shell=True)

sheet = np.loadtxt("Sample_and_gear_types_AeN.csv", delimiter=';', dtype=str)
sheet = np.char.strip(sheet, '"')

# Remove
sheet = sheet[:, 1:-1]
print(sheet)
f = "Sample_and_gear_types_AeN.xml"
root = xml.Element('root')

for idx in range(len(sheet[0, :])):
    if not sheet[0, idx]:
        sheet[0, idx] = sheet[0, idx - 1]

for ii, el in enumerate(sheet[0, :]):
    if ii == 0 or el != sheet[0, ii - 1]:
        te = xml.SubElement(root, 'group', {'id': el})
    if sheet[1, ii]:
        group = xml.SubElement(te, 'gear', {'id': sheet[1, ii]})
        for row in range(3, len(sheet[:, ii])):
            if sheet[row, ii]:
                sample = xml.SubElement(
                    group, 'sample', {'id': sheet[row, ii + 1]})
                # Handle subsample flag
                if sheet[row, ii][:2] == '1,':
                    xml.SubElement(
                        sample, 'long_name').text = sheet[row, ii][3:]
                    xml.SubElement(sample, 'subsample').text = '1'
                else:
                    xml.SubElement(sample, 'long_name').text = sheet[row, ii]
                    xml.SubElement(sample, 'subsample').text = '0'

xml.ElementTree(root).write(
    f, method='xml', encoding='utf8', pretty_print=True, xml_declaration=True,)
