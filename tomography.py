from math import *
from bresenham import bresenham
from measure import measure
from multiprocessing import Process, Manager, Lock
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
from skimage import color, io
import ctypes as c
import time

def image_properties(img):
    (img_width, img_height) = (img.shape[0], img.shape[1])
    r = (sqrt(img_width ** 2 + img_height ** 2) / 2)
    return img_width, img_height, r


def radon(img, detectors_n, alpha, d, nrOfThreads, mask, is_iterative):
    (img_width, img_height, r) = image_properties(img)
    print(img_height, img_width)
    iter_n = floor(360 / alpha)

    measures = Manager().list([0] *iter_n)
    mp_arr = mp.Array(c.c_double, detectors_n * iter_n)  # shared, can be used from multiple processes

    # then in each new process create a new numpy array using:
    arr = np.frombuffer(mp_arr.get_obj())  # mp_arr and arr share the same memory
    # make it two-dimensional
    sinogram = arr.reshape((iter_n, detectors_n))  # b and arr share the same memory

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    ax1.imshow(img, cmap='gray')
    ax3.imshow(np.zeros((img_width, img_height)), cmap='gray')
    plt.pause(0.0001)

    # new_img = np.zeros((img_width, img_height))
    # ax2.imshow(new_img, cmap='gray')
    # plt.show(block=False)

    iterationsPerThread = int(iter_n/nrOfThreads)

    processes=[]
    for threadNumber in range(nrOfThreads):
        p = Process(target=getAndInsertSinogramVec, args=[alpha, d, detectors_n, img, img_height, img_width, threadNumber, measures, r, sinogram, iterationsPerThread, mask])
        p.start()
        processes.append(p)


    while any(p.is_alive() for p in processes):
        if is_iterative:
            arr = np.asarray(sinogram)
            arr = np.transpose(arr)
            time.sleep(0.05)
            fig.canvas.flush_events()
            ax2.imshow(arr, cmap='gray')
            # im.set_data(arr)

            # plt.show(block=False)
            plt.pause(0.0001)

    sinogram = normalize_sinogram(sinogram)

    arr = np.asarray(sinogram)
    arr = np.transpose(arr)
    ax2.imshow(arr, cmap='gray')
    plt.pause(0.0001)

    return sinogram, measures, fig

def normalize_sinogram(sinogram):
    mini, maxi = sinogram.min(), sinogram.max()
    for i in range(len(sinogram)):
        for j in range(len(sinogram[0])):
            sinogram[i][j] = (sinogram[i][j] - mini)/(maxi - mini)
    return sinogram

def getAndInsertSinogramVec(alpha, d, detectors_n, img, img_height, img_width, threadNumber, measures, r, sinogram, iterationsPerThread, mask):
    start = threadNumber*iterationsPerThread
    for iteration in range(start, start + iterationsPerThread):
        measuration, sinogram_vec = getSinogramVec(alpha, d, detectors_n, img, img_height, img_width, iteration, r, mask)

        for i in  range(len(sinogram_vec)):
            sinogram[iteration][i] = sinogram_vec[i]
        #measures[iteration] = measuration


def applyFilter(sinogram_vec, mask):
    copy = sinogram_vec.copy()
    for i in range(1, len(sinogram_vec)-1):
        copy[i] = sinogram_vec[i]*mask[1] + sinogram_vec[i-1]*mask[0] + sinogram_vec[i+1]*mask[2]
    return copy

def getSinogramVec(alpha, d, detectors_n, img, img_height, img_width, iteration, r, mask):
    print(iteration)
    measuration = measure(iteration)
    iter_alpha = iteration * alpha
    xE = floor(r * cos(radians(iter_alpha)) + img_width / 2)
    yE = floor(r * sin(radians(iter_alpha)) + img_height / 2)
    sinogram_vec = []
    for i in range(detectors_n):
        xD = floor(r * cos(radians(iter_alpha + 180 - (d / 2) + i * d / (detectors_n - 1))) + img_width / 2)
        yD = floor(r * sin(radians(iter_alpha + 180 - (d / 2) + i * d / (detectors_n - 1))) + img_height / 2)
        ray = bresenham(xE, yE, xD, yD)
        measuration.rays.append(ray)
        sinogram_vec.append(get_sinogram_value(ray, img, img_width, img_height))
    sinogram_vec = applyFilter(sinogram_vec, mask)
    return measuration, sinogram_vec


