
# coding: utf-8

# In[1]:

from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
import matplotlib.pyplot as plt
import skimage.io as io
import pylab
import sys
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')

if len(sys.argv)<2:
    print 'usage: <val2014 or test2014>'
    exit()


# set up file names and pathes
dataDir='.'
dataType=sys.argv[1]
algName = 'soft'
annFile='%s/../captions_val2014.json'%(dataDir)
subtypes=['results', 'evalImgs', 'eval']
[resFile, evalImgsFile, evalFile]= ['%s/results/captions_%s_%s_%s.json'%(dataDir,dataType,algName,subtype) for subtype in subtypes]


# In[3]:

# create coco object and cocoRes object
coco = COCO(annFile)
cocoRes = coco.loadRes(resFile)


# In[4]:

# create cocoEval object by taking coco and cocoRes
cocoEval = COCOEvalCap(coco, cocoRes)

# evaluate on a subset of images by setting
# cocoEval.params['image_id'] = cocoRes.getImgIds()
# please remove this line when evaluating the full validation set
cocoEval.params['image_id'] = cocoRes.getImgIds()

# evaluate results
cocoEval.evaluate()


# In[5]:

# print output evaluation scores
for metric, score in cocoEval.eval.items():
    print '%s: %.3f'%(metric, score)


# In[6]:

# demo how to use evalImgs to retrieve low score result
evals = [eva for eva in cocoEval.evalImgs if eva['CIDEr']<30]
for i in xrange(5):
    print 'ground truth captions'
    imgId = evals[i]['image_id']
    annIds = coco.getAnnIds(imgIds=imgId)
    anns = coco.loadAnns(annIds)
    coco.showAnns(anns)

    print '\n'
    print 'generated caption (CIDEr score %0.1f)'%(evals[i]['CIDEr'])
    print '\n'
    annIds = cocoRes.getAnnIds(imgIds=imgId)
    anns = cocoRes.loadAnns(annIds)
    coco.showAnns(anns)

# In[8]:

# save evaluation results to ./results folder
json.dump(cocoEval.evalImgs, open(evalImgsFile, 'w'))
json.dump(cocoEval.eval,     open(evalFile, 'w'))

