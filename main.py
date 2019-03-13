from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np
from tomography import radon
import time

alpha = 1 #kat obrotu
n = 300 #liczba detektorow
d = 90 #rozpietosc
numberOfThreads = 24
image = color.rgb2gray(io.imread('Kropka.jpg'))

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
