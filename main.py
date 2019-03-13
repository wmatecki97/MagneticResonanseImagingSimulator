from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np
from tomography import radon

alpha = 1 #kat obrotu
n = 300 #liczba detektorow
d = 90 #rozpietosc

image = color.rgb2gray(io.imread('Kropka.jpg'))

plt.imshow(image, cmap='gray')
plt.show()

sinogram = radon(image, n, alpha, d)
arr = np.asarray(sinogram)
arr = np.transpose(arr)

plt.imshow(arr, cmap='gray')
plt.show()
