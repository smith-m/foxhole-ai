# foxhole-ai

runs at lowest Foxhole graphics settings with 1024 x 768 resolution

# image detection guidance
https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10

# Training Setup
This is way more complicated than it needs to be.

https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html

# Training
1. to update labels.csv used by training records run
py -m image_recognition.xml_to_csv
2. update unique labels in CLASS_MAP in
image_recognition/generate_tfrecord.py
3. to create training records
py -m image_recognition.generate_tfrecord --csv_input=image_recognition/annotations/train_labels.csv --image_dir=images/screens/1024-768 --output_path=image_recognition/tfrecords/train.record --class_descriptor_output_path=image_recognition/tfrecords/class-descriptor.pbtxt
py -m image_recognition.generate_tfrecord --csv_input=image_recognition/annotations/test_labels.csv --image_dir=images/screens/1024-768 --output_path=image_recognition/tfrecords/test.record --class_descriptor_output_path=image_recognition/tfrecords/class-descriptor.pbtxt
4. train model
py -m object_detection.model_main --logstdserr --train_dir=image_recognition/tfrecords/ --pipeline_config_path=image_recognition/trained_models/faster_rcnn_inception_v2_foxhole/model.config
5. view training progress
tensorboard --logdir=image_recognition/tfrecords/
6. when satisfied with model generate trained inference graph
python -m object_detection.export_inference_graph --input_type image_tensor --pipeline_config_path image_recognition/trained_models/faster_rcnn_inception_v2_coco/pipeline.config --trained_checkpoint_prefix model/model.ckpt-200
000 --output_directory image_recognition/inference_graph
7. run live image detection. your primary monitor must be set to foxhole and on 1024x768 res.
py -m image_recognition.game_image_detection
