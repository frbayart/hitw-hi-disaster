#!/usr/bin/env python3

import matplotlib.image as mpimg
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from PIL import Image
from sklearn import preprocessing
import numpy as np

#
# input image
# model directory
#

### read an image 
img = mpimg.imread('bigafter.png')
img1 = img.reshape(-1, 4)[:, 0:3]
img1 = preprocessing.normalize(img1, norm='l1')
print(img1.shape)

export_dir = './model/model'

sess = tf.InteractiveSession()
graph = tf.get_default_graph()

tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], './model100relu')
features_placeholder = graph.get_tensor_by_name("features_placeholder:0")
pred = graph.get_tensor_by_name("pred:0")
sess.run([pred], {features_placeholder: img1})
kiki = pred.eval({features_placeholder: img1})#sess.run([pred], {features_placeholder: img1})
for q in (1, 5, 10, 25, 50, 75, 90, 95, 99):
  print("Quantile:", '%.2f' % q, " = ", '%.3f' % (np.percentile(kiki[:, 0], q)) )

print(kiki.shape)

kiki = kiki.reshape(img.shape[0], img.shape[1], 2)[:, :, 0:1].reshape(img.shape[0], img.shape[1])
print(kiki.shape)

for q in (1, 5, 10, 25, 50, 75, 90, 95, 99):
  print("Quantile:", '%.2f' % q, " = ", '%.3f' % (np.percentile(kiki, q)) )

mask = (kiki >0.5)*1.0
zouzou = (kiki > 2)*1.0
kiki = mask*kiki

img = Image.fromarray(np.uint8(kiki*255), 'L')
img.save('mud-pred.png')
img.show()
sess.close()

def wscore(arr):
  return np.mean(arr, dtype=np.float32)

output = np.empty([0, 5])

kikiki = np.copy(kiki)
for ws in (100, 50, 25, 12, 6):

  kiki = np.copy(kikiki)
  ni = kiki.shape[0]//ws*2 -1
  nj = kiki.shape[1]//ws*2 -1
  
  for i in range(0, ni):
    for j in range(0, nj):
      x = i * ws//2
      y = j * ws//2
      score = wscore(kiki[x:x+ws, y:y+ws])
      newrow = [x,y,x+ws, y+ws, score]
      if (score > 0.75):
        output = np.vstack([output, newrow])
        kikiki[x:x+ws+1, y:y+ws+1] = 0
        zouzou[x:x+ws+1, y:y+ws+1] = 255

print(output)


img = Image.fromarray(np.uint8(zouzou), 'L')
img.show()
img.save('mud-mask.png')