def get_sinogram_value(ray,image, img_width, img_height):
    (points_sum, points_n) = (0, 0)
    for point in ray:
        if 0 <= point[0] < img_width and 0 <= point[1] < img_height:
            points_n += 1
            points_sum += image[point[0]][point[1]]
    if points_n > 0:
        return points_sum / points_n
    return 0


def inverse_radon(img, sinogram, detectors_n, alpha, d, nrOfThreads, fig, is_iterative):
    (img_width, img_height, r) = image_properties(img)
    mp_arr = mp.Array(c.c_double, img_width*img_height)  # shared, can be used from multiple processes
    mp_arr2 = mp.Array(c.c_double, img_width*img_height)  # shared, can be used from multiple processes
    mp_arr3 = mp.Array(c.c_double, img_width*img_height)  # shared, can be used from multiple processes

    # then in each new process create a new numpy array using:
    arr = np.frombuffer(mp_arr.get_obj())  # mp_arr and arr share the same memory
    arr2 = np.frombuffer(mp_arr2.get_obj())  # mp_arr and arr share the same memory
    arr3 = np.frombuffer(mp_arr3.get_obj())  # mp_arr and arr share the same memory

    # make it two-dimensional
    normalized_img = arr.reshape((img_width, img_height))  # b and arr share the same memory
    result_img = arr2.reshape((img_width, img_height))  # b and arr share the same memory
    result_counter = arr3.reshape((img_width, img_height))  # b and arr share the same memory

    detectors_n = len(sinogram[0])
    iter_n = len(sinogram)
    print("INVERSE RADON")

    iterationsPerThread = int(iter_n/nrOfThreads)
    processes=[]

    index=0

    # image = color.rgb2gray(io.imread('picbrain.jpg'))
    plt.subplot(313)
    # im = plt.imshow(image, cmap='gray')
    # plt.show(block=False)
    # plt.pause(0.0001)
    lock = Lock()
    for thread_num in range(nrOfThreads):
        index=thread_num*iterationsPerThread
        p = Process(target=CreateImage, args=[alpha, d, detectors_n, img_height, img_width, index, iterationsPerThread, normalized_img, r, result_counter, result_img, sinogram, lock])
        p.start()
        processes.append(p)

    while any(p.is_alive() for p in processes):
        if is_iterative:
            updateImage(fig, normalized_img)

    updateImage(fig, normalized_img)

    # plt.waitforbuttonpress()
    return normalized_img


def updateImage(fig, normalized_img):
    time.sleep(0.05)
    # lock.acquire()
    # im.set_data(normalized_img)
    # plt.draw()
    plt.imshow(normalized_img, cmap='gray')
    fig.canvas.flush_events()
    # lock.release()
    plt.pause(0.0001)


def CreateImage(alpha, d, detectors_n, img_height, img_width, index, iterationsPerThread, normalized_img, r,
                result_counter, result_img, sinogram, lock):
    for i in range(index, index + iterationsPerThread):
        print(i)
        iter_alpha = i * alpha
        xE = floor(r * cos(radians(iter_alpha)) + img_width / 2)
        yE = floor(r * sin(radians(iter_alpha)) + img_height / 2)
        for detector in range(detectors_n):
            xD = floor(r * cos(radians(iter_alpha + 180 - (d / 2) + detector * d / (detectors_n - 1))) + img_width / 2)
            yD = floor(r * sin(radians(iter_alpha + 180 - (d / 2) + detector * d / (detectors_n - 1))) + img_height / 2)
            ray = bresenham(xE, yE, xD, yD)
            for point in ray:
                if 0 <= point[0] < img_width and 0 <= point[1] < img_height:
                    #lock.acquire()
                    result_counter[point[0]][point[1]] += 1
                    result_img[point[0]][point[1]] += sinogram[i][detector]
                    normalized_img[point[0]][point[1]] = result_img[point[0]][point[1]] / result_counter[point[0]][point[1]]
                    #lock.release()
