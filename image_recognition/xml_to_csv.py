import os

import glob

import pandas as pd

import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []

    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )

            xml_list.append(value)

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    xml_df = pd.DataFrame(xml_list, columns=column_name)

    return xml_df


def main():
    train_annotation_path = os.path.join(os.getcwd(), ('image_recognition/annotations/train/'))
    xml_df = xml_to_csv(train_annotation_path)
    xml_df.to_csv(('image_recognition/annotations/train_labels.csv'), index=None)

    test_annotation_path = os.path.join(os.getcwd(), ('image_recognition/annotations/test/'))
    xml_df = xml_to_csv(test_annotation_path)
    xml_df.to_csv(('image_recognition/annotations/test_labels.csv'), index=None)

    print('Successfully converted xml to csv.')


main()