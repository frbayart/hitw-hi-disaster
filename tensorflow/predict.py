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
# tested rectangle sizes

def suggestions(imgUrl, modelDir = './model100relu', sizes = (100, 50, 25, 12, 6)):


  ### read an image, TODO READ FROM DB?
  img = mpimg.imread(imgUrl)

  ### Format a array of normalized [R,G,B]
  img1 = img.reshape(-1, 4)[:, 0:3]
##  row_sums = img1.sum(axis=1)
##  img1 = img1 / row_sums[:, np.newaxis]
  img1 = preprocessing.normalize(img1, norm='l1')
  #print(img1.shape)

  ## Initialize a tensorflow session (sync computations)
  sess = tf.InteractiveSession()
  graph = tf.get_default_graph()
  
  ## restore the model and features/prediction tensors
  tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], modelDir)
  features_placeholder = graph.get_tensor_by_name("features_placeholder:0")
  pred = graph.get_tensor_by_name("pred:0")

  ## compute predictions on input image
  sess.run([pred], {features_placeholder: img1})
  kiki = pred.eval({features_placeholder: img1})



  ##for q in (1, 5, 10, 25, 50, 75, 90, 95, 99):
  ##  print("Quantile:", '%.2f' % q, " = ", '%.3f' % (np.percentile(kiki[:, 0], q)) )
  ##
  ##print(kiki.shape)

  ## extract the mud-class probability as output
  kiki = kiki.reshape(img.shape[0], img.shape[1], 2)[:, :, 0:1].reshape(img.shape[0], img.shape[1])
  #print(kiki.shape)
  
  #for q in (1, 5, 10, 25, 50, 75, 90, 95, 99):
  #  print("Quantile:", '%.2f' % q, " = ", '%.3f' % (np.percentile(kiki, q)) )

  ## mask to set score to zero for non-mud predicted pixels
  mask = (kiki >0.5)*1.0
  kiki = mask*kiki

  #### create the masked image for vizualization of predictions
  ##img = Image.fromarray(np.uint8(kiki*255), 'L')
  ##img.save('mud-pred.png')
  ##img.show()
  ##sess.close()

  ## inner function to average score over a predition tile
  def wscore(arr):
    return np.mean(arr, dtype=np.float32)

  ## variable aggregating regions of interest to ne returned
  output = np.empty([0, 5])

  ## kikiki is the predition scores image with masked regions to avoid overlaps
  kikiki = np.copy(kiki)
  ## zouzou is the image containing the suggestions rectangles for viz
  zouzou = (kiki > 2)*1.0

  ## for each window size,
  ## we slide by half window
  ## we avaluate if average score > 075 to define a suggestion square
  for ws in sizes:
  
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

## img = Image.fromarray(np.uint8(zouzou), 'L')
## img.show()
## img.save('mud-mask.png')
  return output


if __name__ == '__main__':
  print(suggestions('./bigafter.png', './model100relu', sizes = (100, 50, 25, 12, 6)))



