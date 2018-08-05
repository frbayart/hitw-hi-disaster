#!/usr/bin/env python3

import tensorflow as tf

with tf.Session(graph=tf.Graph()) as sess:
  graph = tf.get_default_graph()
  tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], './fuckitman/')
  X = graph.get_tensor_by_name("X:0")
  pred = graph.get_tensor_by_name("pred:0")

  print( sess.run([pred], {X: 5.0}) )
  print(pred)
