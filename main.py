from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np
from tomography import radon, inverse_radon

alpha = 1 #kat obrotu
n = 400 #liczba detektorow
d = 180 #rozpietosc

image = color.rgb2gray(io.imread('picbrain.jpg'))

plt.imshow(image, cmap='gray')
plt.show()

sinogram = radon(image, n, alpha, d)
arr = np.asarray(sinogram)
arr = np.transpose(arr)

plt.imshow(arr, cmap='gray')
plt.show()

inverse = inverse_radon(image, sinogram, n, alpha, d)
plt.imshow(inverse, cmap='gray')
plt.show()