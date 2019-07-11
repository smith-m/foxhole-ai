"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf
import logging

from PIL import Image
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('class_descriptor_output_path', '', 'Path to output labelmap proto descriptor')
flags.DEFINE_string('image_dir', '', 'Path to images')
FLAGS = flags.FLAGS

# TO-DO replace this with label map
CLASS_MAP = {
    'storage_box': 1,
    'scrap': 2,
    # 'sandbag': 5,
    'player': 3,
    'foxhole': 4,
    # 'crane': 6,
    # 'truck': 7,
    # 'scrapyard': 8,
    # 'watchtower': 9,
    # 'pillbox': 10,
    # 'scv': 11,
    # 'toggle_storage_box': 12,
    # 'observation_tower': 13,
    # 'wire': 14,
    # 'vehicle_operator_toggle': 15,
    # 'toggle_vehicle_operation': 15,
    # 'flatbed': 16,
    # 'fortified_wall': 17,
    # 'raised_gate': 18,
    # 'lowered_gate': 19,
    # 'fence': 20,
    # 'container': 21,
    # 'howitzer': 22,
    # 'tanker': 23,
    # 'motorcycle': 24,
    # 'colonial': 25,
    # 'backpack': 26,
    # 'dead_player': 27,
    # 'use_gate': 28,
    'other':5
}

CLASS_TO_TEXT_MAP = {value: key for key, value in CLASS_MAP.items()}


def class_text_to_int(row_label):
    return CLASS_MAP.get(row_label, 5)


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def class_map_to_labelmap(path):
    with tf.io.gfile.GFile(path, 'w') as fid:
        for name, id in CLASS_MAP.items():
            fid.write(
                f"""item {{
    id: {id}
    name: '{name}'             
}}\n\n"""
            )


def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_png = fid.read()
    encoded_png_io = io.BytesIO(encoded_png)
    image = Image.open(encoded_png_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'png'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        logging.info(f"{CLASS_TO_TEXT_MAP[class_text_to_int(row['class'])]}: {class_text_to_int(row['class'])}: {row['class']} ")

        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(CLASS_TO_TEXT_MAP[class_text_to_int(row['class'])].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),
        'image/width': tf.train.Feature(int64_list=tf.train.Int64List(value=[width])),
        'image/filename': tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename])),
        'image/source_id': tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename])),
        'image/encoded': tf.train.Feature(bytes_list=tf.train.BytesList(value=[encoded_png])),
        'image/format': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_format])),
        'image/object/bbox/xmin': tf.train.Feature(float_list=tf.train.FloatList(value=xmins)),
        'image/object/bbox/xmax': tf.train.Feature(float_list=tf.train.FloatList(value=xmaxs)),
        'image/object/bbox/ymin': tf.train.Feature(float_list=tf.train.FloatList(value=ymins)),
        'image/object/bbox/ymax': tf.train.Feature(float_list=tf.train.FloatList(value=ymaxs)),
        'image/object/class/text': tf.train.Feature(bytes_list=tf.train.BytesList(value=classes_text)),
        'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=classes)),
    }))
    return tf_example


def main(_):
    writer = tf.io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))

    class_descriptor_output_path = os.path.join(os.getcwd(), FLAGS.class_descriptor_output_path)
    class_map_to_labelmap(class_descriptor_output_path)

    print('Successfully created the class descriptor: {}'.format(class_descriptor_output_path))


if __name__ == '__main__':
    tf.compat.v1.app.run()
