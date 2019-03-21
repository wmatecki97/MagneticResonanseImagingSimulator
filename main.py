from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np
from tomography import radon, inverse_radon
import time

alpha = 1 #kat obrotu
n = 180 #liczba detektorow
d = 180 #rozpietosc
numberOfThreads = 8
mask=[-30,61,-30]
saveResult=False

image = color.rgb2gray(io.imread('picbrain.jpg'))

start = time.time()
#plt.imshow(image, cmap='gray')
#plt.show()

plt.figure(figsize=(5,10))
sinogram, measures = radon(image, n, alpha, d, numberOfThreads, mask)
arr = np.asarray(sinogram)
arr = np.transpose(arr)

end = time.time()
print(end - start)
plt.subplot(211)
plt.imshow(arr, cmap='gray')
plt.show(block=False)


sino = np.copy(sinogram)

inverse = inverse_radon(image, sino, n, alpha, d, numberOfThreads)
if saveResult:
    plt.imsave('wynik' + str(n) + '_' +str(mask[0])+'_'+str(mask[1])+'_'+str(mask[2]), inverse)
