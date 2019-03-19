from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np
from tomography import radon, inverse_radon
import time

alpha = 1 #kat obrotu
n = 400 #liczba detektorow
d = 180 #rozpietosc
numberOfThreads = 8

image = color.rgb2gray(io.imread('picbrain.jpg'))

start = time.time()
#plt.imshow(image, cmap='gray')
plt.show()

sinogram, measures = radon(image, n, alpha, d, numberOfThreads)
arr = np.asarray(sinogram)
arr = np.transpose(arr)

end = time.time()
print(end - start)
plt.imshow(arr, cmap='gray')
plt.show()

sino = np.copy(sinogram)
inverse = inverse_radon(image, sino, n, alpha, d)
plt.imshow(inverse, cmap='gray')
plt.show()
