from Globals import TRAIN_PATH, TEST_PATH, LABEL_PATH, BATCH_SIZE, CLASS_NUM, SEED
import csv
import tensorflow as tf
from preprocessing import inception_preprocessing
import matplotlib.pyplot as plt
import numpy as np


def parser(filename, label):
    # with tf.gfile.GFile(filename, 'rb') as f:
    img = tf.read_file(filename)  # f.read()
    img = tf.image.decode_image(img, channels=3)
    # NOTE the inception_preprocessing will convert image scale to [-1,1]
    img_resized = inception_preprocessing.preprocess_image(img, 224, 224, is_training=True)

    one_hot_label = tf.one_hot(label, CLASS_NUM, 1, 0)
    # NOTE label should expand axis
    one_hot_label = one_hot_label[tf.newaxis, tf.newaxis, :]
    return img_resized, one_hot_label


def get_filelist(fliepath):
    name_list = []
    label_list = []
    train_reader = csv.reader(open(fliepath, 'r'))
    for pa, la in train_reader:
        name_list.append(pa)
        label_list.append(int(la))
    return name_list, label_list


def create_dataset(namelist, labelist, batchsize, parserfn):
    # create the dataset from the list
    dataset = tf.data.Dataset.from_tensor_slices((tf.constant(namelist), tf.constant(labelist)))
    # parser the data set
    dataset = dataset.map(parserfn)
    # set batch size
    dataset = dataset.batch(batchsize)
    # repeat
    dataset = dataset.repeat()
    # shuffle
    dataset = dataset.shuffle(100, seed=SEED)
    # clac step for per epoch
    step_for_epoch = int(len(labelist)/BATCH_SIZE)
    return dataset, step_for_epoch


def create_iter(dataset):
    data_it = dataset.make_one_shot_iterator()
    # 定义个获取下一组数据的操作(operator)
    return data_it.get_next()