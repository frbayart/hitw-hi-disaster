# TENSORFLOW
## Installation
```
pip3 install --upgrade pip
pip3 install tensorflow
pip3 install numpy
```

Optimized binary
- https://github.com/lakshayg/tensorflow-build/

```
macos> pip3 install --ignore-installed --upgrade "https://github.com/lakshayg/tensorflow-build/releases/download/tf1.9.0-macos-py27-py36/tensorflow-1.9.0-cp36-cp36m-macosx_10_13_x86_64.whl"
```

## Documentation
### SAVE AND RESTORE MODELS
- https://stackabuse.com/tensorflow-save-and-restore-models/
- http://cv-tricks.com/tensorflow-tutorial/save-restore-tensorflow-models-quick-complete-tutorial/
- https://www.tensorflow.org/serving/docker
- http://vict0rsch.github.io/2018/05/17/restore-tf-model-dataset/

## Output

Sortie: Array de Rectangles
Point = Array [ X1, Y1, X2, Y2,  Score]
e.g.
Ne contiendra que les prédictions positives.

```
[
[ 200, 300, 225, 325,  0.97],
[ 400, 300, 420, 320, 0.88]
]
```
