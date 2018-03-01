import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import wiener, filtfilt, butter, gaussian, freqz
from scipy.ndimage import filters
import scipy.optimize as op
import matplotlib.pyplot as plt


x = np.arange(40)
y = np.log(x + 1) * np.exp(-x/8.) * x**2 + np.random.random(40) * 15
rft = np.fft.rfft(y)
print('rft at this point is \n', rft)
rft[5:] = 0   # Note, rft.shape = 21
y_smooth = np.fft.irfft(rft)


print("y is ")
print(y)
print("rft is ", rft)

plt.plot(x, y, label='Original')
plt.plot(x, y_smooth, label='Smoothed')
plt.legend(loc=0).draggable()
plt.show()


'''
numpy.fft.fft(a, n=None, axis=-1, norm=None)[source]
Compute the one-dimensional discrete Fourier Transform.

This function computes the one-dimensional n-point discrete Fourier Transform (DFT) with the efficient Fast Fourier Transform (FFT) algorithm [CT].

Parameters:
a : array_like
    Input array, can be complex.
n : int, optional
    Length of the transformed axis of the output. If n is smaller than the length of the input, the input is cropped. If it is larger, the input is padded with zeros. If n is not given, the length of the input along the axis specified by axis is used.
axis : int, optional
     Axis over which to compute the FFT. If not given, the last axis is used.
norm : {None, “ortho”}, optional
New in version 1.10.0.
Normalization mode (see numpy.fft). Default is None.
Returns:
out : complex ndarray
The truncated or zero-padded input, transformed along the axis indicated by axis, or the last one if axis is not specified.
Raises:
IndexError
    if axes is larger than the last axis of a.

'''
