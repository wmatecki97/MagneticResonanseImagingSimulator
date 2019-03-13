from math import *
from bresenham import bresenham
import numpy as np


def image_properties(img):
    (img_width, img_height) = (img.shape[0], img.shape[1])
    r = (sqrt(img_width ** 2 + img_height ** 2) / 2)
    return img_width, img_height, r


def radon(img, detectors_n, alpha, d):
    (img_width, img_height, r) = image_properties(img)
    print(img_height, img_width)
    iter_n = floor(360 / alpha)
    sinogram = []
    for iteration in range(iter_n):
        print(iteration)
        iter_alpha = iteration * alpha
        xE = floor(r * cos(radians(iter_alpha)) + img_width/2)
        yE = floor(r * sin(radians(iter_alpha)) + img_height/2)
        sinogram_vec = []
        for i in range(detectors_n):
            xD = floor(r * cos(radians(iter_alpha + 180 - (d / 2) + i * d / (detectors_n - 1))) + img_width / 2)
            yD = floor(r * sin(radians(iter_alpha + 180 - (d / 2) + i * d / (detectors_n - 1))) + img_height / 2)
            ray = bresenham(xE, yE, xD, yD)
            sinogram_vec.append(get_sinogram_value(ray, img))
        sinogram.append(sinogram_vec)
    return sinogram


def get_sinogram_value(ray, image):
    (img_width, img_height, _) = image_properties(image)
    (points_sum, points_n) = (0, 0)
    for point in ray:
        if 0 <= point[0] < img_width and 0 <= point[1] < img_height:
            points_n += 1
            points_sum += image[point[0]][point[1]]
    if points_n > 0:
        return points_sum / points_n
    return 0


def inverse_radon(img, sinogram, detectors_n, alpha, d):
    (img_width, img_height, r) = image_properties(img)
    result_img = np.zeros((img_width, img_height))
    result_counter = np.zeros((img_width, img_height))


    detectors_n = len(sinogram[0])
    iter_n = len(sinogram)
    print("INVERSE RADON")
    for i in range(iter_n):
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
                    result_counter[point[0]][point[1]] += 1
                    result_img[point[0]][point[1]] += sinogram[i][detector]
    for i in range(img_width):
        for j in range(img_height):
            if result_counter[i][j] > 0:
                result_img[i][j] = result_img[i][j]/result_counter[i][j]
    return result_img
