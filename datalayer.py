#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# TRIPLET LOSS
# Copyright (c) 2015 Pinguo Tech.
# Written by David Lu
# --------------------------------------------------------

"""The data layer used during training to train the network.
   This is a example for online triplet selection
   Each minibatch contains a set of archor-positive pairs, random select negative exemplar
"""

import caffe
import numpy as np
from numpy import *
import yaml
from sampledata import sampledata
import random
import cv2
from blob import prep_im_for_blob, im_list_to_blob
import config
import datetime

class DataLayer(caffe.Layer):
    """Sample data layer used for training."""    
        
    
    def _get_next_minibatch(self):
        # num_images = self._batch_size
        # Sample to use for each image in this batch
        sample = []
        if self._index >= len(self.data_container._sample):
            self._index = 0
        archor = self.data_container._sample[self._index]
        archor_comm_type = archor.split('/')[0]
        self._index = self._index + 1
        while len(sample) < self._triplet:
            sample.append(archor)
        #print 'Done anchor. Pick positive...'
        # Sample positive samples
        while len(sample) < self._triplet*2:
            if len(self.data_container._sample_commodity[archor_comm_type]) == 1:
                sample.append(self.data_container._sample_commodity[archor_comm_type][0])
            else:
                picindex = random.randint(0,len(self.data_container._sample_commodity[archor_comm_type])-1)
                while self.data_container._sample_commodity[archor_comm_type][picindex] == archor:
                    picindex = random.randint(0,len(self.data_container._sample_commodity[archor_comm_type])-1)
                sample.append(self.data_container._sample_commodity[archor_comm_type][picindex])
        # print 'Done positive. Pick negative...'
        # Sample negative samples
        while len(sample) < self._triplet*3:      
            rand = random.randint(0,len(self.data_container._sample_commodity)-1)
            nega_comm_type = self.data_container._sample_commodity.keys()[rand]
            if archor_comm_type == nega_comm_type :
                index = max(0,rand - 1)
                if index == 0 :
                    index = rand + 1
                else:
                    index = rand - 1
                nega_comm_type = self.data_container._sample_commodity.keys()[index]
            picindex = random.randint(0,len(self.data_container._sample_commodity[nega_comm_type])-1)
            if (self.data_container._sample_commodity[nega_comm_type][picindex]) not in sample:
                sample.append(self.data_container._sample_commodity[nega_comm_type][picindex])
        im_blob,labels_blob = self._get_image_blob(sample)
        # print 'length of sample:', len(sample)
        blobs = {'data': im_blob, 'labels': labels_blob}
        # print np.shape(blobs["data"]),blobs["labels"]
        return blobs

    def _get_image_blob(self,sample):
        im_blob = []
        labels_blob = []
        for i in range(self._batch_size):
            im = cv2.imread(config.IMAGEPATH+sample[i])
            comm_type = sample[i].split('/')[0]
            # print str(i)+':'+personname+','+str(len(sample))
            labels_blob.append(self.data_container._sample_label[comm_type])
            im = prep_im_for_blob(im)
            
            im_blob.append(im)

        # Create a blob to hold the input images
        blob = im_list_to_blob(im_blob)
        return blob,labels_blob

    def setup(self, bottom, top):
        """Setup the RoIDataLayer."""
        # parse the layer parameter string, which must be valid YAML
        layer_params = yaml.load(self.param_str)    
        self._batch_size = config.BATCH_SIZE
        self._triplet = self._batch_size/3
        assert self._batch_size % 3 == 0
        self._name_to_top_map = {
            'data': 0,
            'labels': 1}

        self.data_container =  sampledata() 
        self._index = 0

        # data blob: holds a batch of N images, each with 3 channels
        # The height and width (100 x 100) are dummy values
        top[0].reshape(self._batch_size, 3, 224, 224)

        top[1].reshape(self._batch_size)

    def forward(self, bottom, top):
        """Get blobs and copy them into this layer's top blob vector."""
        blobs = self._get_next_minibatch()

        for blob_name, blob in blobs.iteritems():
            top_ind = self._name_to_top_map[blob_name]
            # Reshape net's input blobs
            #top[top_ind].reshape(*(blob.shape))
            # Copy data into net's input blobs
            top[top_ind].data[...] = blob

    def backward(self, top, propagate_down, bottom):
        """This layer does not propagate gradients."""
        pass

    def reshape(self, bottom, top):
        """Reshaping happens during the call to forward."""
        pass

class TestBlobFetcher():
    """Experimental class for prefetching blobs in a separate process."""
    
    def __init__(self):
        self._batch_size = 30
        self.data_container =  sampledata() 
        self._index = 0
        self._triplet = self._batch_size/3

    def _get_next_minibatch(self):
        # num_images = self._batch_size
        # Sample to use for each image in this batch
        if self._index >= len(self.data_container._sample):
            self._index = 0  
        sample = []
        archor = self.data_container._sample[self._index]
        archor_comm_type = archor.split('/')[0]
        self._index = self._index + 1 
        while len(sample) < self._triplet:
            sample.append(archor)
        # Sample positive samples
        while len(sample) < self._triplet*2:
            if len(self.data_container._sample_commodity[archor_comm_type]) == 1:
                sample.append(self.data_container._sample_commodity[archor_comm_type][0])
            else:
                picindex = random.randint(0,len(self.data_container._sample_commodity[archor_comm_type])-1)
                while self.data_container._sample_commodity[archor_comm_type][picindex] == archor:
                    picindex = random.randint(0,len(self.data_container._sample_commodity[archor_comm_type])-1)
                sample.append(self.data_container._sample_commodity[archor_comm_type][picindex])
        # Sample negative samples
        while len(sample) < self._triplet*3:     
            rand = random.randint(0,len(self.data_container._sample_commodity)-1)
            nega_comm_type = self.data_container._sample_commodity.keys()[rand]
            if archor_comm_type == nega_comm_type :
                index = max(0,rand - 1)
                if index == 0 :
                    index = rand + 1
                else:
                    index = rand - 1
                nega_comm_type = self.data_container._sample_commodity.keys()[index]
            picindex = random.randint(0,len(self.data_container._sample_commodity[nega_comm_type])-1)
            if (self.data_container._sample_commodity[nega_comm_type][picindex]) not in sample:
                sample.append(self.data_container._sample_commodity[nega_comm_type][picindex])
        # print 'sample:', sample
        im_blob,labels_blob = self._get_image_blob(sample)

        blobs = {'data': im_blob, 'labels': labels_blob}
        
        return blobs

    def _get_image_blob(self,sample):
        im_blob = []
        labels_blob = []
        for i in range(len(sample)):
            im = cv2.imread(config.IMAGEPATH+sample[i])
            comm_type = sample[i].split('/')[0]
            #print str(i)+':'+personname+','+str(len(sample))
            labels_blob.append(self.data_container._sample_label[comm_type])
            im = prep_im_for_blob(im)
            
            im_blob.append(im)

        # Create a blob to hold the input images
        blob = im_list_to_blob(im_blob)
        return blob,labels_blob

if __name__ == '__main__':

    #print data_container._sample
    test = TestBlobFetcher()
    for i in range(10):
        blob = test._get_next_minibatch()
        print str(i),np.shape(blob["data"]),blob["labels"]#,blob 


