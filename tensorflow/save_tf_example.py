#!/usr/bin/env python3

import tensorflow as tf

X = tf.placeholder(tf.float32, shape=(), name = "X")

pred = X * X
pred = tf.identity(pred, name="pred")
with tf.Session() as sess:
  print( sess.run([pred], {X: 100.0}) )
  print(pred)
  tf.saved_model.simple_save(sess,
                             './fuckitman/',
            inputs={"X": X},
            outputs={"pred": pred})