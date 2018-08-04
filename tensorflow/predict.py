#!/usr/bin/env python3

import matplotlib.image as mpimg
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants

import numpy as np

### read an image 
img = mpimg.imread('after.png')
img1 = img.reshape(-1, 4)[:, 0:3]
print(img1.shape)

export_dir = './model'

sess = tf.InteractiveSession()
graph = tf.get_default_graph()

tf.saved_model.loader.load(sess, [tag_constants.SERVING], export_dir)

logits = graph.get_tensor_by_name("logits:0")
y = tf.nn.softmax(logits)
classs = y.eval({features_placeholder: img1})
print(classs)
sess.close()