# Triplet-Loss
Add the triplet loss layer and the corresponding data layer to an exited network(i.e., AlexNet) by Python
Running the new network on Caff

The implementation of the paper "FaceNet: A Unified Embedding for Face Recognition and Clustering"

These codes are the modified version of codes from the following author:
https://github.com/luhaofang/tripletloss

1. You should configure the Caffe first that the new layers written by Python can be added
Setup

Rebuild your caffe directory and makesure your python could find the added layers.

Go to your caffe root path:

cp Makefile.configexample Makefile.config
Open Makefile.config uncomment the line :

WITH_PYTHON_LAYER := 1
Then return to caffe root create build directory:

mkdir build
cd build
cmake ..
make all & make pycaffe

2. The "train.prototxt" shows an example how to add a layer in a model
