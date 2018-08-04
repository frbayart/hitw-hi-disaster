#!/usr/bin/env python3

import matplotlib.image as mpimg
import tensorflow as tf
import numpy as np

img = mpimg.imread('before.png')

print(img.shape)

img1 = img.reshape(-1, 4)[:, 0:3]
img1 = np.insert(img1, 3, values=0, axis=1)
img1 = np.insert(img1, 4, values=1, axis=1)
#[R, G, B, 0, 1]
print(img1.shape)

#print(img1[:, 0:3].shape)

img001 = mpimg.imread('001.png').reshape(-1, 4)[:, 0:3]
img002 = mpimg.imread('002.png').reshape(-1, 4)[:, 0:3]
img003 = mpimg.imread('003.png').reshape(-1, 4)[:, 0:3]
img004 = mpimg.imread('004.png').reshape(-1, 4)[:, 0:3]
img005 = mpimg.imread('005.png').reshape(-1, 4)[:, 0:3]
img006 = mpimg.imread('006.png').reshape(-1, 4)[:, 0:3]
img007 = mpimg.imread('007.png').reshape(-1, 4)[:, 0:3]
img008 = mpimg.imread('008.png').reshape(-1, 4)[:, 0:3]
img009 = mpimg.imread('009.png').reshape(-1, 4)[:, 0:3]
img010 = mpimg.imread('010.png').reshape(-1, 4)[:, 0:3]
img011 = mpimg.imread('011.png').reshape(-1, 4)[:, 0:3]

img2 = np.concatenate((img001, img002, img003, img004, img005, img006, img007, img008, img009, img010, img011)).reshape(-1, 4)[:, 0:3]
img2 = np.insert(img2, 3, values=1, axis=1)
img2 = np.insert(img2, 4, values=0, axis=1)
img2 = np.repeat(img2, 20, axis=0)
#[R, G, B, 1, 0]
print(img2.shape)

data = np.concatenate((img1, img2))

init = tf.global_variables_initializer()

features = data[:, 0:3]
labels   = data[:, 3:]

########################################################

# Parameters
learning_rate = 0.001
training_epochs = 1
batch_size = 10000
display_step = 1

# Network Parameters
n_hidden_1 = 20 # 1st layer number of neurons
n_hidden_2 = 20 # 2nd layer number of neurons
n_input = 3 # MNIST data input (img shape: 28*28)
n_classes = 2 # MNIST total classes (0-9 digits)

# tf Graph input
#X = tf.placeholder("float", [None, n_input])
#Y = tf.placeholder("float", [None, n_classes])

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}


# Create model
def multilayer_perceptron(x):
    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer


features_placeholder = tf.placeholder(features.dtype, features.shape)
labels_placeholder = tf.placeholder(labels.dtype, labels.shape)

dataset = tf.data.Dataset.from_tensor_slices((features_placeholder, labels_placeholder)).shuffle(buffer_size=batch_size).batch(batch_size)
# [Other transformations on `dataset`...]
iterator = dataset.make_initializable_iterator()

x, y = iterator.get_next()

# Construct model
logits = multilayer_perceptron(features_placeholder)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(
    logits=logits, labels = labels_placeholder))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# Initializing the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
#	  initialize variables
  sess.run(init)
  sess.run(iterator.initializer, feed_dict={features_placeholder: features, labels_placeholder: labels})
    #print(sess.run([x, y]))
  # Training cycle
  for epoch in range(training_epochs):
    avg_cost = 0.
    total_batch = int(features.shape[0]/batch_size)
    total_batch = 10
    # Loop over all batches
    for i in range(total_batch):    
      _, c = sess.run([train_op, loss_op], feed_dict={features_placeholder: features, labels_placeholder: labels})
      avg_cost += c / total_batch
      #print("Batch #", '%04d' % i)
    print("Epoch:", '%04d' % (epoch+1), "cost={:.9f}".format(avg_cost))
  # Test model
  pred = tf.nn.softmax(logits)  # Apply softmax to logits
  correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(labels_placeholder, 1))
  # Calculate accuracy
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
  print("Accuracy:", accuracy.eval({features_placeholder: features, labels_placeholder: labels}))
  tf.saved_model.simple_save(sess,
            './model',
            inputs={"features_placeholder": features_placeholder,
                    "logits": logits},
            outputs={"pred": pred})

#  for epoch in range(training_epochs):

###
###    # Training cycle
###    for epoch in range(training_epochs):
###        avg_cost = 0.
###        total_batch = int(features.shape[0]/batch_size)
###        # Loop over all batches
###        for i in range(total_batch):
###        	  print(i)
###        	  xx = iterator.get_next()
###        	  print(xx)
###            #batch_x, batch_y = iterator.get_next()
###            #features_placeholder.next_batch(batch_size), labels.next_batch(batch_size)
###            #print(batch_x.dtype)
##            # Run optimization op (backprop) and cost op (to get loss value)
##            _, c = sess.run([train_op, loss_op], feed_dict={X: batch_x,
##                                                            Y: batch_y})
##            # Compute average loss
##            avg_cost += c / total_batch
##        # Display logs per epoch step
##        if epoch % display_step == 0:
##            print("Epoch:", '%04d' % (epoch+1), "cost={:.9f}".format(avg_cost))
##    print("Optimization Finished!")
##
##    # Test model
##    pred = tf.nn.softmax(logits)  # Apply softmax to logits
##    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
##    # Calculate accuracy
##    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
##    #print("Accuracy:", accuracy.eval({X: mnist.test.images, Y: mnist.test.labels}))
