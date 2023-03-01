import cv2
from glob import glob
import numpy as np
import random
from sklearn.utils import shuffle
import pickle
import os


def pickle_images_labels():
    images_labels = []
    images = glob("gestures/*/*.jpg")
    images.sort()
    for image in images:
        print(image)
        label = image[image.find(os.sep) + 1 : image.rfind(os.sep)]
        img = cv2.imread(image, 0)
        images_labels.append((np.array(img, dtype=np.uint8), int(label)))
    return images_labels


images_labels = pickle_images_labels()
images_labels = shuffle(shuffle(shuffle(shuffle(images_labels))))
images, labels = zip(*images_labels)
print("Length of images_labels", len(images_labels))

test_images = images[:]
print("Length of test_images", len(test_images))
with open("test_images", "wb") as f:
    pickle.dump(test_images, f)
del test_images

test_labels = labels[:]
print("Length of test_labels", len(test_labels))
with open("test_labels", "wb") as f:
    pickle.dump(test_labels, f)
del test_labels
