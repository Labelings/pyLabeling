# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from datetime import datetime

import numpy as np
from scipy.ndimage import rotate
from tifffile import imread

import Labeling as lb
from line_profiler import LineProfiler

result = np.zeros((512, 512))
resolution = (512, 512)


def read_img():
    files = []
    for i in range(1, 6):
        for j in range(1, 5):
            files.append("C:/mpicbg/metaseg_data/Euclidean_squared_distance/000/diverse" + str(i) + "/sweep_" + str(
                j) + "_mask.tif")
    images = imread(files)
    return images


def test1():
    # setting up the images for second example
    example2_images = []
    example2_images.append(np.invert(imread("tutorial/up_big.tif")))
    example2_images[0][example2_images[0] > 0] = 130
    example2_images.append(
        rotate(np.transpose(np.flip(example2_images[0]).copy()), angle=45, reshape=False, mode="constant", cval=0))
    example2_images[1][example2_images[1] > 0] = 131
    example2_images.append(np.transpose(np.flip(example2_images[0]).copy()))
    example2_images[2][example2_images[2] > 0] = 132
    example2_images.append(rotate(np.flip(example2_images[0]).copy(), angle=45, reshape=False, mode="constant", cval=0))
    example2_images[3][example2_images[3] > 0] = 133
    example2_images.append(np.flip(example2_images[0]).copy())
    example2_images[4][example2_images[4] > 0] = 134
    example2_images.append(
        rotate(np.transpose(example2_images[0]).copy(), angle=45, reshape=False, mode="constant", cval=0))
    example2_images[5][example2_images[5] > 0] = 135
    example2_images.append(np.transpose(example2_images[0]).copy())
    example2_images[6][example2_images[6] > 0] = 136
    example2_images.append(rotate(example2_images[0], angle=45, reshape=False, mode="constant", cval=0))
    example2_images[7][example2_images[7] > 0] = 137

    merger = lb.Labeling.fromValues(np.zeros((512, 512), np.int32))
    merger.iterate_over_images(example2_images, [str(int) for int in list(range(1, len(example2_images) + 1))])
    img, labeling2 = merger.save_result("example2")



def test4():
    global result, img
    a = np.zeros((4, 4), np.int32)
    a[:2] = 1
    example1_images = []
    example1_images.append(a)
    #example1_images.append(a.copy())
    b = a.copy()
    example1_images.append(np.flip(b.transpose()))
    c = a.copy()
    example1_images.append(np.flip(c))
    d = a.copy()
    example1_images.append(d.transpose())
    e = np.zeros((4, 4), np.int32)
    e[1:3, 1:3] = 1
    example1_images.append(e)
    # Initialize the merger with the first image. This can also be an empty image of zeros in the correct shape
    merger = lb.Labeling.fromValues(first_image=np.zeros((4,4), dtype="int32"))
    merger2 = lb.Labeling.fromValues(first_image=np.zeros((4, 4), dtype="int32"))
    result = merger2.add_segments(example1_images[0], (0, 0), source_id=str(0))
    result = merger2.add_segments(example1_images[1], (0, 0), source_id=str(1))
    result = merger2.add_segments(example1_images[2], (0, 0), source_id=str(2))
    result = merger2.add_segments(example1_images[3], (0, 0), source_id=str(3))
    result = merger2.add_segments(example1_images[4], (0, 0), source_id=str(4))

    merger.iterate_over_images(example1_images,['a','b','c','d','e'])

    img, labeling = merger.save_result("example1_1", True)
    img, labeling = merger2.save_result("example1", True)
    print(img)
    print(vars(labeling))
    # add_anything(data, (x,y,z):Tuple, merge:dict=None)
    # returns dict of actual labels dif


def test3():
    # init
    images = read_img()
    patch_size = 64
    # profiler = LineProfiler()
    start = datetime.now()
    # initialize the merger
    merger = lb.Labeling.fromValues(first_image=np.zeros(images[0].shape, np.int32))
    # profiler.add_function(lb.Labeling.add_segments)
    # profiler.add_function(lb.Labeling.iterate_over_images)
    # iterate over all images
    i = 0
    for image in images:
        # start position
        x, y = 0, 0
        # create 64x64 patches from each image
        patches = np.vsplit(image, int(image.shape[0] / patch_size))
        patches = [np.hsplit(seg, int(image.shape[1] / patch_size)) for seg in patches]
        for patchList in patches:
            for patch in patchList:
                # print(x,y)
                # profiler.runcall(merger.add_segments, patch, (x,y))
                merger.add_segments(patch=patch, position=(x, y), source_id=str(i))
                y += patch_size
            y = 0
            x += patch_size
        i +=1
    img, labeling = merger.save_result("big_img", True)
    print(datetime.now() - start)
    print(vars(labeling))

    temp ={}
    for key,value in labeling.labelSets.items():
        if value["source"] not in temp:
            temp[value["source"]] = 1
        else:
            temp[value["source"]] += 1
    print(temp)
    print([a/len(labeling.labelSets) for a in temp.values()])
    print(sum([a / len(labeling.labelSets) for a in temp.values()]))
    # profiler.print_stats()
    # profiler.dump_stats("profiling.lprof")


if __name__ == '__main__':

    test1()
    #test3()
    #test4()
